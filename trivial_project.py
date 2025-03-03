def players_profile(player):                                                                 #δημιουργία παίχτη(όνομα και επίπεδο δυσκολίας που θέλει να παίξει)
    player = {}
    while True:
        players_profile['name'] = input('Δώσε όνομα παίχτη')
        if 6<=len(players_profile['name']<=15 and players_profile['name'] not in player:    # το όνομα να είναι 6-15 χαρακτήρες και να μην υπάρχει ήδη στους παίχτες
                  break
        else:
            print('Λάθος καταχώρηση. Παρακαλώ επανάλαβε.')

    while True:
        players_profile[level]=int(input('Διάλεξε επίπεδο δυσκολίας (1,2,3):') 
            if not players_profile[level].isdigit():                                        #έλεγχος ότι το επίπεδο δυσκολίας δίνεται με αριθμό                               
                print('Το επίπεδο δυσκολίας πρέπει να είναι 1,2 ή 3')
            else:
                break

def display_menu():                                                                         #εμφάνιση κατηγοριών ερωτήσεων
    print("\n--- Επιλογή κατηγορίας ερωτήσεων---")
    print("1. General Knowledge")
    print("2. Geography")
    print("3. Art")
    print("4. Sports")
    print("5. Music")

    
category= {}                                                                                             
while True:                                                                                 #επιλογή κατηγορίας ερωτήσεων από τον παίχτη
    display_menu()
    choice = input("Επιλέξτε μια επιλογή (1-5): ")
    if choice == "1":
        category['general_knowledge']
    elif choice == "2":
        category['geography']
    elif choice == "3":
        category['art']
    elif choice == "4":
        category['sports']
    elif choice == "5":
        category['music']
    else:
        print("Μη έγκυρη επιλογή. Προσπαθήστε ξανά.")   
    
