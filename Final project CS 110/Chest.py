import random
from Weapon import Weapon 

class Chest():
    def __init__(self, room_level):
        self.room_level = room_level
        self.drop_type = random.choice(['weapon', 'potion'])  # Randomly decide between a weapon or potion

        # Generate either a weapon or potion based on drop_type
        if self.drop_type == 'weapon':
            self.weapon = self.generate_random_weapon()
            self.potion = None  # No potion for this chest
        elif self.drop_type == 'potion':
            self.weapon = None  # No weapon for this chest
            self.potion = self.generate_random_potion()

    def generate_random_weapon(self):
        rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
        rarity_weights = [50, 30, 15, 4, 1]
        chosen_rarity = random.choices(rarities, weights=rarity_weights, k=1)[0]

        weapon_names = {
            "Common": ["Rusty Sword", "Wooden Club", "Wooden Sword"],
            "Uncommon": ["Iron Sword", "Steel Dagger", "Iron Staff"],
            "Rare": ["Elven Blade", "Orcish War Axe", "Refined Longsword"],
            "Epic": ["Dragon Slayer", "Shadow Fang", "Entangled Staff"],
            "Legendary": ["Excalibur", "Godslayer", "Demon's Lust"],
        }
        name = random.choice(weapon_names[chosen_rarity])
        base_damage = random.randint(5, 20)
        return Weapon(name, chosen_rarity, base_damage, self.room_level)

    def generate_random_potion(self):
        potion_names = ['Small Healing Potion', 'Large Healing Potion', 'Defense Potion']
        potion_effects = {
            'Small Healing Potion': 20,  # Heals 20 HP
            'Large Healing Potion': 50,  # Heals 50 HP
            'Defense Potion': 10  # Adds 10 defense for one room
        }

        potion_name = random.choice(potion_names)
        return {'name': potion_name, 'effect': potion_effects[potion_name]}

    def get_drop(self):
        # Return either weapon or potion based on what was randomly chosen
        if self.drop_type == 'weapon':
            return self.weapon  # Return weapon if drop_type is weapon
        else:
            return self.potion  # Return potion if drop_type is potion