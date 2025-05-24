import time
import json
import os


start_time=time.time()                           #αρχικοποίηση χρονόμετρου
answer_time= time.time()          #αρχικοποίηση καθολικής μεταβλητής χρόνου απάντησης
question_time = {}                     #λεξικό ερωτήσεων - χρόνου απάντησης
total_score = 0
start_question = {}
question_examined = {}



#Από λοιπά αρχεία μόλις είναι έτοιμα

#from data import show_leaderboard  #εισαγωγή απάντησης από το button Submit Answers  που είναι αποθηκευμένο στο data
#from gui import TrivialGameUI      #εισαγωγή κλάσης για να χρησιμοποιώ τον επιλεγμένο χρόνο 


#ενδεικτικό λεξικό για στοιχεια παίχτη και ερωτήσεων
#κανονικά θα ληφθούν από το αρχείο data
player = {
    "name": self.name_entry.get(), #ονομα παίχτη
    "difficulty": self.difficulty_var.get(), #επίπεδο δυσκολίας
    "category": self.category_var.get(), #κατηγορία ερωτήσεων
    "set_of_questions": self.questions_var.get(), #αριθμος ερωτησεων του σετ
    "selected_time" : self.time_var.get(), # η επιλογή χρόνου από το Menu
    "answers": [        #εμφανιση απαντησεων
        {
            "question_num" :self.answer_var.get(),  #αριθμος ερώτησης από api
            "presented_question" : self.answer_var.get(), #η εμφανιζόμενη ερώτηση
            "selected_answer" :self.answer_var.get(), #η απάντηση του παιχτη
            "correct" : self.answer_var.get(),  #αν η απάντηση του παίχτη είναι σωστή (True/False)
            "AT_i" : get.spent_time() #ο χρόνος μέσα στην ερώτηση
            }
        ]
    }

selection = {
    "submit" : self.submit_btn,
    "first" : self.first_btn,
    "previous" : self.previous_btn,
    "next_question" : self.next_btn
    }

    #"question_num" : number_of_presented_question.get() #αριθμός ερώτησης όπως εμφανίζεται στην οθόνη




def question_timer(question_num):  #χρονόμετρο για κάθε απάντηση
    if question_num not in start_question:
        start_question[question_num] = time.time()                 #εκκίνηση χρόνου απάντησης
    
    if selection["submit"] or selectio["first"] or selection["previous"] or selection["next_question"] is True:   #αν απαντηθεί ή βγει από τη ερώτηση
        end_question = time.time()                     #σταμάτημα χρόνου απάντησης
        duration = end_question - start_question[question_num]      #χρονος απαντησης
        question_time[question_num] = duration #αποθήκευση χρόνου απάντησης
        return duration
    
    return None

def update_answer(player,question_num,new_answer):  #αλλαγή απάντησης από παίχτη
    for answer in player["answers"]:
        if answer["question_num"] == question_num:
            answer["selected_answer"] = new_answer
            start_question[question_num] = time.time()
            break
        question_timer()      #update χρονου απάντησης


def timer():                            #συνολικό χρονόμετρο
    
    
    global answer_time                 #ενημέρωση της καθολικής μεταβλητής με το χρόνο κάθε απάντησης
    answer_time = time.time()-start_time[question_num]     #υπολογισμός χρόνου απαντήσεων σε σχέση 
                                             #με την αρχη προκειμένου να εμφανίζει
                                            #μήνυμα στον παίχτη

    if answer_time < selected_time :                #αν δεν έχει τελειώσει ο χρόνος
        time_left = player["selected_time"]-answer_time # υπολοιπόμενος χρόνος
        print(f"Time left{time_left:.0f} seconds.")
        return True, time_left                     #το παιχνίδι συνεχίζεται
    else:
        submit_answers_automatically()
        print ('End of game,no more time left.')           #μήνυμα για τερματισμό παιχνιδιού
        print("Your total score is:", total_score) #ανακοίνωση συνολικής βαθμολογίας
        return False, 0                    #το παιχνίδι τελείωσε



def submit_answers_automatically():
    unanswered = 0 # αρχικοποίηση αναπάντητων ερωτήσεων
    for item in range( player["set_of_questions"]): # για κάθε ερώτηση του κάθε σετ ερωτήσεων
        if player["answers"]["selected_answer"] is None or player["answers"]["selected_answer"] == " ": # η απάντηση δεν απαντήθηκε
            unanswered +=1

    save_unanswered(unanswered) #αποθήκευση των αναπάντητων ερωτήσεων
    
    if not subsequent_unanswered(): # έλεγχος ότι δεν ξεπερνά τις αναπάντητες ερωτήσεις 
        return False  #τερματισμος παιχνιδιού

    return True

def answer_score():
    total_vathmos = 0
    for answer in player["answers"]:  #να δ ι ο ρ θ ω θ ε ί ως προς την εντολή για τις σωστές απαντήσεις
        is_correct = player["answers"]["correct"]
        
        C_i = 1 if is_correct else 0

        if player["difficulty"] == "easy":
            D_i = 1
        elif player["difficulty"] == "medium":
            D_i = 2
        elif player["difficulty"] == "hard":
            D_i = 3

        AT_i = question_time.get(answer["question_num"],1)

        total_vathmos += C_i * D_i * AT_i
        
    return total_vathmos



 
total_score += answer_score()

with open ("score.json", "w") as f:
    json.dump({"score":total_score}, f)
##    with open("high_scores.json","w") as f:
##        json.dump({"high_scores":highscore},f)
##    

# Υποθέτουμε ότι οι αναπάντητες ερωτήσεις είναι μέσα στο φάκελος data που είναι στον ίδιο φάκελο με το timer.py
 
json_path = os.path.join("data", "anapantites.json")

def load_anapantites():
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def subsequent_unanswered(): # έλεγχος αναπάντητων ερωτήσεων σε δύο διαδοχικά σετ
    
    unanswered = load_anapantites()

    if len(unanswered)<2: #έλεγχος για ύπαρξη 2 ζευγάρια σετ ερωτήσεων
        return True
    
    for i in range (len(unanswered)-1): #εξέτασε δύο διαδοχικών σετ απαντήσεων
        if isinstance(unanswered[i], list) and isinstance(unanswered[i+1], list):
            counter1 = len(unanswered[i]) #σύνολο αναπαντητων ερωτήσεων στο αρχείο ι
            counter2 = len(unanswered[i+1]) # συνολο αναπάντητων ερωτήσεων στο επόμενο αρχείο από το ι
            if counter1 >3 and counter2 >3:          #έλεγχος αν σε δύο διαδοχικά σετ έχουμε πάνω από 3 αναπαντητες ερωτήσεις
                print("Unfortunately you lost as you left 3 questions without answering")
                print("Your total score is:", total_score)
            return False                           #το παιχνίδι σταματάει αν ξεπεράσει τις 3 αναπάντητες
    
    return True #επιστροφή αν το παιχνίδι συνεχίζεται
