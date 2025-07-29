from sentence_transformers import SentenceTransformer, util
import json
from show_test import HTMLViewer
import pickle
import torch
import os
import random


model = SentenceTransformer("all-MiniLM-L6-v2")

def get_question_html(match):
    html = f"<div>{match['stem']}</div>"
    html += "<ol type='A'>"
    for option in match['answerOptions']:
        html += f"<li><div>{option['content']}</div></li>"
    html += "</ol>"
    return html


k = 2  # higher k means more similar questions

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

with open("all_questions.json", "r") as f:
    all_questions = json.load(f)

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

blacklisted_indices = {
    i for i, q in enumerate(all_questions)
    if q.get('id') in blacklist
}

viewer = HTMLViewer()
try:
    question_page = viewer.show("<html><body>Waiting for question...</body></html>", "Question")
    rationale_page = viewer.show("<html><body>Waiting for rationale...</body></html>", "Rationale")
    print(f'{len(matches)} matches found, with {len(blacklisted_indices)} blacklisted\n\n{"="*100}\n\n')
    for i, match in enumerate(matches, 1):
        embedding = all_embeddings[match['original_index']]
        
        cosine_scores = util.cos_sim(embedding, all_embeddings)
        
        # Exclude the question itself and other initial matches from the similarity search
        for m in matches:
            cosine_scores[0][m['original_index']] = -1
        
        # Exclude blacklisted questions
        for idx_bl in blacklisted_indices:
            cosine_scores[0][idx_bl] = -1
        
        top_results = torch.topk(cosine_scores[0], k=k)
        top_indices = top_results.indices.tolist()

        print(f"\nFound {len(top_indices)} similar questions for Match {i}:")

        for idx, index in enumerate(top_indices, 1):
            best_match_question = all_questions[index]
            print(f"\n--- Similar Question {idx}/{len(top_indices)} ---")

            question_html = get_question_html(best_match_question)
            viewer.update(question_page, question_html, f"Similar Question {idx}")
            
            input(f"Press Enter to show rationale...")

            viewer.update(rationale_page, best_match_question['rationale'], f"Rationale for Similar Question {idx}")


            got_it_right = input("Did you get it right? [y/n]: ").lower().strip() == 'y'


            if got_it_right:
                question_id = best_match_question.get('id')
                if question_id:
                    blacklist.add(question_id)
                    blacklisted_indices.add(index)
                    with open(blacklist_path, "w") as f:
                        json.dump(list(blacklist), f)
                    print(f"Question {question_id} added to blacklist. It will not be shown again.")

            if idx < len(top_indices):
                input(f"Press Enter to continue to the next similar question...")
            else:
                input(f"Press Enter to continue to the next main match...")
finally:
    print("Closing browser...")
    viewer.close()