from sentence_transformers import SentenceTransformer, util
import json
from show_test import show_html
import pickle
import torch
import os


model = SentenceTransformer("all-MiniLM-L6-v2")

def show_html_helper(match):
    html = match['stem']
    html += "<ol type='A'>"
    for option in match['answerOptions']:
        html += f"<li>{option['content']}</li>"
    html += "</ol>"
    show_html(html)


k = 2  # higher k means more similar questions

keyphrases = [
    """ is the first term of the sequence, the value of""",
    """Expanding the left-hand side of this equation yields""",
    """"""
]

with open("all_questions.json", "r") as f:
    all_questions = json.load(f)

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
    rationale = thing['rationale']
    for keyphrase in keyphrases:
        if keyphrase in rationale:
            if 'id' not in thing or not any(m['id'] == thing['id'] for m in matches):
                thing['original_index'] = i
                matches.append(thing)



print(f"\nFound {len(matches)} questions matching keyphrases.")
if matches:
    print("Finding most similar questions...")

for match in matches:
    embedding = all_embeddings[match['original_index']]
    
    cosine_scores = util.cos_sim(embedding, all_embeddings)
    
    cosine_scores[0][match['original_index']] = -1
    
    top_results = torch.topk(cosine_scores[0], k=k)
    top_scores = top_results.values.tolist()
    top_indices = top_results.indices.tolist()
    
    print("\n" + "="*40)
    print("Original question (matched by keyphrase):")
    show_html_helper(match)

    for idx, (score, best_match_index) in enumerate(zip(top_scores, top_indices), 1):
        best_match_question = all_questions[best_match_index]
        print(f"\nMost similar question #{idx} (Cosine Similarity: {score:.4f}):")
        show_html_helper(best_match_question)
        input(f"Press Enter to continue to the next match #{idx} and show answer...")
        print(best_match_question['rationale'])