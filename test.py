import json


with open('all_questions_math.json', 'r') as f:
    all_questions = json.load(f)


with open('fhwof.json', 'w') as f:
    json.dump(all_questions[0], f, indent=4)
