import random

class Enemy:
    enemies_names = ['Skeleton', 'Goblin', 'Fireball', 'Slime']
    bosses_names = ['Magma Cube', 'Huge Skeleton Boss', 'Flying Controller', 'Final Dragon Boss', 'World Eater']

    def __init__(self, name, health, damage, defense, boss=False, dodge_chance=0.0, can_heal=False):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
        self.max_health = health
        self.can_heal = can_heal
        self.heal_power = random.uniform(0.1, 0.3) if can_heal else 0
        self.dodge_chance = dodge_chance
        self.boss = boss
        self.status_effects = {}

    def apply_status_effect(self, player):
        if "fire" in player.status_effects or "poison" in player.status_effects:
            return f"{self.name} attacked but no new status effect was applied."

        status_effects = ["fire", "poison", None]
        effect_weights = [0.4, 0.3, 0.3]
        chosen_effect = random.choices(status_effects, weights=effect_weights, k=1)[0]

        if chosen_effect == "fire":
            player.add_effect("fire", 3)
            return f"{self.name} inflicted fire damage on you!"
        elif chosen_effect == "poison":
            player.add_effect("poison", 3)
            return f"{self.name} inflicted poison damage on you!"
        return f"{self.name} attacked but applied no status effect."

    def generate_enemy(self, stage, room_number):
        if room_number < 4:
            health_scaling = 50 + (stage * random.randint(3,8)) + (room_number * 5)
            damage_scaling = 10 + (stage * 2) + (room_number * 1)
            defense_scaling = 3 + (stage * random.randint(1,2)) + (room_number * 1)
            dodge_chance = random.uniform(0.1, 0.2)
            can_heal = random.random() < 0.2
        else:
            health_scaling = 150 + (stage * 30) + (room_number * random.randint(13,18))
            damage_scaling = 30 + (stage * 5) + (room_number * random.randint(3,5))
            defense_scaling = 20 + (stage * 3) + (room_number * random.randint(2,4))
            dodge_chance = random.uniform(0.05, 0.1)
            can_heal = random.random() < 0.2

        return Enemy(name="Regular Enemy", health=health_scaling, damage=damage_scaling,
                     defense=defense_scaling, dodge_chance=dodge_chance, can_heal=can_heal)

    def create_boss(self, stage, room_number):
        if room_number == 4:
            health_scaling = 50 + (stage * 7) + (room_number * random.randint(3,10))
            damage_scaling = 30 + (stage * 3) + (room_number * 5)
            defense_scaling = 10 + (stage * 2) + (room_number * 3)
            dodge_chance = random.uniform(0.1, 0.2)
            can_heal = random.random() < 0.2
        else:
            health_scaling = 450 + (stage * 50) + (room_number * 320)
            damage_scaling = 40 + (stage * 30) + (room_number * 15)
            defense_scaling = 50 + (stage * 10) + (room_number * 10)
            dodge_chance = random.uniform(0.2, 0.4)
            can_heal = random.random() < 0.2

        return Enemy(name="Boss", health=health_scaling, damage=damage_scaling,
                     defense=defense_scaling, boss=True, dodge_chance=dodge_chance, can_heal=True)
    
    def assign_to_room(self, stage, room_number):
        enemies = []  
        if (room_number == 8) or (room_number == 4):
            enemies.append(self.create_boss(stage, room_number))
        else:
            num_enemies = random.randint(1, 3)
            print(f"Generating {num_enemies} enemies for room {room_number}...")  
            for _ in range(num_enemies):
                enemies.append(self.generate_enemy(stage, room_number))

        return enemies

    def take_damage(self, amount):
        effective_damage = max(0, amount - self.defense)
        self.health = max(0, self.health - effective_damage)

        if self.health == 0:
            print(f"{self.name} has been defeated!")
            return

    def render_stats(self):
        return (f"{'Boss' if self.boss else 'Enemy'}: {self.name}\n"
                f"Health: {self.health}/{self.max_health}\n"
                f"Damage: {self.damage}\n"
                f"Defense: {self.defense}\n"
                f"Dodge Chance: {self.dodge_chance * 100:.1f}%")

    def try_dodge(self):
        dodge_chance = self.dodge_chance * 0.5 
        return random.random() < dodge_chance

    def choose_action(self, player):
        if self.health < self.max_health * 0.4 and self.can_heal and random.random() < 0.5:
            return self.heal()
        elif random.random() < 0.4:
            return self.apply_status_effect(player)
        else:
            return f"{self.name} attacks for {self.damage} damage!"

    def heal(self):
        heal_amount = int(self.max_health * self.heal_power)
        self.health = min(self.max_health, self.health + heal_amount)
        return f"{self.name} healed for {heal_amount} HP! (Health: {self.health}/{self.max_health})"