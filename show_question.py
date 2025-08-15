import json
import os
import random
from show_test import HTMLViewer


def get_question_html(question):
    html = f"<div>{question['stem']}</div>"
    html += "<ol type='A'>"
    for option in question['answerOptions']:
        html += f"<li><div>{option['content']}</div></li>"
    html += "</ol>"
    return html


def main():
    question = {
  "stem": "<p style=\"text-align: left;\">A function <math alttext=\"f\"><mi>f</mi>\n</math> is defined by <math alttext=\"f left parenthesis x right parenthesis equals 2 left parenthesis x minus 6 right parenthesis left parenthesis x plus 6 right parenthesis\"><mi>f</mi><mfenced><mi>x</mi></mfenced><mo>=</mo><mrow><mn>2</mn></mrow><mfenced><mrow><mi>x</mi><mo>-</mo><mrow><mn>6</mn></mrow></mrow></mfenced><mfenced><mrow><mi>x</mi><mo>+</mo><mrow><mn>6</mn></mrow></mrow></mfenced></math>. For what value of <math alttext=\"x\"><mi>x</mi>\n</math> does <math alttext=\"f left parenthesis x right parenthesis\"><mi>f</mi><mfenced><mi>x</mi></mfenced></math> reach its minimum?</p>",
  "type": "spr",
  "answerOptions": [],
  "rationale": "<ul>\n<li style=\"text-align: left;\">The correct answer is <math alttext=\"0\"><mn>0</mn>\n</math>.</li>\n<li style=\"text-align: left;\">The function <math alttext=\"f\"><mi>f</mi>\n</math> is defined by <math alttext=\"f left parenthesis x right parenthesis equals 2 left parenthesis x minus 6 right parenthesis left parenthesis x plus 6 right parenthesis\"><mi>f</mi><mfenced><mi>x</mi></mfenced><mo>=</mo><mn>2</mn><mfenced><mrow><mi>x</mi><mo>-</mo><mn>6</mn></mrow></mfenced><mfenced><mrow><mi>x</mi><mo>+</mo><mn>6</mn></mrow></mfenced></math>, or <math alttext=\"f left parenthesis x right parenthesis equals 2 x squared minus 72\"><mi>f</mi><mfenced><mi>x</mi></mfenced><mo>=</mo><mn>2</mn><msup><mi>x</mi><mn>2</mn></msup><mo>-</mo><mn>72</mn></math>. This function can be rewritten in the form <math alttext=\"f left parenthesis x right parenthesis equals a left parenthesis x minus h right parenthesis squared plus k\"><mi>f</mi><mfenced><mi>x</mi></mfenced><mo>=</mo><mi>a</mi><msup><mfenced><mrow><mi>x</mi><mo>-</mo><mi>h</mi></mrow></mfenced><mn>2</mn></msup><mo>+</mo><mi>k</mi></math>, where <math alttext=\"a\"><mi>a</mi>\n</math>, <math alttext=\"h\"><mi>h</mi>\n</math>, and <math alttext=\"k\"><mi>k</mi>\n</math> are constants. This form shows that the graph of the function in the <em>xy</em>-plane is a parabola with vertex <math alttext=\"left parenthesis h comma k right parenthesis\"><mfenced><mrow><mi>h</mi><mo>,</mo><mi>k</mi></mrow></mfenced></math> and opens upward if <math alttext=\"a greater than 0\"><mi>a</mi><mo>&gt;</mo><mn>0</mn></math> or downward if <math alttext=\"a less than 0\"><mi>a</mi><mo>&lt;</mo><mn>0</mn></math>. It follows that the minimum or maximum of the function is reached at <math alttext=\"x equals h\"><mrow>\n\t<mi>x</mi>\n\t<mo>=</mo>\n\t<mi>h</mi>\n</mrow>\n</math>. The given function can be rewritten as <math alttext=\"f left parenthesis x right parenthesis equals 2 left parenthesis x squared minus 0 x plus left parenthesis minus 72 right parenthesis right parenthesis\"><mi>f</mi><mfenced><mi>x</mi></mfenced><mo>=</mo><mn>2</mn><mfenced><mrow><msup><mi>x</mi><mn>2</mn></msup><mo>-</mo><mn>0</mn><mi>x</mi><mo>+</mo><mfenced><mrow><mo>-</mo><mn>72</mn></mrow></mfenced></mrow></mfenced></math>. Therefore, the minimum of the function is reached at <math alttext=\"x equals StartFraction minus 0 Over 2 left parenthesis 2 right parenthesis EndFraction\"><mi>x</mi><mo>=</mo><mfrac><mrow><mo>-</mo><mn>0</mn></mrow><mrow><mn>2</mn><mfenced><mn>2</mn></mfenced></mrow></mfrac></math>, or <math alttext=\"x equals 0\"><mrow>\n\t<mi>x</mi>\n\t<mo>=</mo>\n\t<mn>0</mn>\n</mrow>\n</math>. Note that 0 must be entered in the response field to be considered correct.</li>\n</ul>",
  "correct_answer": [
    "0"
  ]
}


    viewer = HTMLViewer()
    try:
        question_html = get_question_html(question)
        question_page = viewer.show("<html><body>Waiting for question...</body></html>", "Question")
        rationale_page = viewer.show("<html><body>Waiting for rationale...</body></html>", "Rationale")

        viewer.update(question_page, question_html, "Question")
        input("Press Enter to show rationale...")
        viewer.update(rationale_page, question['rationale'], "Rationale")
        input("Press Enter to close...")
    finally:
        viewer.close()


if __name__ == "__main__":
    main() 