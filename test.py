import json

with open('all_questions_math_non_live.json', 'r') as f:
    all_questions = json.load(f)



lengths = []
total_length = 0
for question in all_questions:
    lengths.append(len(str(question)))
    total_length += len(str(question))


print(f"Total length: {total_length}")
print(f"Average length: {total_length / len(all_questions)}")

top_n_percent = int(input("Enter the percent of smallest questions to keep: "))

sorted_lengths = sorted(lengths)

index_cutoff = int(len(sorted_lengths) * (top_n_percent / 100))

new_lengths = sorted_lengths[:index_cutoff]
new_total_length = sum(new_lengths)

print(f"New total length (kept {top_n_percent}% smallest): {new_total_length}")
print(f"This is {new_total_length / total_length * 100}% of the original total length")