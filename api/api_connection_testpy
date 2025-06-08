import requests
import json
import html

CATEGORIES = {
    9: "General Knowledge",
    10: "Entertainment: Books",
    11: "Entertainment: Film",
    12: "Entertainment: Music",
    13: "Entertainment: Musicals & Theatres",
    14: "Entertainment: Television",
    15: "Entertainment: Video Games",
    16: "Entertainment: Board Games",
    17: "Science & Nature",
    18: "Science: Computers",
    19: "Science: Mathematics",
    20: "Mythology",
    21: "Sports",
    22: "Geography",
    23: "History",
    24: "Politics",
    25: "Art",
    26: "Celebrities",
    27: "Animals",
    28: "Vehicles",
    29: "Entertainment: Comics",
    30: "Science: Gadgets",
    31: "Entertainment: Japanese Anime & Manga",
    32: "Entertainment: Cartoon & Animations"
}

DIFFICULTIES = ['easy', 'medium', 'hard']

def display_categories(): # Εμφάνιση κατηγοριών
    for cat_id, cat_name in CATEGORIES.items():
        print(f"{cat_id}: {cat_name}")

def get_user_choice(): # Λήψη επιλογών από τον χρήστη, για την κατηγορία και την δυσκολία
    display_categories()
    category = int(input("\nΔώσε τον αριθμό της κατηγορίας που επιθυμείς: "))
    while category not in CATEGORIES:
        category = int(input("Μη έγκυρη κατηγορία. Προσπάθησε ξανά: "))

    difficulty = input("\nΕπίλεξε επίπεδο δυσκολίας (easy, medium, hard): ").lower()
    while difficulty not in DIFFICULTIES:
        difficulty = input("Μη έγκυρη δυσκολία. Προσπάθησε ξανά (easy, medium, hard): ").lower()

    return category, difficulty

def fetch_questions(category, difficulty, num_questions=10): # Λήψη ερωτήσεων από το API
    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)

    if response.status_code == 200: # Έλεγχος εάν το αίτημα ήταν επιτυχές
        data = response.json()
        questions = data['results']

        for question in questions: # Αποκωδικοποίηση των ερωτήσεων για να είναι αναγνώσιμες
            question['question'] = html.unescape(question['question'])
            question['correct_answer'] = html.unescape(question['correct_answer'])
            question['incorrect_answers'] = [html.unescape(ans) for ans in question['incorrect_answers']]

        return questions
    else:
        return None

def save_questions_to_file(questions, filename="questions.json"): # Αποθήκευση ερωτήσεων σε αρχείο
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

def load_questions_from_file(filename="questions.json"): # Φόρτωση ερωτήσεων από αρχείο
    with open(filename, "r", encoding='utf-8') as file:
        questions = json.load(file)
    return questions


# Τεστάρισμα
if __name__ == "__main__":
    print("Καλώς ήρθες στο Trivia Game!")
    category, difficulty = get_user_choice()

    questions = fetch_questions(category, difficulty)

    if questions:
        save_questions_to_file(questions)

        loaded_questions = load_questions_from_file()

        for i, q in enumerate(loaded_questions, 1): # Εκτύπωση των ερωτήσεων για έλεγχο
            print(f"\nΕρώτηση {i}: {q['question']}")
            print(f"Σωστή απάντηση: {q['correct_answer']}")
            print(f"Λάθος απαντήσεις: {', '.join(q['incorrect_answers'])}")
