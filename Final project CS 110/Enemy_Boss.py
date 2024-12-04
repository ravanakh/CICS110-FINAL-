import random

class Enemy:
    enemies_names = ['Skeleton', 'Goblin', 'Fireball', 'Slime']
    bosses_names = ['Magma Cube', 'Huge Skeleton Boss', 'Flying Controller', 'Final Dragon Boss']

    def __init__(self, name, health, damage, defense, boss=False):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.max_health = health
        self.boss = boss

    def generate_enemy(self, stage, room_number):
        # Scaling for first 4 rooms: lower scaling for early game
        if room_number <= 4:
            health_scaling = 50 + (stage * 10) + (room_number * 5)  # Moderate scaling
            damage_scaling = 10 + (stage * 2) + (room_number * 1)
            defense_scaling = 3 + (stage * 1) + (room_number * 1)
        else:
            # Increased scaling for later rooms: exponential difficulty curve
            health_scaling = 50 + (stage * 30) + (room_number * 15)
            damage_scaling = 10 + (stage * 5) + (room_number * 3)
            defense_scaling = 3 + (stage * 3) + (room_number * 2)

        return Enemy(name="Regular Enemy", health=health_scaling, damage=damage_scaling, defense=defense_scaling)

    def create_boss(self, stage, room_number):
        # Boss scaling should be more aggressive, increasing as rooms and stages progress
        if room_number <= 4:
            health_scaling = 150 + (stage * 20) + (room_number * 10)
            damage_scaling = 30 + (stage * 3) + (room_number * 2)
            defense_scaling = 10 + (stage * 2) + (room_number * 1)
        else:
            health_scaling = 150 + (stage * 50) + (room_number * 30)  # Much higher scaling for bosses after room 4
            damage_scaling = 30 + (stage * 10) + (room_number * 5)
            defense_scaling = 10 + (stage * 5) + (room_number * 3)

        return Enemy(name="Boss", health=health_scaling, damage=damage_scaling, defense=defense_scaling)

    def assign_to_room(self, stage, room_number, player):
        print(f"Assigning to stage {stage}, room {room_number}")  # Debug message
        if stage == 1:
            if room_number in [1, 2, 3]:
                return self.generate_enemy(stage, room_number)
            elif room_number == 4:
                return self.create_boss(stage, room_number)
            elif room_number in [5, 6, 7]:
                return self.generate_enemy(stage, room_number)
            elif room_number == 8:
                return self.create_boss(stage, room_number)
        elif stage == 2:
            if room_number in [1, 2, 3]:
                return self.generate_enemy(stage, room_number)
            elif room_number == 4:
                return self.create_boss(stage, room_number)
            elif room_number in [5, 6, 7]:
                return self.generate_enemy(stage, room_number)
            elif room_number == 8:
                return self.create_boss(stage, room_number)

        print("Error: No enemy generated!")  # Fallback error message
        return None

    def render_stats(self):
        if self.boss:
            return (f"Boss: {self.name}\n"
                    f"Health: {self.health}/{self.max_health}\n"
                    f"Damage: {self.damage}\n"
                    f"Defense: {self.defense}")
        else:
            return (f"Enemy: {self.name}\n"
                    f"Health: {self.health}/{self.max_health}\n"  # Use max_health here
                    f"Damage: {self.damage}\n"
                    f"Defense: {self.defense}")

    def take_damage(self, amount):
        effective_damage = max(0, amount)  # No negative damage
        self.health -= effective_damage
        if self.health <= 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} has {self.health} HP remaining."