import pickle
import json
from sentence_transformers import SentenceTransformer, util
from show_test import HTMLViewer


def get_question_html(match):
    html = match['stem']
    html += "<ol type='A'>"
    for option in match['answerOptions']:
        html += f"<li>{option['content']}</li>"
    html += "</ol>"
    return html


with open('preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)


with open('all_questions.json', 'r') as f:
    all_questions = json.load(f)

keyphrase = "sides of this equation must be equal, and the constant terms on both sides of this equation must not be equal"

matches = []

for idx, item in enumerate(all_questions):
    if keyphrase in item['rationale']:
        matches.append([item, data[idx][1]])


cosine_scores = util.cos_sim(matches[0][1], [data[idx][1] for idx in range(len(data))])



k = 5
topk = cosine_scores[0].topk(k)
top_indices = topk.indices.tolist()

viewer = HTMLViewer()
try:
    question_page = viewer.show("<html><body>Waiting for question...</body></html>", "Question")
    rationale_page = viewer.show("<html><body>Waiting for rationale...</body></html>", "Rationale")

    for i, idx in enumerate(top_indices):
        question = all_questions[idx]

        question_html = get_question_html(question)
        viewer.update(question_page, question_html, f"Similar Question {i + 1}")

        input("Press Enter to show rationale...")

        viewer.update(rationale_page, question['rationale'], f"Rationale for Similar Question {i + 1}")

        if i < len(top_indices) - 1:
            input("Press Enter to continue to the next similar question...")
finally:
    print("Closing browser...")
    viewer.close()








