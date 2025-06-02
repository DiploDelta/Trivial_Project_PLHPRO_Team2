import time
import json
import os


class TrivialTimerGame:
    DATA_FOLDER = "data"

    def __init__(self):
        self.score_path = os.path.join(self.DATA_FOLDER, "score.json")
        self.highscore_path = os.path.join(self.DATA_FOLDER, "high_scores.json")
        self.unanswered_path = os.path.join(self.DATA_FOLDER, "anapantites.json")

        self.total_score = 0
        self.question_starts = {}
        self.end_question = {}
        self.temporary_question = {}
        self.question_time = {}
        self.current_question = 0

        # Ενδεικτικά στοιχεία
        self.player = {
            "name": "playername",
            "difficulty": "easy",
            "category": "sports",
            "set_of_questions": 9,
            "selected_time": 180,
            "answers": []
        }

        self.selection = {
            "submit": False,
            "first": False,
            "previous": False,
            "next_question": False
        }

    def load_anapantites(self): #άνοιγμα αρχείου αναπάντητων
        try:
            with open(self.unanswered_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_unanswered(self): #αποθήκευση αναπάντητων ερωτήσεων του σετ
        try:
            with open(self.unanswered_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        unanswered = 0
        for answer in self.player["answers"]:
            if answer.get("selected_answer") is None or answer.get("selected_answer") == " ":
                unanswered += 1

        data.append(unanswered)
        with open(self.unanswered_path, "w") as f:
            json.dump(data, f)

        return unanswered

    def subsequent_unanswered(self): #έλεγχος αριθμού αναπάντητων σε δύο συνεχόμενα σετ
        unanswered_set = self.load_anapantites()
        if len(unanswered_set) < 2:
            return True
        if unanswered_set[-2] > 3 and unanswered_set[-1] > 3:
            print("Unfortunately you lost as you left more than 3 questions unanswered.")
            print("Your total score is:", self.total_score)
            return False
        return True

    def submit_answers_automatically(self): #υποβολή απαντήσεων αυτόματα στη λήξη του χρόνου
        return self.subsequent_unanswered()
    
    def start_countdown(self, time_left=None):# χρονόμετρο
        if time_left is None:
            time_left = self.player["selected_time"]

        mins, secs = divmod(time_left, 60)
    
        if hasattr(self, 'timer_label'): #έλεγχος για τη διασύνδεση με το GUI
           self.timer_label.config(text=f"{mins:02}:{secs:02}")
    
        if time_left > 0 and not self.selection["submit"]: #έχει μείνει χρόνος και δεν έχει υποβάλλει απάντηση
            if hasattr(self, 'root'):
                self.root.after(1000, self.start_countdown, time_left - 1)
            return
    
    
        if not self.selection["submit"]: # δεν έχει γινεi υποβολή της απάντησης
            print("Time is up!")
            if self.submit_answers_automatically(): #αν έχει μείνει χρόνος
                print("Continue playing")
                return True
            else: # ο χρόνος τελείωσε 
                print("Game Over")
                return False
        else: #ο παίχτης υποβάλλει την απάντηση
            print("Answers submitted in time.")
            return True

    def handle_time_end(self): #αντιμετώπιση τέλος χρόνου
        if not self.selection["submit"]: #αν δεν έχει υποβάλλει απάντηση
            return self.submit_answers_automatically() #αυτόματη υποβολή απαντήσεων
        return True

    def handle_manual_submit(self): # έχει υποβάλλει απάντηση
        self.selection["submit"] = True
        unanswered = self.save_unanswered()
        return self.subsequent_unanswered()


    def get_question_time(self, question_num, new_answer=None): #χρονόμετρο ερώτησης
        previous_answer = None
        for answer in self.player["answers"]:
            if answer.get("question_num") == question_num:
                previous_answer = answer.get("selected_answer")
                break

        if previous_answer is None:
            return self.first_appearance_time(question_num)
        else:
            return self.repeated_appearance_time(question_num, new_answer, previous_answer)

    def first_appearance_time(self, question_num): #αν η ερώτηση δεν έχει ξαναεμφανιστει, εκκίνηση χρόνου
        if question_num not in self.question_starts:
            self.question_starts[question_num] = time.time()
            self.question_time[question_num] = 0

        current_time = time.time()

        if self.selection["submit"]: #αν γίνει υποβολή απάντησησ
            self.end_question[question_num] = current_time
            duration = self.end_question[question_num] - self.question_starts[question_num]
            self.question_time[question_num] = duration
        elif self.selection["first"] or self.selection["previous"] or self.selection["next_question"]: #αν "βγει" από την ερώτηση
            self.temporary_question[question_num] = current_time
            pause_time = self.temporary_question[question_num] - self.question_starts[question_num]
            self.question_time[question_num] = pause_time

        return self.question_time.get(question_num, 0)

    def repeated_appearance_time(self, question_num, new_answer, previous_answer): #αν η ερώτηση έχει ξαναεμφανιστεί
        current_time = time.time()

        if new_answer != previous_answer: #αν αλλάζει η απάντηση το χρονόμετρο ξαναρχίζει
            self.question_starts[question_num] = time.time()
            self.question_time[question_num] = 0
        else: # αν η απάντηση μένει η ίφια, το χρονόμετρο συνεχίζει από την προηγούμενη έξοδο
            if question_num in self.question_starts:
                previous_time = self.question_time.get(question_num, 0)
                session_time = current_time - self.question_starts.get(question_num, 0)
                self.question_time[question_num] = previous_time + session_time

        return self.question_time.get(question_num, 0)

    def answer_score(self, question_num): #υπολογισμός βαθμολογίας ερώτησης
        for answer in self.player["answers"]:
            if answer.get("question_num") == question_num:
                C_i = 1 if answer.get("correct", False) else 0
                difficulty_map = {"easy": 1, "medium": 2, "hard": 3}
                D_i = difficulty_map.get(self.player["difficulty"], 1)
                duration = self.get_question_time(question_num)
                AT_i = duration * 100
                return C_i * D_i * AT_i
        return 0

    def score_of_set(self): #υπολογισμός βαθμολογίας κάθε σετ ερωτήσεων
        total = 0
        for answer in self.player["answers"]:
            if answer.get("question_num") is not None:
                score = self.answer_score(answer["question_num"])
                total += score
        return total

    def load_total_score(self): #εμφάνιση αρχείου βαθμολογιών
        try:
            with open(self.score_path, "r") as f:
                data = json.load(f)
                return data.get("total_score", 0)
        except FileNotFoundError:
            return 0

    def save_total_score_to_file(self, score): # αποθήκευση βαθμολογίας
        with open(self.score_path, "w") as f:
            json.dump({"total_score": score}, f)

    def calculate_final_score(self): # υπολογισμός συνολικής βαθμολογίας
        self.total_score = self.load_total_score()
        current_set_score = self.score_of_set()
        self.total_score += current_set_score
        self.save_total_score_to_file(self.total_score)
        return self.total_score

    def load_high_scores(self): #άνοιγμα αρχείου υψηλότερων βαθμολογιών
        try:
            with open(self.highscore_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_high_scores(self, high_scores_dictionary): #αποθήκευση υψηλότερν βαθμολογιών 
        with open(self.highscore_path, "w") as f:
            json.dump(high_scores_dictionary, f)

    def check_and_save_high_score(self, final_score): # έλεγχος κατάταξης βαθμολογιών
        high_scores = self.load_high_scores()
        player_name = self.player["name"]
        high_scores[player_name] = max(high_scores.get(player_name, 0), final_score)
        self.save_high_scores(high_scores)

        sorted_scores = sorted(high_scores.values(), reverse=True)
        if final_score in sorted_scores[:10]:
            print("Congratulations! New High Score 🎉")
            return True
        return False

    def display_high_scores(self): #εμφάνιση υψηλότερων βαθμολογιών
        high_scores = self.load_high_scores()
        sorted_scores = sorted(high_scores.items(), key=lambda x: x[1], reverse=True)
        top_10 = sorted_scores[:10]

        print("Top 10 High Scores:\n")
        for i, (name, score) in enumerate(top_10, 1):
            print(f"{i:2d}. {name:<20} {score:>10.2f}")

    