# Ravan
import random 

class Enemy:
    def __init__(self, name, health, damage, boss = False):
        self.name = name
        self.health = health
        self.damage = damage
        self.boss = boss
    enemies_names = ['Skeleton','Goblin','Fireball','Slime']
    health_enemy = random.randint(40,60)
    damage_enemy = random.randint(8,16)
    names_enemy = random.choice(enemies_names)

    bosses_names = ['Magma Cube','Huge Skeleton Boss','Flying Controller','Final Dragon Boss']

    
    def create_enemy():
        name = random.choice(Enemy.enemies_names)
        health = random.randint(40, 60)
        damage = random.randint(8, 16)
        return Enemy(name, health, damage)

    
    def create_boss(name, health, damage):
        return Enemy(name, health, damage, boss = True)
    
        
    def assign_boss_andd_enemies_to_room_and_stages(stage, room_number):
        if stage == 1:
            bosses_stage_1 = ['Magma Cube', 'Huge Skeleton Boss']
            if room_number in [1,2,3]:
                return Enemy.create_enemy()
            elif room_number == 4:
                return Enemy.create_boss(bosses_stage_1[0], random.randint(100, 150), random.randint(20, 30))
            elif room_number in [5,6,7]:
                return Enemy.create_enemy
            elif room_number == 8:
                return Enemy.create_boss(bosses_stage_1[1], random.randint(150, 200), random.randint(30, 40))
        elif stage == 2:
            bosses_stage_2 = ['Flying Controller', 'Final Dragon Boss']
            if room_number in [1,2,3]:
                return Enemy.create_enemy()
            elif room_number == 4:
                return Enemy.create_boss(bosses_stage_2[0], random.randint(100, 150), random.randint(20, 30))
            elif room_number in [5,6,7]:
                return Enemy.create_enemy
            elif room_number == 8:
                return Enemy.create_boss(bosses_stage_2[1], random.randint(200, 300), random.randint(25, 45))


   # guys, I made this func below for printing out the boss/enemy if some requirements are met. Further we can go without this 
    def print_enemy(self):
        if self.boss:
            print(f"Boss Name: {self.name}")
            print(f"Health: {self.health}")
            print(f"Damage: {self.damage}")
        else:
            print(f"Enemy Name: {self.name}")
            print(f"Health: {self.health}")
            print(f"Damage: {self.damage}")

#for testing if u wanna check:

# random_enemy = Enemy.create_enemy()
# random_enemy.print_enemy()

# # Create a boss and print its details
# boss = Enemy.assign_boss_andd_enemies_to_room_and_stages(stage=1, room_number=2)
# if boss:
#     boss.print_enemy()

# # Create another boss for stage 2
# final_boss = Enemy.assign_boss_andd_enemies_to_room_and_stages(stage=2, room_number=8)
# if final_boss:
#     final_boss.print_enemy()