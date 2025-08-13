import json

target_dataset = "all_questions_math.json"
target_difficulty = "H"

with open(target_dataset, "r") as f:
    all_questions = json.load(f)


filtered_questions = []
for question in all_questions:
    if question['difficulty'] == target_difficulty:
        filtered_questions.append(question)

with open(f"filtered_questions_{target_difficulty}.json", "w") as f:
    json.dump(filtered_questions, f, indent = 4)
print(len(filtered_questions))