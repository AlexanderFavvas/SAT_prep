from PIL import Image
from io import BytesIO
import json
from playwright.sync_api import sync_playwright


class HTMLViewer:
    def __init__(self):
        """Launches a persistent browser instance."""
        self.playwright = sync_playwright().start()
        # Launch headless=False to make the browser window visible.
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.pages = []

    def _get_full_html(self, html, title):
        """Wraps content in a full HTML document."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            <title>{title}</title>
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

    def show(self, html, title="Content"):
        """Shows HTML content in a new browser page."""
        page = self.context.new_page()
        full_html = self._get_full_html(html, title)
        page.set_content(full_html)
        self.pages.append(page)
        return page

    def update(self, page, html, title="Content"):
        """Updates HTML content in an existing page."""
        full_html = self._get_full_html(html, title)
        page.set_content(full_html)
        page.bring_to_front()

    def close_page(self, page):
        """Closes a specific page."""
        if page and not page.is_closed():
            try:
                page.close()
                if page in self.pages:
                    self.pages.remove(page)
            except Exception:
                # Page might already be closing or closed.
                pass

    def close(self):
        """Closes the browser and stops Playwright."""
        if hasattr(self, 'browser') and self.browser:
            self.browser.close()
        if hasattr(self, 'playwright') and self.playwright:
            self.playwright.stop()

