from sentence_transformers import SentenceTransformer
import json
import torch
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

correct_keyphrases = ["""Choice B is the best answer because it most logically completes the text&rsquo;s discussion of Booker T. Whatley.""",
                      "Choice B is the best answer because it most logically completes the text&rsquo;s discussion of bronze- and brass-casting techniques used by the Igun Eronmwon guild. In this context &ldquo;adhere to&rdquo; would mean to act in accordance with. The text states that although members of the Igun Eronmwon guild typically do something with techniques that have been passed down since the thirteenth century, they &ldquo;don&rsquo;t strictly observe every tradition.&rdquo; By establishing a contrast with not always following traditions, the context suggests that guild members do typically adhere to traditional techniques. </p><p>Choice A is incorrect because in this context &ldquo;experiment with&rdquo; would mean to do something new with. Although using motors rather than manual bellows is presented as a new approach, the text establishes a contrast between what the guild members typically do with techniques that have been passed down over centuries and the idea that the members &ldquo;don&rsquo;t strictly observe every tradition.&rdquo; The phrase &ldquo;experiment with&rdquo; wouldn&rsquo;t support the contrast because regularly trying new things with the techniques would be an example of not strictly following all traditions. Choice C is incorrect because in this context &ldquo;improve on&rdquo; would mean to make better. Although using motors rather than manual bellows might be an improved approach, the text establishes a contrast between what the guild members typically do with techniques that have been passed down over centuries and the idea that the members &ldquo;don&rsquo;t strictly observe every tradition.&rdquo; The phrase &ldquo;improve on&rdquo; wouldn&rsquo;t support the contrast because regularly making changes to the techniques would be an example of not strictly following all traditions. Choice D is incorrect because in this context &ldquo;grapple with&rdquo; would mean to try hard to solve a difficult problem. Although bronze- and brass-casting are likely challenging tasks, nothing in the text suggests that the guild members have any particular difficulties with the techniques passed down since the thirteenth",
                      "completes the text&rsquo;s discussion of Yu&rsquo;s novel",
                      "logically completes the text&rsquo;s discussion of single-celled organism behavior. As used in this context, &ldquo;rudimentary&rdquo; means basic or unsophisticated. According to the text, a study of the single-celled protozoan <em>Stentor roeseli</em> showed that the organisms can switch strategies for escaping certain stimuli, &ldquo;sophisticatedly &lsquo;changing their minds&rsquo;&rdquo; and using new strategies should other strategies fail. This context suggests that single-celled organisms may not be limited to behaviors that are basic or rudimentary, since the study showed that single-celled protozoans can respond complexly to irritating stimuli. </p><p>Choice A is incorrect because the text doesn&rsquo;t suggest that single-celled organisms may not be limited to behavior that is &ldquo;aggressive,&rdquo; or threatening. Rather, the text suggests that single-celled organisms may not be limited to behaviors that are basic, since the study of <em>Stentor roeseli</em> showed that single-celled protozoans can respond complexly to irritating stimuli. Choice C is incorrect because the text doesn&rsquo;t suggest that single-celled organisms may not be limited to behavior that is &ldquo;evolving,&rdquo; or advancing. Rather, the text suggests that single-celled organisms may not be limited to behaviors that are basic, since the study of <em>Stentor roeseli</em> showed that single-celled protozoans can respond complexly to irritating stimuli. Choice D is incorrect because the text doesn&rsquo;t suggest that single-celled organisms may not be limited to behavior that is &ldquo;advantageous,&rdquo; or helpful. Rather, the text suggests that single-celled organisms may not be limited to behaviors that are basic, since the study of <em>Stentor roeseli</em> showed that single-celled protozoans can respond complexly to irritating",
                      "FABRY: One Robot can replace two and a half",
                      "Mars would not provide enough resistance to the rotating blades of a standard",
                      "jalis have traditionally been keepers of information about family histories and records of important events",
                      "e graph to effectively complete the example of Eludoyin and his coll",
                      "Herbivorous sauropod dinosaurs could grow more than 100 feet long and weigh up",
                      "Known for her massive photorealistic paintings of African American",
                      "2010, archaeologist Noel Hidalgo Tan was",
                      "Cheng Dang and her colleagues at the University of Washington",
                      "The Mission 66 initiative, which was approved by Congress",
                      "The Progressive Era in the United States witnessed the rise of numerous Black",
                      "Eli Eisenberg, a genetics expert at Tel Aviv University in Israel",
                      "Award-winning travel writer Linda Watanabe McFerrin considers",
                      "Bharati Mukherjee was",
                      "Pterosaurs were flying reptiles that existed millions of years ago",
                      "Seven species of sea turtle exist today",
                      "Emily Shepard and colleagues in the UK and Germany studied the effect",
                      "New and interesting research conducted by Suleiman A. Al-Sweedan and Moath",
                      "Researcher Haesung Jung led a 2020 study showing",
                      "a 1902 memoir by Ohiyesa (Charles",
                      "The following text is from Charlotte Bront",
                      "Musician Joni Mitchell, who is also a painter, uses images she",
                      "including finance professor Madhu Veeraraghavan",
                      "Most animals can regenerate some parts of their bodies",
                      "Mosasaurs were large marine reptiles that lived in the Late Cretaceous",
                      "Considering a large sample of companies, economics experts Maria Guadalupe",
                      "Given that stars and planets initially form from the same gas",
                      "While attending school in New York City in the 1980s",
                      "One challenge when researching whether holding elected office changes",
                      "Compiled in the late 1500s largely through the efforts of Indigenous",
                      "spacecraft when she made an interesting discovery: the tiny",
                      "Hegra is an archaeological site in present-day Saudi Arabia",
                      "The Babylonian king Hammurabi achieved much",
                      "When designing costumes for film, American artist Suttirat",
                      "Astronomers estimate that the number of comets orbiting the Sun is in"]

incorrect_keyphrases = ["idea or assumption with little evidence. The text explains that certain economic hi",
                        "Buck refused to notice them",
                        "that upon hearing Black folk songs, he felt an intuitive",
                        "authored several works herself, such as the novel",
                        "A model created by biologist Luis Valente predicts that the rate of speciation",
                        "Samuel Selvon was a Trinidadian author",
                        "Abdulrazak Gurnah was awarded the 2021 Nobel Prize in Literature",
                        "In studying the use of external stimuli to reduce the itching sensation",
                        "Whether the reign of a French monarch such as Hugh Capet or Henry",
                        "Some researchers studying Indigenous actors and filmmakers in the United",
                        "To humans, it does not appear that the golden orb-weaver",
                        "New York Harbor under the guidance of Captain",
                        "Bengali author Toru Dutt’s",
                        " 1937, Chinese American screen actor Anna May Wong",
                        "The Arctic-Alpine Botanic Garden in Norway",
                        "Rita Dove interweaves the titular"]

correct_questions = []
incorrect_questions = []


with open('all_questions_english.json', 'r') as f:
    all_questions = json.load(f)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

for question in all_questions:
    for keyphrase in correct_keyphrases:
        if keyphrase in str(question):
            correct_questions.append(embedding_model.encode(question['rationale']))
    for keyphrase in incorrect_keyphrases:
        if keyphrase in str(question):
            incorrect_questions.append(embedding_model.encode(question['rationale']))


if not correct_questions or not incorrect_questions:
    print("Not enough training data for both classes. Exiting.")
    exit()

# Use numpy arrays for scikit-learn
correct_embeddings = np.array(correct_questions)
incorrect_embeddings = np.array(incorrect_questions)

# Create labels. incorrect is 1, correct is 0.
correct_labels = np.zeros(correct_embeddings.shape[0])
incorrect_labels = np.ones(incorrect_embeddings.shape[0])


# Combine data
X = np.concatenate((incorrect_embeddings, correct_embeddings), axis=0)
y = np.concatenate((incorrect_labels, correct_labels), axis=0)

# Split data into training and testing sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=43, stratify=y
)

# Scale data for better performance with linear models
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Use Logistic Regression with strong regularization (low C) and balanced class weights
# This is much more robust against overfitting on small datasets.
model = LogisticRegression(class_weight='balanced', random_state=43, C=0.1, solver='liblinear')

print("Training model...")
model.fit(X_train_scaled, y_train)


# Evaluation
print("\nEvaluating model...")
# Evaluate on training set
train_predictions = model.predict(X_train_scaled)
train_accuracy = accuracy_score(y_train, train_predictions)
print(f'Train Accuracy: {train_accuracy*100:.2f}%')

# Evaluate on test set
test_predictions = model.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, test_predictions)
print(f'Test Accuracy: {test_accuracy*100:.2f}%')


# Evaluation on all questions
print("\nEvaluating model on all questions...")
wrong_count = 0
with torch.no_grad():
    all_embeddings = np.array([embedding_model.encode(q['rationale']) for q in all_questions])
    all_embeddings_scaled = scaler.transform(all_embeddings)
    all_predictions = model.predict(all_embeddings_scaled)
    wrong_count = int(all_predictions.sum())

print(f"\nThe model predicts you would get {wrong_count} questions wrong out of {len(all_questions)}.")




