import requests
import json
import html

#Κατηγορίες που επιλέξαμε να μπουν στο παιχνίδι
CATEGORIES = {
    9: "General Knowledge",
    15: "Entertainment: Video Games",
    17: "Science & Nature",
    18: "Science: Computers",
    21: "Sports",
    22: "Geography",
    23: "History",
    25: "Art",
    27: "Animals"
}
#Επίπεδο δυσκολίας
DIFFICULTIES = ['easy', 'medium', 'hard']

#Εμφάνιση των διαθέσιμων κατηγοριών
def display_categories():
    for cat_id, cat_name in CATEGORIES.items():
        print(f"{cat_id}: {cat_name}") #Εκτυπώνει την κατηγορία και το ID της

#Ο χρήστης επιλέγει κατηγορία και επίπεδο δυσκολίας
def get_user_choice():
    #Εμφανίζει όλες τις διαθέσιμες κατηγορίες στην οθόνη
    display_categories()
    category = int(input("\nΔώσε τον αριθμό της κατηγορίας που επιθυμείς: "))
    while category not in CATEGORIES: #Ελέγχει αν η κατηγορία που έδωσε ο χρήστης είναι έγκυρη (δηλαδή αν υπάρχει στο λεξικό CATEGORIES)
        category = int(input("Μη έγκυρη κατηγορία. Προσπάθησε ξανά: ")) #Επαναλαμβάνει την ερώτηση αν η κατηγορία δεν είναι έγκυρη

    #Επιλογή επιπέδου δυσκολίας, μετατρέποντας σε πεζά γράμματα
    difficulty = input("\nΕπίλεξε επίπεδο δυσκολίας (easy, medium, hard): ").lower()
    while difficulty not in DIFFICULTIES: #Ελέγχει αν η δυσκολία που έδωσε ο χρήστης είναι έγκυρη, εάν όχι επαναλαμβάνει την ερώτηση
        difficulty = input("Μη έγκυρη δυσκολία. Προσπάθησε ξανά (easy, medium, hard): ").lower()

    # Επιστρέφει την τελική επιλογή κατηγορίας και δυσκολίας
    return category, difficulty

#Λήψη ερωτήσεων από το API του Open Trivia Database
def fetch_questions(category, difficulty, num_questions=10):
    #Δημιουργία URL για το API με τις παραμέτρους που έθεσε ο χρήστης πρίν
    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple"
    response = requests.get(url) #Στέλνει αίτημα στο API για να πάρει τις ερωτήσεις

    if response.status_code == 200: #Έλεγχος εάν ήταν επιτυχές η σύνδεση με το API
        data = response.json() #Μετατρέπει την απάντηση του API σε JSON
        questions = data['results']

        for question in questions: #Αποκωδικοποίηση των ερωτήσεων για να είναι αναγνώσιμες (πχ αντί για $quot; να εμφανίζεται " ")
            question['question'] = html.unescape(question['question'])
            question['correct_answer'] = html.unescape(question['correct_answer'])
            question['incorrect_answers'] = [html.unescape(ans) for ans in question['incorrect_answers']]

        #Επιστρέφει τις επεξεργασμένες ερωτήσεις
        return questions
    else:
        return None #Εάν η σύνδεση με το API απέτυχε, επιστρέφει None

# Αποθήκευση σωστών απαντήσεων σε JSON
def save_sostes_apantiseis(questions, filename="sostes_apantiseis.json"):
    #Δημιουργεί λεξικό με αριθμημένες ερωτήσεις και τις σωστές απαντήσεις
    data = {
        f"question {i+1}": {
            "question": q["question"],
            "correct_answer": q["correct_answer"]
        } for i, q in enumerate(questions)
    }
    #Ανοίγει το αρχείο σε λειτουργία εγγραφής και αποθηκεύει τα δεδομένα σε μορφή JSON με κωδικοποίηση UTF8
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        #ensure_ascii=False επιτρέπει την αποθήκευση χαρακτήρων Unicode όπως είναι, χωρίς δηλαδή να εμφανίζονται ως \u03a3\u03c9\
        #indent=4 το JSON θα έχει εσοχές 4 χαρακτήρων για καλύτερη αναγνωσιμότητα

# Αποθήκευση λάθως απαντήσεων σε JSON
def save_lathos_apantiseis(questions, filename="lathos_apantiseis.json"):
    #Δημιουργεί λεξικό με αριθμημένες ερωτήσεις και τις 3 λάθος απαντήσεις
    data = {
        f"question {i+1}": {
            "question": q["question"],
            "incorrect_answers": q["incorrect_answers"]
        } for i, q in enumerate(questions)
    }
    #Ανοίγει το αρχείο σε λειτουργία εγγραφής και αποθηκεύει τα δεδομένα σε μορφή JSON με κωδικοποίηση UTF8
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        #ensure_ascii=False επιτρέπει την αποθήκευση χαρακτήρων Unicode όπως είναι, χωρίς δηλαδή να εμφανίζονται ως \u03a3\u03c9\
        #indent=4 το JSON θα έχει εσοχές 4 χαρακτήρων για καλύτερη αναγνωσιμότητα

# Τεστάρισμα
if __name__ == "__main__":
    print("Καλώς ήρθες στο Trivia Game!")
    category, difficulty = get_user_choice()

    questions = fetch_questions(category, difficulty)

    if questions:
        save_sostes_apantiseis(questions)
        save_lathos_apantiseis(questions)

        for i, q in enumerate(questions, 1):
            print(f"\nΕρώτηση {i}: {q['question']}")
            print(f"Σωστή απάντηση: {q['correct_answer']}")
            print(f"Λάθος απαντήσεις: {', '.join(q['incorrect_answers'])}")
