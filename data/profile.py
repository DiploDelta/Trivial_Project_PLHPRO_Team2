import json
import os

class PlayerAccount:
    def __init__(self):
        self.player_data_file = "player_accounts.json"
        self.max_players = 4
        self.avatars = []              #εδώ θα μπει η λίστα με τα αβαταρς
        self.players = self._load_player_data()

    def _load_player_data(self):

        if os.path.exists(self.player_data_file):
            with open(self.player_data_file, 'r') as f:
                return json.load(f)
        return {"παίκτες": {}}

    def _save_player_data(self):

        with open(self.player_data_file, 'w') as f:
            json.dump(self.players, f, indent=4)

    def create_player_account(self):

        if len(self.players["παίκτες"]) >= self.max_players:
            print(f"Το μέγιστο όριο με {self.max_players} players reached!")
            return None

        print("\nAvailable avatars:")
        for i, avatar in enumerate(self.avatars, 1):
            print(f"{i}. {avatar}")

        while True:
            try:
                avatar_choice = int(input("Διάλεξε το avatar σου (πληκτρολογήστε τον αριθμό της επιλογής σας): "))
                if 1 <= avatar_choice <= len(self.avatars):
                    selected_avatar = self.avatars[avatar_choice - 1]
                    break
                else:
                    print("Σφάλμα κατά την επιλογή. Παρακαλώ διαλέξτε έναν έγκυρο αριθμό.")
            except ValueError:
                print("Παρακαλώ διαλέξτε αριθμό.")

        while True:
            player_name = input("Πες μας το όνομα σου: ").strip()
            if not player_name:
                print("Το όνομα του παίκτη δεν μπορεί να είναι κενό")
            elif player_name in self.players["παίκτες"]:
                print("Το όνομα υπάρχει ήδη!")
            else:
                break

        self.players["παίκτες"][player_name] = {
            "avatar": selected_avatar,
            "score": 0,
        }
        self._save_player_data()
        print(f"Δημιουργήθηκε λογαριασμός για τ@ {player_name} με το avatar {selected_avatar}!")
        return player_name

    def get_player_info(self, player_name):

        return self.players["παίκτες"].get(player_name)

    def update_player_score(self, player_name, points):

        if player_name in self.players["παίκτες"]:
            self.players["παίκτες"][player_name]["score"] += points
            self._save_player_data()



    def show_all_players(self):

        print("\nRegistered Players:")
        for i, (name, data) in enumerate(self.players["παίκτες"].items(), 1):
            print(f"{i}. {data['avatar']} {name}: Score {data['score']} ")
