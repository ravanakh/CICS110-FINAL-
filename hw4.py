import random #ravan
def prompt():
    print("\t\t\tWelcome to Our Game\n\n"
          "\tYou have to defeat all bosses on 3 stages to Complete the Game!")
    start_the_game = input("\t\t\tPress any ket to continue")


prompt()
def chest():
    chest_items = ["Health Potion", "Greater Health Potion", "Mana Potion", "Greater Mana Potion", "Stamina Potion", "Greater Stamina Potion", "Elixir of Strength", "Elixir of Defense", "Rusty Sword (1★)", "Iron Sword (2★)", "Steel Sword (3★)", "Enchanted Blade (4★)", "Mythic Sword (5★)", "Full Restore"]
    drop_chances = [
    30,  # Health Potion 
    15,  # Greater Health Potion 
    30,  # Mana Potion 
    15,  # Greater Mana Potion 
    35,  #stamina
    15,  #greater stamina
    10,  #el of strenght
    10,   #el of defense
    25,  # Rusty Sword 
    12,  # Iron Sword 
    10,  # Steel Sword  
    5,   #enchanted blade 4 stars
    3, #mythic blade 5 star
    8,  #full restore of health
    ]
    dropped_item = ', '.join(random.choices(chest_items, weights=drop_chances, k=3))
    print(f'WOW, you got: {dropped_item}')

