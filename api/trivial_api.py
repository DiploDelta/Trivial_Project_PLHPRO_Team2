import requests
import json
import html
import os
import random

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

# Λήψη ερωτήσεων από το API του Open Trivia Database
def fetch_questions(category, difficulty, num_questions):
    #Δημιουργία URL για το API με τις παραμέτρους που επιλέγει ο χρήστης από το GUI
    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type=multiple"

    response = requests.get(url, timeout=10) #Αίτημα προς το API με όριο χρόνου

    if response.status_code == 200: #Έλεγχος εάν ήταν επιτυχής η σύνδεση με το API
        data = response.json() #Μετατρέπει την απάντηση του API σε JSON

        if data.get('response_code') == 0:
            questions = data['results']

            for question in questions:  #Αποκωδικοποίηση των ερωτήσεων για να είναι αναγνώσιμες (πχ αντί για $quot; να εμφανίζεται " ")
                question['question'] = html.unescape(question['question'])
                question['correct_answer'] = html.unescape(question['correct_answer'])
                question['incorrect_answers'] = [html.unescape(ans) for ans in question['incorrect_answers']]

            return questions #Επιστρέφει τις επεξεργασμένες ερωτήσεις

    return None #Εάν η σύνδεση με το API απέτυχε, επιστρέφει None

#Αποθήκευση σωστών απαντήσεων σε JSON
def save_sostes_apantiseis(questions, filename="sostes_apantiseis.json"):
    #Δημιουργεί λεξικό με αριθμημένες ερωτήσεις και τις σωστές απαντήσεις
    data = {
        f"question {i + 1}": {
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
        f"question {i + 1}": {
            "question": q["question"],
            "incorrect_answers": q["incorrect_answers"]
        } for i, q in enumerate(questions)
    }
    #Ανοίγει το αρχείο σε λειτουργία εγγραφής και αποθηκεύει τα δεδομένα σε μορφή JSON με κωδικοποίηση UTF8
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        #ensure_ascii=False επιτρέπει την αποθήκευση χαρακτήρων Unicode όπως είναι, χωρίς δηλαδή να εμφανίζονται ως \u03a3\u03c9\
        #indent=4 το JSON θα έχει εσοχές 4 χαρακτήρων για καλύτερη αναγνωσιμότητα

def clean_category_name(
        category_name):  #Για την εμφάνιση στο GUI καθαρίζω τις κατηγορίες (χωρίς Entertainment, Science κλπ)
    return (category_name
            .replace("Entertainment: ", "")  #Αντικαθιστώ το "Entertainment" με κενό
            .replace("Science & Nature", "Science")  #Αντικαθιστώ το "Science & Nature" με "Science"
            .replace("Science: ", ""))  #Αντικαθιστώ το "Science" με κενό

def get_questions_from_gui(difficulty_var, category_var, questions_var):  #Παίρνει τις τιμές από το GUI
    difficulty = difficulty_var.get()
    category_name = category_var.get()
    num_questions = int(questions_var.get())

    #Βρίσκει το category_id από το όνομα
    category_id = None  # Αρχικοποιώ το ID
    for cat_id, cat_name in CATEGORIES.items():
        if clean_category_name(cat_name) == category_name:  # Αν το όνομα απο την λίστα ταιριάζει με το dropdown
            category_id = cat_id  # Βρίσκει το σωστό ID
            break

    if category_id is None:  #Εάν για κάποιο λόγο δεν ταιριάξει η κατηγορία απο το dropdown
        category_id = 9  #Πάμε αυτόματα στην General Knowledge

    #Καλεί την κανονική συνάρτηση
    questions = fetch_questions(category_id, difficulty, num_questions)

    return questions

def get_categories_for_gui():  #Οι κατηγορίες που θα εμφανίζονται στο GUI
    return [clean_category_name(category_name) for category_name in CATEGORIES.values()]

def mix_answers(question):  #Ανακατεύει τις απαντήσεις και τις επιστρέφει στο GUI
    all_answers = [question['correct_answer']] + question['incorrect_answers']
    random.shuffle(all_answers)
    return all_answers