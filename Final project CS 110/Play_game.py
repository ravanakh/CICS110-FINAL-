from Player import Player
from Enemy_Boss import Enemy
from Chest import Chest

class PlayGame:
    def __init__(self):
        self.player = Player(health=100, damage=10, max_hp=100, defense=0)
        self.current_stage = 1
        self.current_room = 1

    def start_game(self):
        print("\nLet the dungeon adventure begin!")
        while self.current_stage <= 2:  # Two stages, each with 8 rooms
            for self.current_room in range(1, 9):  # 8 rooms per stage
                print(f"\nEntering Room {self.current_room} on Stage {self.current_stage}...")
                self.handle_room()
            self.current_stage += 1

        print("\nYou have reached the final boss room!")
        self.handle_boss(final_boss=True)

        print("\nCongratulations! You have conquered the dungeon!")

    def handle_room(self):
        # Generate the enemy
        enemy = Enemy.assign_to_room(self.current_stage, self.current_room, self.player)
        if not enemy:
            print("Error: No enemy generated!")
            exit()  # Exit if no enemy was generated

        print(enemy.render_stats())

        # Battle loop
        while enemy.health > 0 and self.player.is_alive():
            self.handle_turn(enemy)

        if not self.player.is_alive():
            print("You have been defeated... Game over!")
            exit()

        print(f"Room {self.current_room} cleared!")
        self.reward_player()

    def handle_boss(self, final_boss=False):
        if final_boss:
            enemy = Enemy.create_boss(self.current_stage, self.current_room, self.player)
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

    def handle_turn(self, enemy):
        print("\nYour turn!")
        print("1. Attack")
        print("2. Evade")
        print("3. Use Item")
        choice = None
        while choice not in ["1", "2", "3"]:
            choice = input("Choose an action (1, 2, 3): ")
            if choice not in ["1", "2", "3"]:
                print("Invalid choice. Please choose 1, 2, or 3.")

        if choice == "1":
            print(self.player.attack(enemy))
        elif choice == "2":
            print(self.player.dodge(enemy.damage))
        elif choice == "3":
            print(self.player.use_potion())

        # Enemy's turn if it's still alive
        if enemy.health > 0:
            print("\nEnemy's turn!")
            print(self.player.got_hit(enemy.damage))

    def reward_player(self):
        # Apply a random buff
        print("\nYou have cleared the room! Time for a reward!")
        self.player.complete_stage_one()

        # Generate and open a chest
        chest = Chest(room_level=self.current_room)
        self.player.open_chest(chest)