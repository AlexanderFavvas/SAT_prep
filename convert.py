import json

def create_html_visualization(json_file_path, output_html_path):
    """
    Reads a JSON file containing question data, takes the first question,
    and generates an HTML file to visualize it.

    Args:
        json_file_path (str): Path to the input JSON file.
        output_html_path (str): Path to save the output HTML file.
    """
    with open(json_file_path, 'r') as f:
        questions_data = json.load(f)

    if not questions_data:
        print("No questions found in the JSON file.")
        return

    question = questions_data[0] # Taking the first question as specified

    stem_html = question.get("stem", "")
    answer_options = question.get("answerOptions", [])
    correct_answer_keys = question.get("keys", [])
    rationale_html = question.get("rationale", "")

    # Determine the letter for each answer option (A, B, C, D, ...)
    option_letters = [chr(65 + i) for i in range(len(answer_options))]

    # Map correct answer IDs to their letters
    correct_answer_letters = []
    for i, option in enumerate(answer_options):
        if option.get("id") in correct_answer_keys:
            correct_answer_letters.append(option_letters[i])


    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Visualization</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 20px;
        }}
        .question-stem {{
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .answer-options ul {{
            list-style-type: none;
            padding: 0;
        }}
        .answer-options li {{
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 5px;
        }}
        .answer-options li.correct {{
            background-color: #e6ffe6;
            border-left: 5px solid #4CAF50;
        }}
        .rationale {{
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        figure.image svg {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>

    <h2>Question:</h2>
    <div class="question-stem">
        {stem_html}
    </div>

    <h2>Answer Options:</h2>
    <div class="answer-options">
        <ul>
"""

    for i, option in enumerate(answer_options):
        option_id = option.get("id")
        option_content = option.get("content", "")
        is_correct = option_id in correct_answer_keys
        correct_class = "correct" if is_correct else ""
        html_content += f'            <li class="{correct_class}"><strong>{option_letters[i]}.</strong> {option_content}</li>\n'

    html_content += """
        </ul>
    </div>
"""

    if rationale_html:
        html_content += f"""
    <h2>Rationale:</h2>
    <div class="rationale">
        {rationale_html}
    </div>
"""

    html_content += """
</body>
</html>
"""

    with open(output_html_path, 'w') as f:
        f.write(html_content)
    print(f"HTML visualization saved to {output_html_path}")

if __name__ == "__main__":
    json_file = "all_questions.json"
    html_file = "question_visualization.html"
    create_html_visualization(json_file, html_file)