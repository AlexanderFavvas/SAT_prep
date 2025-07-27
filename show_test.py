from PIL import Image
from io import BytesIO
import json
from playwright.sync_api import sync_playwright

with open("all_questions.json", "r") as f:
    all_questions = json.load(f)

def show_html(html):
    # Wrap the partial HTML in a full document structure for the browser
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            body {{
                margin: 0;
                padding: 1em;
                background-color: white;
                /* Set a reasonable width for the content */
                width: 800px; 
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html)

        # Wait for MathJax to finish rendering. 
        # It adds a <mjx-container> element, so we wait for the first one to appear.
        try:
            page.wait_for_selector('mjx-container', timeout=15000)
        except Exception as e:
            print(f"MathJax did not render in time: {e}")

        # Find the body element to screenshot just the content
        body = page.query_selector('body')
        if body:
            # Take screenshot of just the body element
            img_bytes = body.screenshot(type='png')
        else:
            # Fallback to full page screenshot if body isn't found
            img_bytes = page.screenshot(type='png')
        
        browser.close()

    image = Image.open(BytesIO(img_bytes))
    image.show()

