import time
import json
import os




class TrivialTimerGame:
    DATA_FOLDER = "timer_data"

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
        self.question_start_times = {}
        self.question_accumulated_times = {}
        self.question_last_answers = {}
        self.question_pause_times = {}

        
        self.player = {
            "name": "",
            "difficulty": "",
            "category": "",
            "set_of_questions":0,
            "selected_time": 0,
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
            return True

        if not self.selection["submit"]: # δεν έχει γινεi υποβολή της απάντησης
            can_continue=self.submit_answers_automatically()
            return can_continue
        else: # ο χρόνος τελείωσε
            return True

    def handle_time_end(self): #αντιμετώπιση τέλος χρόνου
        if not self.selection["submit"]: #αν δεν έχει υποβάλλει απάντηση
            return self.submit_answers_automatically() #αυτόματη υποβολή απαντήσεων
        return True

    def handle_manual_submit(self): # έχει υποβάλλει απάντηση
        self.selection["submit"] = True
        unanswered = self.save_unanswered()
        return self.subsequent_unanswered()

    def start_new_game(self, num_questions, time_limit, difficulty, player_name): #Εκκίνηση νέου παιχνιδιού 
        self.player["name"] = player_name
        self.player["difficulty"] = difficulty
        self.player["set_of_questions"] = num_questions
        self.player["selected_time"] = time_limit
        self.player["answers"] = []
        
        for i in range(num_questions):
            self.player["answers"].append({
                "question_num": i,
                "selected_answer": None,
                "correct": False,
                "response_time": 0
            })
        
        self.selection["submit"] = False
        self.current_question = 0
        self.question_starts = {}
        self.question_time = {}

        
        self.reset_all_timers()

    def switch_to_question(self, question_num): #Αλλαγή στην ερώτηση 
        current_time = time.time()
        if hasattr(self,'current_question') and self.current_question != question_num:
                self._pause_current_question(current_time)
                if 0 <= question_num < len(self.player["answers"]):
                    self.current_question = question_num
                    self._resume_question(question_num, current_time)
            

    def select_answer(self, question_num, answer, is_correct): #Επιλογή απάντησης 
        if 0 <= question_num < len(self.player["answers"]):
            current_time = time.time()
            previous_answer = self.player["answers"][question_num].get("selected_answer")
            
            if previous_answer and previous_answer != answer: #Αν άλλαξε η απάντηση, μηδενισμός χρόνου
                self._reset_question_time(question_num, current_time)
                            
            self.player["answers"][question_num].update({ # update απάντησης
                "selected_answer": answer,
                "correct": is_correct,
                "response_time": time.time()
            })

            self.question_last_answers[question_num] = answer



    def get_question_time(self, question_num, new_answer=None): #χρονόμετρο ερώτησης
        current_time = time.time()
        total_time = 0
        
        if question_num in self.question_accumulated_times:
            total_time += self.question_accumulated_times[question_num]

        if (question_num == self.current_question and question_num in self.question_start_times):
            session_time = current_time - self.question_start_times[question_num]
            total_time += session_time
            
        return total_time

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
        else: # αν η απάντηση μένει η ίδια, το χρονόμετρο συνεχίζει από την προηγούμενη έξοδο
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
        except Exception as e:
            print(f"Error loading score: {e}")
            return 0

    def save_total_score_to_file(self, score): # αποθήκευση βαθμολογίας
        try:
            with open(self.score_path, "w") as f:
                json.dump({
                    "total_score": score,
                    "player": self.player["name"],
                    "difficulty": self.player["difficulty"]
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving score: {e}")

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
        except Exception as e:
            print(f"Error loading high scores: {e}")
            return {}

    def save_high_scores(self, high_scores_dictionary): #αποθήκευση υψηλότερν βαθμολογιών 
        try:
            with open(self.highscore_path, "w") as f:
                json.dump(high_scores_dictionary, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")

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

    def submit_answers(self):#Υποβολή απαντήσεων 
        self.selection["submit"] = True

        if hasattr(self, 'current_question') and self.current_question is not None:
            self._pause_current_question(time.time())
            
        final_score = self.calculate_final_score() # Υπολογισμός βαθμολογίας
        self.check_and_save_high_score(final_score) # Αποθήκευση high score

        return final_score


    def _pause_current_question(self, current_time):
        current_q = self.current_question
        session_time = 0  # Αρχικοποίηση
    
        if current_q in self.question_start_times:
            session_time = current_time - self.question_start_times[current_q]
        
        if current_q in self.question_accumulated_times:
            self.question_accumulated_times[current_q] += session_time
        else:
            self.question_accumulated_times[current_q] = session_time
    
        self.question_pause_times[current_q] = current_time

    
    def _resume_question(self, question_num, current_time):
        if question_num not in self.question_accumulated_times:
            self.question_accumulated_times[question_num] = 0

        self.question_start_times[question_num] = current_time

    def _reset_question_time(self, question_num, current_time):
        self.question_accumulated_times[question_num] = 0
        self.question_start_times[question_num] = current_time

        if question_num in self.question_pause_times:
            del self.question_pause_times[question_num]

    def get_question_time_detailed(self, question_num):
        current_time = time.time()

        accumulated = self.question_accumulated_times.get(question_num, 0)

        current_session = 0

        if (question_num == self.current_question and question_num in self.question_start_times):
            current_session = current_time - self.question_start_times[questio_-num]

        total_time = accumulated + current_session

        return {
            "accumulated_time" : accumulated,
            "current_session_time" : current_session,
            "total_time" : total_time,
            "is_active" : self.player["answers"][question_num].get("selected_answer") is not None
            }

    def get_all_questions_time_summary(self):
        summary = {}
        for i in range(len(self.player["answers"])):
            summary[f"question_{i+1}"] = self.get_question_time_detailed(i)
        return summary

    def reset_all_timers(self):
        self.question_start_times = {}
        self.question_accumulated_times = {}
        self.question_last_answers = {}
        self.question_pause_times = {}
        self.current_question = 0

    def get_current_question_time_live(self):
        if hasattr (self,'current_question') and self.current_question is not None:
            return self.get_question_time(self.current_question)
        return 0

    def format_time(self,seconds):
        if seconds < 60:
            return f"{seconds:.1f}s"
        else:
            mins = int(seconds//60)
            secs = seconds % 60
            return f"{mins}m {secs:.1f}s"

    def get_question_status_summary(self):
        summary = []
        for i in range(len(self.player["answers"])):
            answer = self.player["answers"][i]
            time_spent = self.get_question_time(i)

            status = {
                "question_num" : i+1,
                "answered" : answer.get("selected_answer") is not None,
                "selected_answer" : answer.get("selected_answer", ""),
                "is_correct" : answer.get("correct", False),
                "time_spent" : time_spent,
                "time_formatted" : self.format_time(time_spent),
                "is_current" : i == self.current_question
                }
            summary.append(status)

        return summary


    def cleanup(self): # Παύση του χρονομέτρου
        self.selection["submit"] = True # εφόσον ο παιχτης υποβάλει την ερώτηση
        for question_num in self.question_starts.keys():
            if question_num in self.question_starts:
                current_time = time.time()
                if question_num in self.question_time:
                    self.question_time[question_num] += current_time - self.question_starts[question_num]
                else:
                    self.question_time[question_num] = current_time - self.question_starts[question_num]
        
