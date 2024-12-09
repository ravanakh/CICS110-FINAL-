
class MainMenuScreen:
    def display(self):
        print("Welcome to the Dungeon Adventure!")
        print("==============================")
        print("1. Play Game")
        print("2. Instructions")
        print("3. Quit")
        print("==============================")

    def get_choice(self):
        choice = None
        while choice not in ["1", "2", "3"]:
            choice = input("Please select an option (1, 2, or 3): ")
            if choice not in ["1", "2", "3"]:
                print("Invalid choice. Please choose 1, 2, or 3.")
        return choice

    def instructions(self):
        print("\nInstructions:")
        print("1. Progress through 16 rooms filled with enemies and rewards.")
        print("2. Each room will have turn-based battles where you can attack, evade, or use an item.")
        print("3. Defeat enemies to earn buffs and open chests for better weapons.")
        print("4. Every 4th room has a mini-boss, and the final room has the ultimate boss!")
        print("5. Plan your moves wisely to survive the dungeon!")
        input("\nPress Enter to return to the main menu.")