# Trivial_Project_PLHPRO_Team2

import tkinter as tk  "εισαγωγή γραφικών"
import requests  "σύνδεση με το API"
import json "για μετατροπή των Data που θα παίρνουμε από τον server Trivial"
import time "για το χρονόμετρο"

# θα πρέπει να προστεθεί το μήνυμα καλωσορίσματος

def display_erotiseis():                                                                            #συνάρτηση δημιουργίας μενού επιλογής ερωτήσεων
    print("\n--- Κατηγορίες ερωτήσεων---")
    print("1. Υπολογιστές")
    print("2. Γενικές Γνώσεις")
    print("3. Video Games")
    print("4. Μουσική")
    print("5. Ιστορία")
    print("6. Αθλητικά")
    print("7. Αυτοκίνητα")
    print("8. Τηλεόραση")
    print("9. Επιστήμες")
    print("10. Έξοδος")



players = []                                 # Λίστα για την αποθήκευση των παικτών

def add_playerinfo(player):                                                                          #συνάρτηση δημιουργίας παίχτη
    player={}                                                                                        #λεξικό για στοιχεια παίχτη  #πιθανά να θέλει άλλο τύπο αρχείου
    while True:
        player['name'] = input('Ποιό είναι το ονομά σου;: ')                                         # ο χρήστης εισάγει το όνομα με το οποίο θα παιζει      
        if player['name']  in players:                                                                # έλεγχος αν υπάρχει ήδη παίχτης  με το ίδιο όνομα
               print ('Παρακαλώ διάλεξε ένα άλλο όνομα. Ο παίχτης', player['name'] ,' υπάρχει ήδη.') #μήνυμα λάθους                                                                                    #αν είναι στη σωστή μορφή το πρόγραμμα προχωράει στο επόμενο στοιχειο
        else:
            break

##    while True:
##        player['avatar']= input('θέλεις να προσθέσεις avatar;\n Πάτησε y/n αν θέλεις να προσθέσεις avatar').strip().lower() #ότι πληκτολογηθεί μετατρέπεται σε μικρό γράμμα χωρίς κενά
##        if player['avatar'] == 'n':                                                                   # αν δεν διαλέξει avatar 
##            exit()
        

 ##πως επιλεγει avatar?

    while True:
        player['antipaloi']=input('Θα παίξεις μόνος σου ή θα έχεις αντίπαλο;Πάτησε 1 για μόνος σου ή 2 για αντίπαλο:')       #επιλέγει αν θα παίξει μόνος ή με αντίπαλο
        if player['antipaloi'].isdigit() and 1<=int(player['antipaloi'])<=2:                                       #έλεγχος αν εισάγεται αριθμός και αριθμός παιχτών
            break
        else:
            print('Δώσε αριθμό παιχτών(1 ή 2)')

    while True:                                                                                             #επιλογή βαθμού δυσκολίας ερωτήσεων
        player['difficulty']= input('Διάλεξε επίπεδο δυσκολίας (1=εύκολο,2= μέτριο,3=δύσκολο):') 
        if player['difficulty'].isdigit() and 1<=int(player['difficulty'])<=3:
            break
        else:
            print('Λάθος επιλογή. Παρακαλώ διάλεξε επίπεδο δυσκολίας (1=εύκολο,2= μέτριο,3=δύσκολο):')


    while True:
        display_erotiseis()
        player['category'] = int(input('Διάλεξε κατηγορία ερωτήσεων(1-10): '))
##                                       if player['category'] == "1":
##                                       null #επιλογή κατηγορίας ερωτήσεων
                                       
                                   

comp_easy = "https://opentdb.com/api.php?amount=9&category=18&difficulty=easy"
comp_medium ="https://opentdb.com/api.php?amount=9&category=18&difficulty=medium"
comp_hard = "https://opentdb.com/api.php?amount=9&category=18&difficulty=hard"
general_easy = "https://opentdb.com/api.php?amount=9&category=9&difficulty=easy"
general_medium = "https://opentdb.com/api.php?amount=9&category=9&difficulty=medium"
general_hard = "https://opentdb.com/api.php?amount=9&category=9&difficulty=hard"
video_easy = "https://opentdb.com/api.php?amount=9&category=15&difficulty=easy"
video_medium = "https://opentdb.com/api.php?amount=9&category=15&difficulty=medium"
video_hard = "https://opentdb.com/api.php?amount=9&category=15&difficulty=hard"
music_easy = "https://opentdb.com/api.php?amount=9&category=12&difficulty=easy"
music_medium = "https://opentdb.com/api.php?amount=9&category=12&difficulty=medium"
music_hard = "https://opentdb.com/api.php?amount=9&category=12&difficulty=hard"
history_easy = "https://opentdb.com/api.php?amount=9&category=23&difficulty=easy"
history_medium = "https://opentdb.com/api.php?amount=9&category=23&difficulty=medium"
history_hard = "https://opentdb.com/api.php?amount=9&category=23&difficulty=hard"
sports_easy = "https://opentdb.com/api.php?amount=9&category=21&difficulty=easy"
sports_medium = "https://opentdb.com/api.php?amount=9&category=21&difficulty=medium"
sports_hard = "https://opentdb.com/api.php?amount=9&category=21&difficulty=hard"
vehicles_easy = "https://opentdb.com/api.php?amount=9&category=28&difficulty=easy"
vehicles_medium = "https://opentdb.com/api.php?amount=9&category=28&difficulty=medium"
vehicles_hard = "https://opentdb.com/api.php?amount=9&category=28&difficulty=hard"
tv_easy = "https://opentdb.com/api.php?amount=9&category=14&difficulty=easy"
tv_medium = "https://opentdb.com/api.php?amount=9&category=14&difficulty=medium"
tv_hard = "https://opentdb.com/api.php?amount=9&category=14&difficulty=hard"
science_easy = "https://opentdb.com/api.php?amount=9&category=17&difficulty=easy"
science_medium = "https://opentdb.com/api.php?amount=9&category=17&difficulty=medium"
science_hard = "https://opentdb.com/api.php?amount=9&category=17&difficulty=hard"


 

#    player[player_score]=object                                                                         #καταχώρηση σκορ παίχτη

