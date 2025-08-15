import json


target_dataset = "synthetic_question_generator/filtered_questions.json"

with open(target_dataset, "r") as f:
    all_questions = json.load(f)

import random

# Shuffle the questions to ensure randomness
random.shuffle(all_questions)

n_total = len(all_questions)
num_generate_stem = max(1, int(0.3 * n_total))
num_generate_random = max(1, int(0.4 * n_total))
num_give_stem_and_answer = max(0, n_total - num_generate_stem - num_generate_random)

generate_stem = all_questions[:num_generate_stem]
give_stem_and_answer = all_questions[num_generate_stem:num_generate_stem + num_give_stem_and_answer]
generate_random = all_questions[num_generate_stem + num_give_stem_and_answer:]



system_prompt = """You are a JSON SAT practice question generator. You always generate questions that conform to the following constraints: 1. The answer must be correct 2. There must clearly be only one correct answer, and all others must be clearly incorrect 3. Nothing may be ambiguous 4. All required knowledge to solve the question must be standard (e.g. high schools must teach, official study guides must teach, etc), and follow the common patterns of the SAT."""
generate_random_prompt = "Generate a random question."


examples = []

for ground_truth_question in generate_random:
    examples.append({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": generate_random_prompt},
        {"role": "assistant", "content": json.dumps(ground_truth_question)}
    ]})

for ground_truth_question in generate_stem:
    stem = ground_truth_question['stem']
    examples.append({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a random stem."},
        {"role": "assistant", "content": json.dumps({"stem": stem})}
    ]})

for ground_truth_question in give_stem_and_answer:
    stem = ground_truth_question['stem']
    answer = ground_truth_question['correct_answer'][0]
    if answer == 'A' or answer == 'B' or answer == 'C' or answer == 'D':
        for option in ground_truth_question['answerOptions']:
            if option['id'] == answer:
                answer = option['content']
    else:
        answer = f"<p><math alttext=\"{answer}\"><mn>{answer}</mn></math></p>"
    examples.append({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a question with the following stem: {stem} and the following answer: {answer}"},
        {"role": "assistant", "content": json.dumps(ground_truth_question)}
    ]})




random.shuffle(examples)
with open("training_data.jsonl", "w", encoding="utf-8") as f:
    for ex in examples:
        json_line = json.dumps(ex, ensure_ascii=False)
        f.write(json_line + "\n")
