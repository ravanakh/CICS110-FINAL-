from Player import Player
from Enemy_Boss import Enemy
import random
from Chest import Chest
import time 
import json
import os

class PlayGame:
    def __init__(self):
        self.player = Player(health=100, damage=20, max_hp=100, defense=10)
        self.current_stage = 1
        self.current_room = 1

    def start_game(self):
        print("\nLet the dungeon adventure begin!")
        while self.current_stage <= 2:
            for self.current_room in range(1, 9):
                print(f"\nEntering Room {self.current_room} on Stage {self.current_stage}...")
                self.handle_room()
                if self.current_stage == 2 and self.current_room == 8:
                    print("\nCongratulations! You have conquered the dungeon!")
                    return  

            self.current_stage += 1
            
            
    def handle_room(self):
        self.player.turns_charging = 0
        self.player.ultimate_ready = False
        self.player.ultimate_used = False
        enemy = Enemy("dummy", 0, 0, 0)
        enemy_instances = enemy.assign_to_room(self.current_stage, self.current_room)

        if not enemy_instances:
            print("Error: No enemies generated!")
            exit()
        for index, enemy_instance in enumerate(enemy_instances, start=1):
            print(f"\n--- Enemy {index} appears! ---")
            print(enemy_instance.render_stats())

            while enemy_instance.health > 0 and self.player.is_alive():
                self.handle_turn([enemy_instance]) 

            if not self.player.is_alive():
                print("\nYou have been defeated... Game over!")
                input("\nPress Enter to return to the main menu.")
                return

            print(f"\nYou defeated {enemy_instance.name}!")

        print(f"\nRoom {self.current_room} cleared!")
        self.reward_player()  
        
        
    def display_stats(self, enemy):
        player_health = f"Player Health: {self.player.health:.1f}/{self.player.max_hp}"
        ultimate_charge = f"Ultimate Charge: {self.player.turns_charging}/8 (Ready: {self.player.ultimate_ready})"
        enemy_health = f"Enemy Health: {enemy.health:.1f}"

        print(f"\n{player_health:<35} {ultimate_charge:<40} {enemy_health}")
        
    
    def display_stamina_bar(self, stamina, max_stamina): #stamina
        bar_length = 20  
        filled_length = int(bar_length * stamina // max_stamina)  
        bar = '░' * filled_length + '-' * (bar_length - filled_length)  
        stamina_percentage = (stamina / max_stamina) * 100 
        return f"[{bar}] {stamina}/{max_stamina} ({stamina_percentage:.0f}%)"
            
    
    def display_player_stats(self):
        print("\n--- Player's Stats ---")
        health_bar = self.display_health_bar(self.player.health, self.player.max_hp)
        stamina_bar = self.display_stamina_bar(self.player.stamina, 100)  
        print(f"Health: {health_bar}")
        print(f"Stamina: {stamina_bar}")
        print(f"Ultimate Charge: {self.player.turns_charging}/8 (Ready: {'Yes' if self.player.ultimate_ready else 'No'})")
        print(f"Attack: {self.player.damage}")
        print(f"Defense: {self.player.defense}") 
        print(f"Dodge Chance: {self.player.dodge_chance * 100:.1f}%")  
        print("=" * 40)
        
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
            input("\nPress Enter to return to the main menu.")
            return

        print("Boss defeated! You are one step closer to victory!")
        if not final_boss:
            self.reward_player()
    
    def display_health_bar(self, health, max_health): #health
        bar_length = 20  
        filled_length = int(bar_length * health // max_health)  
        bar = '█' * filled_length + '-' * (bar_length - filled_length)  
        health_percentage = (health / max_health) * 100 
        return f"[{bar}] {health}/{max_health} ({health_percentage:.0f}%)"

    def handle_turn(self, enemy_instances):
        remaining_enemies = [enemy for enemy in enemy_instances if enemy.health > 0]

        #player_health_bar = self.display_health_bar(self.player.health, self.player.max_hp)
        #player_stamina_bar = self.display_stamina_bar(self.player.stamina, 100)
        #enemy_health_bar = self.display_health_bar(self, enemy.health, enemy.max_health)
        
        while remaining_enemies:
            enemy = remaining_enemies[0]  
            print("=" * 40)

            self.display_player_stats()

            print(f"\n--- {enemy.name}'s Stats ---")
            print(f"Health: {self.display_health_bar(enemy.health, enemy.max_health)}  "
                f"Attack: {enemy.damage}  Defense: {enemy.defense}  Dodge Chance: {enemy.dodge_chance * 100:.1f}%")
            print("=" * 40)

            # Player's turn
            print("\nYour turn!")
            print("=" * 40)
            print(f'''                 +----------------------------------------------------------------------------------+
                                                                                                   
                                                                 {enemy.name} 👾🐉        
                                                                 {self.display_health_bar(enemy.health, enemy.max_health)}  
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
                 YOU 🛡️🤺                                                                       
                 {self.display_health_bar(self.player.health, self.player.max_hp)}                                          
                 {self.display_stamina_bar(self.player.stamina, 100)}                                          
                 +----------------------------------------------------------------------------------+
                 |   Attack ⚔️ [1]  |  Defend 🛡️ [2]  |  Use a Potion 🧪[3]  |  Ultimate Attack 💥[4] |
                 +----------------------------------------------------------------------------------+''')
            
            
            print("=" * 40)

            while True:
                choice = input("Choose an action (1, 2, 3, or 4): ").strip()

                if choice == "1":  # Attack
                    print("\n\n")
                    if self.player.stamina >= 5:
                        result = self.player.attack(enemy) 
                        print(result)
                        break 
                    else:
                        print("Not enough stamina to attack! Choose another action.")
                elif choice == "2": 
                    print("\n\n")
                    print(f"{enemy.name}'s turn!")
                    result = self.player.dodge(enemy.damage)
                    print(result)
                    time.sleep(1)
                    break  
                elif choice == "3": 
                    print("\n\n")
                    if any(item for item in self.player.inventory if "Potion" in item):  
                        result = self.player.use_potion() 
                        print(result)
                        self.display_player_stats()
                        time.sleep(1.5)
                        break  
                    else:
                        print("No potions left in your inventory! Choose another action.")
                elif choice == "4" and self.player.ultimate_ready and not self.player.ultimate_used:
                    print("\n\n")
                    if self.player.stamina >= 70:
                        result = self.player.ultimate_attack(enemy) 
                        print(result)
                        time.sleep(1)
                        break 
                    else:
                        print("Not enough stamina to use your ultimate! Choose another action.")
                else:
                    print("Invalid choice. Please choose a valid action (1, 2, 3, or 4).")
           
            if enemy.health <= 0:
                print(f"{enemy.name} has been defeated!")
                remaining_enemies.pop(0)  
                
            elif choice == '2' and 'successfully' in result: 
                time.sleep(1)
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                continue
            elif choice == '2' and 'failed' in result: 
                time.sleep(1)
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                continue       
            else:
                print(f"{enemy.name}'s turn!")
                print("=" * 40)
                result = self.player.got_hit(enemy.damage)
                print(result)
                time.sleep(1)  
                print("\n\n\n\n\n\n\n\n\n")

                if self.player.health <= 0:
                    print("You have been defeated... Game over!")
                    exit()

            print("=" * 40)

        print("All enemies are defeated!")
        
    
    def reward_player(self):
        print("+----------------------------------------------------------------------------------+")
        print("\nYou have cleared the room! Time for a reward!")
        self.player.complete_stage_one()

        potion = Chest(room_level=self.current_room).generate_random_potion()  
        self.player.add_potion(potion) 

        print("+--------------------------------------------------------------+") 
        print(f"You received a {potion['name']}!")
        print(f"Potions in inventory after addition: {self.player.inventory}") 
        time.sleep(1)

        if random.random() < 0.7:
            weapon = Chest(room_level=self.current_room).generate_random_weapon()
            print("+---------------------------------------------------------------------------------------------------------+") 
            print(f"Inside the chest, you find a new weapon: {weapon.name} - Damage: {weapon.damage}")
            print(f"Your current weapon: {self.player.current_weapon.name} - Damage: {self.player.current_weapon.damage}")

            choice = None
            while choice not in ["yes", "no"]:
                print("+--------------------------------------------------------------------------+") 
                choice = input("Do you want to replace your current weapon with this one? (yes/no): ").strip().lower()
                if choice not in ["yes", "no"]:
                    print("Please respond with 'yes' or 'no'.")

            if choice == "yes":
                self.player.equip_weapon(weapon)
            else:
                print(f"You decided to keep your current weapon. The {weapon.name} has been discarded.")
        else:
            print("No weapon found this time, but you got a potion!")

        heal_amount = self.player.max_hp * 0.30
        self.player.health = min(self.player.max_hp, self.player.health + heal_amount)
        print(f"You have been healed for {heal_amount:.0f} HP!")
        time.sleep(1)
        
        
    def save_game(self):
        save_data = {
            "current_stage": self.current_stage,
            "current_room": self.current_room,
            "player": {
                "health": self.player.health,
                "max_hp": self.player.max_hp,
                "damage": self.player.damage,
                "defense": self.player.defense,
                "inventory": self.player.inventory,
                "stamina": self.player.stamina,
                "dodge_chance": self.player.dodge_chance,
                "blessing": self.player.blessing,
            }
        }
        with open("save_game.json", "w") as f:
            json.dump(save_data, f)
        print("Game saved!")

    def load_game(self):
        try:
            with open("save_game.json", "r") as f:
                save_data = json.load(f)
            self.current_stage = save_data["current_stage"]
            self.current_room = save_data["current_room"]
            player_data = save_data["player"]
            self.player = Player(
                health=player_data["health"],
                max_hp=player_data["max_hp"],
                damage=player_data["damage"],
                defense=player_data["defense"],
            )
            self.player.inventory = player_data["inventory"]
            self.player.stamina = player_data["stamina"]
            self.player.dodge_chance = player_data["dodge_chance"]
            self.player.blessing = player_data["blessing"]
            print("Game loaded!")
        except FileNotFoundError:
            print("No save file found.")