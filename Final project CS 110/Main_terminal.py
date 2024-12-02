from Menu import MainMenuScreen
from Play_game import PlayGame

def main():
    menu = MainMenuScreen()
    while True:
        menu.display()
        choice = menu.get_choice()
        if choice == "1":
            game = PlayGame()
            game.start_game()
            break
        elif choice == "2":
            menu.instructions()
        elif choice == "3":
            print("Thank you for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()