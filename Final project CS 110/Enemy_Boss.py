import random

class Enemy:
    enemies_names = ['Skeleton', 'Goblin', 'Fireball', 'Slime']
    bosses_names = ['Magma Cube', 'Huge Skeleton Boss', 'Flying Controller', 'Final Dragon Boss']

    def __init__(self, name, health, damage, defense, boss = False, dodge_chance = 0.0):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.max_health = health
        self.dodge_chance = dodge_chance
        self.boss = boss

    def generate_enemy(self, stage, room_number):
        if room_number <= 4:
            health_scaling = 50 + (stage * 5) + (room_number * 5)
            damage_scaling = 10 + (stage * 2) + (room_number * 1)
            defense_scaling = 3 + (stage * 1) + (room_number * 1)
        else:
            health_scaling = 150 + (stage * 30) + (room_number * 15)
            damage_scaling = 30 + (stage * 5) + (room_number * 3)
            defense_scaling = 20 + (stage * 3) + (room_number * 2)

        dodge_chance = random.uniform(0.1, 0.2) 
        return Enemy(name="Regular Enemy", health=health_scaling, damage=damage_scaling, 
                     defense=defense_scaling, dodge_chance=dodge_chance)

    def create_boss(self, stage, room_number):
        if room_number <= 4:
            health_scaling = 100 + (stage * 10) + (room_number * 5)
            damage_scaling = 30 + (stage * 5) + (room_number * 5)
            defense_scaling = 10 + (stage * 4) + (room_number * 3)
        else:
            health_scaling = 450 + (stage * 50) + (room_number * 320)
            damage_scaling = 40 + (stage * 30) + (room_number * 15)
            defense_scaling = 50 + (stage * 10) + (room_number * 10)

        dodge_chance = random.uniform(0.2, 0.5) 
        return Enemy(name="Boss", health=health_scaling, damage=damage_scaling, 
                     defense=defense_scaling, boss=True, dodge_chance=dodge_chance)

    def assign_to_room(self, stage, room_number, player):
        print(f"Assigning to stage {stage}, room {room_number}")
        if room_number in [1, 2, 3]:
            return self.generate_enemy(stage, room_number)
        elif room_number == 4 or room_number == 8:
            return self.create_boss(stage, room_number)
        elif room_number in [5, 6, 7]:
            return self.generate_enemy(stage, room_number)

        print("Error: No enemy generated!")
        return None

    def take_damage(self, amount):
        if random.random() < self.dodge_chance:
            return f"{self.name} dodged the attack!"

        effective_damage = max(0, amount - self.defense) 
        self.health -= effective_damage
        if self.health <= 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} took {effective_damage} damage and has {self.health} HP remaining."

    def render_stats(self):
        return (f"{'Boss' if self.boss else 'Enemy'}: {self.name}\n"
                f"Health: {self.health}/{self.max_health}\n"
                f"Damage: {self.damage}\n"
                f"Defense: {self.defense}\n"
                f"Dodge Chance: {self.dodge_chance * 100:.1f}%") 
        
    def try_dodge(self):
        if random.random() < self.dodge_chance:
            return True
        return False