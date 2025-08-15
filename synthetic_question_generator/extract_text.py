
text = {
"stem": """<p style="text-align: center;"><math alttext="x left parenthesis 5 y plus 7 right parenthesis equals 3 y minus 10"><mi>x</mi><mfenced><mrow><mrow><mn>5</mn></mrow><mi>y</mi><mo>+</mo><mrow><mn>7</mn></mrow></mrow></mfenced><mo>=</mo><mrow><mn>3</mn></mrow><mi>y</mi><mo>-</mo><mrow><mn>10</mn></mrow></math></p>\n<p style="text-align: left;">The given equation has solutions for <math alttext="x"><mi>x</mi>\n</math>. Which option is a possible value of <math alttext="y"><mi>y</mi>\n</math>?</p>"""
}


import re
from typing import Dict

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None  # type: ignore


def _replace_math_with_alttext(soup) -> None:
    if soup is None:
        return
    for math_tag in soup.find_all("math"):
        alt_text = math_tag.get("alttext")
        replacement_text = alt_text if alt_text else math_tag.get_text(" ", strip=True)
        math_tag.replace_with(replacement_text)


def _strip_unwanted_tags(soup) -> None:
    if soup is None:
        return
    for tag_name in ["figure", "svg", "script", "style"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()


def _normalize_startfraction(text: str) -> str:
    if not text:
        return text
    pattern = re.compile(r"\bStartFraction\b(.*?)\bOver\b(.*?)\bEndFraction\b", flags=re.IGNORECASE)
    while True:
        new_text, count = pattern.subn(lambda m: f"({m.group(1).strip()}) / ({m.group(2).strip()})", text)
        if count == 0:
            break
        text = new_text
    return text


def _normalize_exponent_words(text: str) -> str:
    if not text:
        return text
    # Parenthesized expression followed by 'squared' or 'cubed'
    patterns = [
        (re.compile(r"(\([^()]+\))\s*squared\b", flags=re.IGNORECASE), r"\1²"),
        (re.compile(r"(\([^()]+\))\s*cubed\b", flags=re.IGNORECASE), r"\1³"),
        # Simple token (variable/number) followed by 'squared' or 'cubed'
        (re.compile(r"\b([A-Za-z0-9]+)\s*squared\b", flags=re.IGNORECASE), r"\1²"),
        (re.compile(r"\b([A-Za-z0-9]+)\s*cubed\b", flags=re.IGNORECASE), r"\1³"),
    ]
    changed = True
    while changed:
        changed = False
        for pat, repl in patterns:
            new_text, count = pat.subn(repl, text)
            if count:
                changed = True
                text = new_text
    return text


def _apply_word_replacements(text: str) -> str:
    replacements = [
        (r"\bleft parenthesis\b", "("),
        (r"\bright parenthesis\b", ")"),
        (r"\bcomma\b", ","),
        (r"\bStartRoot\b", "√("),
        (r"\bEndRoot\b", ")"),
        (r"\bupper\s+([A-Za-z])\b", r"\1"),
        (r"\bequals\b", "="),
        (r"\bpi\b", "π"),
        (r"\bminus\b", "−"),
        (r"\bnegative\b", "−"),
        (r"\bplus\b", "+"),
    ]
    normalized = text
    for pattern, repl in replacements:
        normalized = re.sub(pattern, repl, normalized, flags=re.IGNORECASE)
    return normalized


def _normalize_math_words_to_symbols(text: str) -> str:
    if not text:
        return text

    # Fractions first
    text = _normalize_startfraction(text)

    # First-pass token cleanup (parenthesis words, etc.) before exponent handling
    text = _apply_word_replacements(text)

    # Handle combined operators before single-word replacements
    text = re.sub(r"\bplus\s+or\s+minus\b", "±", text, flags=re.IGNORECASE)
    text = re.sub(r"\bplus\s+or\s+[\-−]\b", "±", text, flags=re.IGNORECASE)

    # Exponent words (squared/cubed)
    text = _normalize_exponent_words(text)

    # Second pass to eliminate any tokens introduced near exponents
    text = _apply_word_replacements(text)

    # Clean spaces around punctuation, operators, and parentheses
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+,\s*", ", ", text)
    text = re.sub(r"\s+([+−=×/])\s+", r" \1 ", text)

    # Collapse any leftover excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def html_to_plain_text(html_str: str) -> str:
    if not html_str:
        return ""

    # Preferred path: BeautifulSoup for robust parsing
    if BeautifulSoup is not None:
        soup = BeautifulSoup(html_str, "html.parser")
        _strip_unwanted_tags(soup)
        _replace_math_with_alttext(soup)
        plain_text = soup.get_text(" ", strip=True)
    else:
        # Fallback: regex-based stripping with special handling for MathML alttext
        tmp = html_str
        # Replace math blocks with their alttext when present
        tmp = re.sub(r'<math[^>]*alttext="([^"]+)"[^>]*>.*?</math>', r'\1', tmp, flags=re.DOTALL | re.IGNORECASE)
        # Drop script/style/svg/figure contents entirely
        tmp = re.sub(r'<(script|style|svg|figure)\b[^>]*>.*?</\1>', ' ', tmp, flags=re.DOTALL | re.IGNORECASE)
        # Strip remaining tags
        tmp = re.sub(r'<[^>]+>', ' ', tmp)
        # Collapse whitespace
        plain_text = re.sub(r'\s+', ' ', tmp).strip()

    try:
        from html import unescape
        plain_text = unescape(plain_text)
    except Exception:
        pass

    # Normalize verbose MathML alttext wording to readable symbols
    plain_text = _normalize_math_words_to_symbols(plain_text)

    return plain_text


def build_readable_text(item: Dict) -> str:
    parts = []

    origin = item.get("origin")
    if origin:
        parts.append(f"Origin: {origin}")

    stem_html = item.get("stem")
    if stem_html:
        parts.append("Question:")
        parts.append(html_to_plain_text(stem_html))

    answer_options = item.get("answerOptions") or []
    if answer_options:
        parts.append("Choices:")
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for idx, option in enumerate(answer_options):
            label = letters[idx] if idx < len(letters) else f"Option {idx+1}"
            content_html = option.get("content", "")
            content_text = html_to_plain_text(content_html)
            parts.append(f"{label}) {content_text}")

    correct_letters = item.get("correct_answer") or []
    numeric_keys = item.get("keys") or []

    if correct_letters:
        parts.append(f"Correct: {', '.join(correct_letters)}")
    elif numeric_keys:
        letters = []
        for key in numeric_keys:
            try:
                index_one_based = int(key)
                letters.append("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index_one_based - 1])
            except Exception:
                letters.append(str(key))
        parts.append(f"Correct: {', '.join(letters)}")

    rationale_html = item.get("rationale")
    if rationale_html:
        parts.append("Explanation:")
        parts.append(html_to_plain_text(rationale_html))

    difficulty = item.get("difficulty")
    if difficulty:
        parts.append(f"Difficulty: {difficulty}")

    return "\n".join(parts)


if __name__ == "__main__":
    print(build_readable_text(text))
