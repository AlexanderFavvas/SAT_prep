from sentence_transformers import SentenceTransformer, util
import json
from show_test import HTMLViewer
import pickle
import torch
import os
import random

all_questions_filepath = "all_questions_math.json"

difficulty = 'H' # 'H' for hard, 'M' for medium, 'E' for easy, False for all

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_question_html(match):
    html = f"<div>{match['stem']}</div>"
    html += "<ol type='A'>"
    for option in match['answerOptions']:
        html += f"<li><div>{option['content']}</div></li>"
    html += "</ol>"
    return html


k = 5  # higher k means more similar questions

# Text contained within the target questions. They act as unique identifiers.
keyphrases = [
    """ is the first term of the sequence, the value of""",
    """Expanding the left-hand side of this equation yields""",
    """in this formula, the slope of the line can be calculated as""",
    """sides of this equation must be equal, and the constant terms on both sides of this equation must not be equal""",
    """right parenthesis x plus k j\"><mi>h</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mfenced><mrow><m""",
    """Choice C is correct. The median of a data set with an odd number of values, in ascending or descending order""",
    """that the graph shown is a partial graph of""",
    "The left-hand side of the given equation is the expression",
    " positive, the parabola will open upward, and"

]

with open(all_questions_filepath, "r") as f:
    all_questions = json.load(f)
    if difficulty:
        all_questions = [q for q in all_questions if q['difficulty'] == difficulty]


blacklist_path = "blacklist.json"
if os.path.exists(blacklist_path):
    print("Loading blacklist from blacklist.json")
    with open(blacklist_path, "r") as f:
        blacklist = set(json.load(f))
else:
    blacklist = set()

if os.path.exists("preprocessed.pkl"):
    print("Loading preprocessed embeddings from preprocessed.pkl")
    with open("preprocessed.pkl", "rb") as f:
        preprocessed = pickle.load(f)
else:
    print("Generating embeddings and saving to preprocessed.pkl")
    preprocessed = []

    #generate embeddings
    for i, thing in enumerate(all_questions):
        print(f'[{i}/{len(all_questions)}]')
        preprocessed.append([i, model.encode(thing['rationale'], convert_to_tensor=False).tolist()])

    with open("preprocessed.pkl", "wb") as f:
        pickle.dump(preprocessed, f)




all_embeddings = torch.tensor([p[1] for p in preprocessed])

matches = []

for i, thing in enumerate(all_questions):
    if thing.get('id') in blacklist:
        continue
    rationale = thing['rationale']
    for keyphrase in keyphrases:
        if keyphrase in rationale:
            if 'id' not in thing or not any(m['id'] == thing['id'] for m in matches):
                thing['original_index'] = i
                matches.append(thing)



print(f"\nFound {len(matches)} questions matching keyphrases.")
if matches:
    random.shuffle(matches)
    print("Finding most similar questions...")



viewer = HTMLViewer()
final_questions = []

question_page = viewer.show("<html><body>Waiting for question...</body></html>", "Question")
rationale_page = viewer.show("<html><body>Waiting for rationale...</body></html>", "Rationale")
print(f'{len(matches)} matches found')
for i, match in enumerate(matches, 1):
    embedding = all_embeddings[match['original_index']]
    
    cosine_scores = util.cos_sim(embedding, all_embeddings)
    
    # Exclude the question itself and other initial matches from the similarity search
    for m in matches:
        cosine_scores[0][m['original_index']] = -1
    
    
    top_results = torch.topk(cosine_scores[0], k=k)
    top_indices = top_results.indices.tolist()


    for idx, index in enumerate(top_indices, 1):
        best_match_question = all_questions[index]
        final_questions.append([best_match_question, match])


random.shuffle(final_questions)


try:
    for question in final_questions:
        question_html = get_question_html(question[0])
        viewer.update(question_page, question_html, f"Question")
        
        debug = input(f"Press Enter to show rationale...").strip().lower()
        if debug == 'debug':
            with open("debug.json", "w") as f:
                json.dump({"question": question, "question_html": question_html}, f, indent=4)
        elif debug == 'show_original':
            viewer.update(question_page, get_question_html(question[1]), f"Original Question")
        debug = False
        
        viewer.update(rationale_page, question[0]['rationale'], f"Rationale for Question")
        debug = input(f"Press Enter to continue...").strip().lower()
        if debug == 'debug':
            with open("debug.json", "w") as f:
                json.dump({"question": question, "rationale": question[0]['rationale']}, f, indent=4)
        debug = False

except KeyboardInterrupt:
    print("\nClosing browser...")
    viewer.close()
