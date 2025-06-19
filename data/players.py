import json
import os

PLAYERS_FILE = "data/players.json"

def load_players():  #Φόρτωση παικτών από αρχείο
    if not os.path.exists(PLAYERS_FILE): #Δημιουργία άδειου αρχείου .json
        save_players({})
        return {}
    with open(PLAYERS_FILE, 'r', encoding='utf-8') as file: #Ανοίγω το αρχείο σε λειτουργία ανάγνωσης
        return json.load(file) #Επιστρέφει τους παίκτες ως λεξικό

def save_players(players):  # Αποθήκευση παικτών σε αρχείο
    with open(PLAYERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(players, file, ensure_ascii=False, indent=2)
    return True

def create_player(username):  # Δημιουργία νέου παίκτη
    if not username or len(username) < 2: #Έλεγχος αν το όνομα χρήστη είναι κενό ή μικρότερο από 2 χαρακτήρες
        return False
    if len(username) > 20: #Έλεγχος αν το όνομα χρήστη είναι μεγαλύτερο από 20 χαρακτήρες
        return False
    if player_exists(username): #Έλεγχος αν υπάρχει ήδη ο παίκτης
        return False
    players = load_players() #Φόρτωση των υπαρχόντων παικτών
    next_number = len(players) + 1 #Εύρεση του επόμενου αριθμού παίκτη
    player_number = f"player{next_number}" #Δημιουργεί καινούργιο αριθμό παίκτη
    players[player_number] = {
        "username": username #Το όνομα χρήστη του παίκτη
    }
    save_players(players)  #Αποθήκευση των παικτών στο αρχείο
    return True

def player_exists(username):  # Έλεγχος αν υπάρχει ήδη ο παίκτης
    players = load_players() #Φόρτωση των υπαρχόντων παικτών
    for player_data in players.values(): #Εάν υπάρχει ο παίκτης στο λεξικό
        if player_data["username"] == username: #Έλεγχος αν το όνομα χρήστη ταιριάζει
            return True
    return False

def get_players_for_gui():  # Λήψη παικτών για το GUI
    players = load_players() #Φόρτωση των υπαρχόντων παικτών
    if not players: # Εάν δεν υπάρχουν παίκτες

        return [] #Επιστρέφει άδειο

    return sorted(player["username"] for player in players.values()) # Επιστρέφει τα ονόματα των παικτών σε αλφαβητική λίστα
