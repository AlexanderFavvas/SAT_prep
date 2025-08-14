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
    question = 




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