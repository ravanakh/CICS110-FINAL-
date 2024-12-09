import random
from Weapon import Weapon 

class Chest():
    def __init__(self, room_level):
        self.room_level = room_level
        self.drop_type = random.choice(['weapon', 'potion']) 
        if self.drop_type == 'weapon':
            self.weapon = self.generate_random_weapon()
            self.potion = None 
        elif self.drop_type == 'potion':
            self.weapon = None  
            self.potion = self.generate_random_potion()

    def generate_random_weapon(self):
        # Select rarity based on some weights
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
        base_damage = random.randint(5, 15)  # Random base damage for simplicity

        # Create the weapon object with the calculated damage
        return Weapon(name, chosen_rarity, base_damage, self.room_level)
    
    
    def generate_random_potion(self):
        potion_names = ['Small Healing Potion', 'Large Healing Potion', 'Defense Potion']
        potion_effects = {
            'Small Healing Potion': 20,
            'Large Healing Potion': 50,  
            'Defense Potion': 10 
        }
        potion_name = random.choice(potion_names)
        return {'name': potion_name, 'effect': potion_effects[potion_name]}

    def get_drop(self):
        if self.drop_type == 'weapon':
            return self.weapon
        elif self.drop_type == 'potion':
            return self.potion
        else:
            raise ValueError(f"Unexpected drop_type: {self.drop_type}")