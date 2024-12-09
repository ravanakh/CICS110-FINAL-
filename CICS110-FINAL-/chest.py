import random

def prompt():
    print("\t\t\tWelcome to Our Game\n\n"
          "\tYou have to defeat all bosses on 3 stages to complete the game!")
    input("\t\t\tPress any key to continue")

def chest():
    # Dictionary with items as keys and drop chances as values
    chest_items = {
        "Health Potion": 30,
        "Greater Health Potion": 15,
        "Mana Potion": 30,
        "Greater Mana Potion": 15,
        "Stamina Potion": 35,
        "Greater Stamina Potion": 15,
        "Elixir of Strength": 10,
        "Elixir of Defense": 10,
        "Rusty Sword (1★)": 25,
        "Iron Sword (2★)": 12,
        "Steel Sword (3★)": 10,
        "Enchanted Blade (4★)": 5,
        "Mythic Sword (5★)": 3,
        "Full Restore": 8
    }
    

dropped_items = ', '.join(random.choices(list(chest_items.keys()), weights=chest_items.values(), k=3))
print(f'WOW, you got: {dropped_items}')

