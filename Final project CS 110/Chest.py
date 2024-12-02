import random
from Weapon import Weapon 
class Chest():
        
    def __init__(self, room_level):
        self.room_level = room_level
        self.weapon = self.generate_random_weapon()

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