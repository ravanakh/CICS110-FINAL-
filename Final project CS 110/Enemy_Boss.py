import random

class Enemy():
    enemies_names = ['Skeleton', 'Goblin', 'Fireball', 'Slime']
    bosses_names = ['Magma Cube', 'Huge Skeleton Boss', 'Flying Controller', 'Final Dragon Boss']

    def __init__(self, name, health, damage, defense, boss=False):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.boss = boss

   
    def create_enemy(cls, stage, room_number):
        # Using class-level method for creating an enemy
        health = random.randint(40, 60) + (room_number * 5) + (stage * 20)
        damage = random.randint(8, 16) + (room_number * 3) + (stage * 5)
        defense = random.randint(0, 5) + (stage * 2) + (room_number // 2)
        return Enemy(random.choice(cls.enemies_names), health, damage, defense)

    def create_boss(cls, stage, room_number):
        boss_name = random.choice(cls.bosses_names)
        health = random.randint(100, 150) + (stage * 50) + (room_number * 10)
        damage = random.randint(20, 40) + (stage * 10) + (room_number * 3)
        defense = random.randint(5, 15) + (stage * 5) + (room_number * 2)
        return Enemy(boss_name, health, damage, defense, boss=True)

    def assign_to_room(self, stage, room_number):
        if stage == 1:
            if room_number in [1, 2, 3]:
                return self.create_enemy(stage, room_number)
            elif room_number == 4:
                return self.create_boss(stage, room_number)
            elif room_number in [5, 6, 7]:
                return self.create_enemy(stage, room_number)
            elif room_number == 8:
                return self.create_boss(stage, room_number)
        elif stage == 2:
            # Handle stage 2 in a similar way
            if room_number in [1, 2, 3]:
                return self.create_enemy(stage, room_number)
            elif room_number == 4:
                return self.create_boss(stage, room_number)
            elif room_number in [5, 6, 7]:
                return self.create_enemy(stage, room_number)
            elif room_number == 8:
                return self.create_boss(stage, room_number)

    def render_stats(self):
        if self.boss:
            return (f"Boss: {self.name}\n"
                    f"Health: {self.health}\n"
                    f"Damage: {self.damage}\n"
                    f"Defense: {self.defense}")
        else:
            return (f"Enemy: {self.name}\n"
                    f"Health: {self.health}\n"
                    f"Damage: {self.damage}\n"
                    f"Defense: {self.defense}")

    def take_damage(self, amount):
        effective_damage = max(0, amount - self.defense)
        self.health -= effective_damage
        if self.health <= 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} has {self.health} HP remaining."