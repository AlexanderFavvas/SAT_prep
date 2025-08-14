import json

target_difficulty = "H"
target_dataset = f"filtered_questions_{target_difficulty}.json"

with open(target_dataset, "r") as f:
    all_questions = json.load(f)

system_prompt = """You are a JSON SAT practice question generator. You always generate questions that conform to the following constraints: 1. The answer must be correct 2. There must clearly be only one correct answer, and all others must be clearly incorrect 3. Nothing may be ambiguous 4. All required knowledge to solve the question must be standard (e.g. high schools must teach, official study guides must teach, etc), and follow the common patterns of the SAT."""
user_prompt = "Generate a random question."

examples = []

for ground_truth_question in all_questions:
    examples.append({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": str(ground_truth_question)}
    ]})





with open("training_data.jsonl", "w", encoding="utf-8") as f:
    for ex in examples:
        json_line = json.dumps(ex, ensure_ascii=False)
        f.write(json_line + "\n")
