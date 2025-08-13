from sentence_transformers import SentenceTransformer
from show_test import HTMLViewer
import random
import json


def get_question_html(match):
    html = f"<div>{match['stem']}</div>"
    html += "<ol type='A'>"
    for option in match['answerOptions']:
        html += f"<li><div>{option['content']}</div></li>"
    html += "</ol>"
    return html

# currently only works for math

with open("all_questions_math_non_live.json", "r") as f:
    all_questions = json.load(f)

try:
    with open ("correct_questions.json", "r") as f:
        correct_questions = json.load(f)
except Exception as e:
    correct_questions = []
try:
    with open("incorrect_questions.json", "r") as f:
        incorrect_questions = json.load(f)
except Exception as e:
    incorrect_questions = []


temp = []
for question in all_questions:
    if question['difficulty'] == "H":
        temp.append(question)
all_questions = temp; del temp

random.shuffle(all_questions)



viewer = HTMLViewer()
question_page = viewer.show("<html><body>Waiting for question...</body></html>", "Question")
rationale_page = viewer.show("<html><body>Waiting for rationale...</body></html>", "Rationale")


for question in all_questions:
    question_html = get_question_html(question)
    viewer.update(question_page, question_html, f"Question")
    input("Press Enter to show rationale...")
    viewer.update(rationale_page, question['rationale'], f"Rationale for Question")
    while True:
        correct = input("Correct? [y/n]").strip().lower()
        if correct == 'y':
            correct_questions.append(question)
            break
        elif correct == 'n':
            incorrect_questions.append(question)
            break
        else:
            print("Incorrect response. Please enter either 'y' for Yes, or 'n' for No.")
    with open("correct_questions.json", "w") as f:
        json.dump(correct_questions, f, indent = 4)
    with open("incorrect_questions", "w") as f:
        json.dump(incorrect_questions, f, indent = 4)
