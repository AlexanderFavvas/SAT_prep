import json
import copy
import math

target_dataset = "all_questions_math.json"
target_difficulty = "H"

with open(target_dataset, "r") as f:
    all_questions = json.load(f)

# Filter by difficulty first
pool = [q for q in all_questions if q['difficulty'] == target_difficulty]

# Remove top 10% longest within this pool
k = math.ceil(0.10 * len(pool))
if k > 0:
    pool = sorted(pool, key=lambda q: len(str(q)))[:-k]

filtered_questions = []
for question in pool:
    question_copy = {}
    question_copy['stem'] = question['stem']
    for x in question:
        if x != 'difficulty' and x != 'origin' and x != 'templateid' and x != 'vaultid' and x != 'externalid' and x != 'keys' and x != 'stem':
            question_copy[x] = question[x]
    if question['type'] == 'mcq':
        correct_id = question['keys'][0]
        for option in question_copy['answerOptions']:
            if option['id'] == correct_id:
                option['id'] = question_copy['correct_answer'][0]
            else:
                index = question_copy['answerOptions'].index(option)
                if index == 0:
                    option['id'] = 'A'
                elif index == 1:
                    option['id'] = 'B'
                elif index == 2:
                    option['id'] = 'C'
                elif index == 3:
                    option['id'] = 'D'
    filtered_questions.append(question_copy)

with open("filtered_questions.json", "w") as f:
    json.dump(filtered_questions, f, indent=4)
print(len(filtered_questions))