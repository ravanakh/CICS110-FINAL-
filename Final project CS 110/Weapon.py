import random

class Weapon():
    
    def __init__(self, name, rarity, base_damage, room_level):
        self.name = name
        self.rarity = rarity
        self.base_damage = base_damage
        self.room_level = room_level        
    
    def calculate_damage(self):  
        rarity_multiplier = {
            'Common':  1.0,
            'Uncommon': 1.2,
            'Rare' : 1.5,
            'Epic' : 2.0,
            'Legendary' : 3.0
        }

        return int(self.base_damage * rarity_multiplier[self.rarity] * (1 + self.room_level // 10))
    
    def __str__(self):
        damage = self.calculate_damage() 
        return f"{self.name} ({self.rarity}) - Damage: {damage}"