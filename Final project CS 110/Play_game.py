from Player import Player
from Enemy_Boss import Enemy
from Chest import Chest
import time 

class PlayGame:
    def __init__(self):
        self.player = Player(health=100, damage=15, max_hp=100, defense=10)
        self.current_stage = 1
        self.current_room = 1

    def start_game(self):
        print("\nLet the dungeon adventure begin!")
        while self.current_stage <= 2:
            for self.current_room in range(1, 9): 
                print(f"\nEntering Room {self.current_room} on Stage {self.current_stage}...")
                self.handle_room()

            # Check for second stage
            if self.current_stage == 2 and self.current_room == 8:
                print("\nCongratulations! You have conquered the dungeon!")
                return  # End the game after Stage 2, Room 8

            self.current_stage += 1

    def handle_room(self):
        enemy = Enemy("dummy", 0, 0, 0)
        enemy_instance = enemy.assign_to_room(self.current_stage, self.current_room, self.player)

        if not enemy_instance:
            print("Error: No enemy generated!") 
            exit()

        print(enemy_instance.render_stats())
        
        while enemy_instance.health > 0 and self.player.is_alive():
            self.handle_turn(enemy_instance)

        if not self.player.is_alive():
            print("You have been defeated... Game over!")
            exit()

        print(f"Room {self.current_room} cleared!")

        # If this is Stage 2, Room 8, code will skip reward and chest drops
        if not (self.current_stage == 2 and self.current_room == 8):
            self.reward_player()
    
    def display_stats(self, enemy):
        player_health = f"Player Health: {self.player.health:.1f}/{self.player.max_hp}"
        ultimate_charge = f"Ultimate Charge: {self.player.turns_charging}/8 (Ready: {self.player.ultimate_ready})"
        enemy_health = f"Enemy Health: {enemy.health:.1f}"

        print(f"\n{player_health:<35} {ultimate_charge:<40} {enemy_health}")
        
        
    def handle_boss(self, final_boss=False):
        if final_boss:
            enemy = Enemy.create_boss(self.current_stage, self.current_room)
        else:
            enemy = Enemy.assign_to_room(self.current_stage, self.current_room, self.player)

        print(enemy.render_stats())

        while enemy.health > 0 and self.player.is_alive():
            self.handle_turn(enemy)

        if not self.player.is_alive():
            print("You have been defeated... Game over!")
            exit()

        print("Boss defeated! You are one step closer to victory!")
        if not final_boss:
            self.reward_player()
    
    def display_health_bar(self, health, max_health):
        bar_length = 20  
        filled_length = int(bar_length * health // max_health)  
        bar = '█' * filled_length + '-' * (bar_length - filled_length)  
        health_percentage = (health / max_health) * 100 
        return f"[{bar}] {health}/{max_health} ({health_percentage:.0f}%)"
        
    def handle_turn(self, enemy):
        # Display current stats
        print(f"\nPlayer Health: {self.display_health_bar(self.player.health, self.player.max_hp)}")
        print(f"Enemy Health: {self.display_health_bar(enemy.health, enemy.max_health)}")
        print(f"\n--- Player's Stats ---")
        print(f"Health: {self.display_health_bar(self.player.health, self.player.max_hp)}  "
            f"Attack: {self.player.damage}  Defense: {self.player.defense}  Dodge Chance: {self.player.dodge_chance}%")
        print(f"Weapon: {self.player.current_weapon}\n")

        print(f"--- Enemy's Stats ---")
        print(f"Health: {self.display_health_bar(enemy.health, enemy.max_health)}  "
            f"Attack: {enemy.damage}  Defense: {enemy.defense}\n")

        # Player's turn
        print("\nYour turn!")
        print(f"Ultimate Charge: {self.player.turns_charging}/8 (Ready: {self.player.ultimate_ready})")

        # Give ptions
        print("Choose an action:")
        print("1. Attack")
        print("2. Dodge")
        print("3. Use Potion")
        if self.player.ultimate_ready and not self.player.ultimate_used:  
            print("4. Use Ultimate Attack")

        choice = None
        while choice not in ["1", "2", "3", "4"]:  
            choice = input("Choose an action (1, 2, 3, 4): ")
            if choice == "1":
                damage_dealt = self.player.attack(enemy)
                print(damage_dealt)
            elif choice == "2":
                print(self.player.dodge(enemy.damage))
            elif choice == "3":
                self.player.use_potion()
            elif choice == "4" and self.player.ultimate_ready and not self.player.ultimate_used:
                print(self.player.ultimate_attack(enemy))  # Use the ultimate
            else:
                print("Invalid choice, please select 1, 2, 3, or 4.")

        # Enemy's turn
        if enemy.health > 0:
            print(f"\nEnemy's turn!")
            print(self.player.got_hit(enemy.damage)) 
                    
    def reward_player(self):
        print("\nYou have cleared the room! Time for a reward!")
        self.player.complete_stage_one()

        chest = Chest(room_level=self.current_room)
        self.player.open_chest(chest)

        heal_amount = self.player.max_hp * 0.30
        self.player.health = min(self.player.max_hp, self.player.health + heal_amount)  
        print(f"You have been healed for {heal_amount:.0f} HP!")