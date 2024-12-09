import random
from Enemy_Boss import Enemy
from Weapon import Weapon
import time

class Player():
    health = 100
    damage = 10
    defense = 5
    buffs = ['Blessing of earth',"Blesssing of wind",'Blessing of strength', 'Blessing of soul', 'Blessing of iron', 'Blessing of the moon','Blessing of the sun', 'Blessing of demon', 'Unknown Blessing','Cursed being', 'Gods favor' ]

    
    def __init__ (self,health,damage,max_hp,defense):
        self.health = health
        self.max_hp = max_hp
        self.damage = damage 
        self.current_hp = health
        self.defense = defense
        self.inventory = {}
        self.stamina = 100
        self.status_effects = {}
        self.is_blocking = False
        self.stage = 1
        self.dodge_chance = 0.25
        self.blessing = {}
        self.ultimate_ready = False
        self.ultimate_used = False
        self.turns_charging = 0
        self.current_weapon = Weapon("Basic Sword",'Common',5,1)
        self.alive = True
        

    def got_hit(self, enemy_damage):
        if self.is_blocking:
            reduce_damage = max(0, enemy_damage // 2)
            reduce_damage = max(0, reduce_damage - self.defense)
            self.health -= reduce_damage
            self.is_blocking = False
            return f"You blocked! Took only {reduce_damage} damage."
        else:
            reduce_damage = max(0, enemy_damage - self.defense)
            self.health -= reduce_damage
            if self.health < 0: 
                self.health = 0
            return f"You took {reduce_damage} damage."
        
    def add_potion(self, potion):
        potion_name = potion['name']
        potion_effect = potion['effect']
        
        if potion_name in self.inventory:
            self.inventory[potion_name] += 1 
        else:
            self.inventory[potion_name] = 1  

        print(f"Added {potion_name} to your inventory!")

    def use_potion(self):
        if not self.inventory:
            return "No potions left in your inventory!" 

        print("\nAvailable Potions:")
        for idx, (potion_name, quantity) in enumerate(self.inventory.items(), start=1):
            print(f"{idx}. {potion_name} - Quantity: {quantity}")

        choice = None
        while choice not in range(1, len(self.inventory) + 1):
            try:
                choice = int(input(f"Choose a potion to use (1-{len(self.inventory)}): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
        potion_name = list(self.inventory.keys())[choice - 1]
        potion_quantity = self.inventory[potion_name]  

        potion_effects = {
            'Small Healing Potion': 20,
            'Large Healing Potion': 50,
            'Defense Potion': 10
        }

        potion_effect = potion_effects.get(potion_name, 0)  

        if 'Healing' in potion_name:
            healed_amount = min(potion_effect, self.max_hp - self.health)
            self.health += healed_amount
            print(f"You used {potion_name} and healed for {healed_amount} HP!")

        elif 'Defense' in potion_name:
            self.defense += potion_effect 
            print(f"You used {potion_name} and gained {potion_effect} defense!")

        if self.inventory[potion_name] > 1:
            self.inventory[potion_name] -= 1 
        else:
            del self.inventory[potion_name]  
        return f"{potion_name} used."
            
    def block(self):
        self.is_blocking = True
        self.stamina = min(100, self.stamina + 20) 
        return "You brace yourself, reducing incoming damage and recovering stamina!"
    
    def apply_status_effects(self):
        damage_taken = 0
        for effect, turns in list(self.status_effects.items()):
            if effect == "Poison":
                damage_taken += 5  
                print(f"You take 5 poison damage! ({turns} turns remaining)")
            elif effect == "Burn":
                damage_taken += 10  
                print(f"You take 10 burn damage! ({turns} turns remaining)")

            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                del self.status_effects[effect]

        self.health -= damage_taken
        if self.health < 0:
            self.health = 0
    
    def dodge(self, enemy_damage):
        if self.dodge_chance <= 0:
            return "You cannot evade!"
        self.stamina = min(100, self.stamina + 20)  
        
        if random.random() < self.dodge_chance: 
            return "You successfully dodged the attack and regained 20 stamina!"
        
        # Failed dodge
        failed_dodge_damage = enemy_damage * 1.25
        self.health -= failed_dodge_damage
        return f"You failed to dodge the attack and took {failed_dodge_damage:.1f} damage. But you still regained 20 stamina."


    def display_stamina_bar(self):
        bar_length = 20
        filled_length = int(bar_length * self.stamina // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        return f"Stamina: [{bar}] {self.stamina}/100"

    
    def attack(self, enemy):
        if self.stamina < 5:  
            return "Not enough stamina to attack! Use dodge to regain stamina."

        self.stamina -= 5  

        if enemy.try_dodge():
            return f"{enemy.name} dodged your attack!"

        is_critical = random.random() < 0.2  
        crit_multiplier = random.uniform(1.1, 1.5) if is_critical else 1.0
        raw_damage = int(self.damage * crit_multiplier)  
        net_damage = max(0, raw_damage - enemy.defense)  

        enemy.take_damage(raw_damage)

        self.increment_turn()

        if is_critical:
            return f"Critical hit! You dealt {net_damage} damage to {enemy.name}!"
        return f"You attacked {enemy.name} and dealt {net_damage} damage!"

    def equip_weapon(self, new_weapon):
        self.current_weapon = new_weapon
        print(f"You have equipped the new weapon: {self.current_weapon.name} - Damage: {self.current_weapon.damage}")
        
        
    def increment_turn(self):
        self.turns_charging += 1
        if self.turns_charging >= 8:
            self.ultimate_ready = True
            print("Your ultimate is ready!")
            
            
    def ultimate_attack(self, enemy):
        if not self.ultimate_ready:
            return "Your ultimate attack is not ready yet!"
        if self.ultimate_used:
            return "You can only use your ultimate once per room."
        if self.stamina < 70: 
            return "Not enough stamina to use your ultimate! Use dodge to regain stamina."

        self.stamina -= 70  
        ultimate_damage = self.damage * 5
        ultimate_damage = max(0, ultimate_damage - enemy.defense)  
        enemy.take_damage(ultimate_damage)
        self.reset_ultimate_attack()

        return f"You used your ultimate and dealt {ultimate_damage} damage to {enemy.name}!"

            
    def reset_ultimate_attack(self):
        self.ultimate_used = True
        self.ultimate_ready = False
        self.turns_charging = 0
        
    def render_stats(self):
        return f"Health: {self.health}/{self.max_hp}, Damage: {self.damage}, Defense: {self.defense}"
    
            
    def complete_stage_one(self):
        buff1,buff2 = self.random_buff_apply()
        print(f'Choose one of the two blessing:')
        print(f'1. {buff1}')
        print(f'2. {buff2}')
        
        choice = None
        while choice not in ['1','2']:
            choice = input('Please announce your choice: 1 or 2: ')
            
        if choice == '1':
            chosen_buff = buff1
        else:
            chosen_buff = buff2
            
        time.sleep(1)
        
        self.apply_buff(chosen_buff)
            
        if chosen_buff in self.blessing:
            self.blessing[chosen_buff] += 1
        else:
            self.blessing[chosen_buff] = 1
        print(f"You have chosen: {chosen_buff}. You now have {self.blessing[chosen_buff]} of this blessing.")     
    
        self.stage +=1
        print(f"Stage {self.stage} completed! You gained a new blessing, the blessing is: {self.blessing}.")
    
    
    def random_buff_apply(self):
        buff_chances = {
            'Blessing of earth': 0.2,  # 20% chance
            'Blessing of wind': 0.15,  # 15% chance
            'Blessing of strength': 0.1,  # 10% chance
            'Blessing of soul': 0.1,  # 10% chance
            'Blessing of iron': 0.1,  # 10% chance
            'Blessing of the moon': 0.05,  # 5% chance
            'Blessing of the sun': 0.05,  # 5% chance
            'Blessing of demon': 0.02,  # 2% chance
            'Unknown Blessing': 0.02,  # 2% chance 
            'Cursed being': 0.005,  # 0.5% chance
            'Gods favor': 0.005  # 0.5% chance
        }
        buff_choices = random.choices(list(buff_chances.keys()), weights=list(buff_chances.values()), k=2)
        
        while buff_choices[0] == buff_choices[1]:
            buff_choices = random.choices(list(buff_chances.keys()), weights=list(buff_chances.values()), k=2)
        
        return buff_choices[0], buff_choices[1]

    def apply_buff(self, chosen_buff):
        if chosen_buff == 'Blessing of earth':
            health_boost = random.randint(15, 35)
            self.max_hp += health_boost
            self.defense += 10
            self.dodge_chance -= 0.05
            print(f'You have gained {health_boost} amount of health, but you got slower')

        elif chosen_buff == "Blessing of wind":
            self.dodge_chance += 0.15
            self.max_hp -= 20
            self.defense -= 10
            if self.dodge_chance > 0.75:
                self.dodge_chance = 0.75
                print(f'Dodge chance has reached the max, cannot increase any further. This buff can no longer be obtained.')
            else:
                print('You have become faster, but you are more vulnerable to attacks')

        elif chosen_buff == 'Blessing of strength':
            self.damage += random.randint(10, 20)
            self.max_hp += random.randint(20, 50)
            self.defense += 5
            self.dodge_chance -= random.uniform(0, 0.03)
            print('You have become stronger, but have become slower')

        elif chosen_buff == 'Blessing of soul':
            self.damage += random.randint(5, 10)
            self.max_hp += random.randint(10, 20)
            self.defense += 10
            self.dodge_chance += random.uniform(0, 0.03)
            print('Overall boost has applied')

        elif chosen_buff == 'Blessing of iron':
            self.max_hp += 60
            self.defense += 20
            self.damage += random.randint(10, 20)
            self.dodge_chance -= 0.15
            print(f'You have gained large amounts of strength, but gotten much slower')

        elif chosen_buff == 'Blessing of the moon':
            damage_boost = 40
            self.damage += damage_boost
            self.defense -= 15
            self.max_hp += 60
            self.dodge_chance = min(0.75, self.dodge_chance + 0.05)
            print(f"You have gained {damage_boost} damage but sacrificed some defense.")

        elif chosen_buff == 'Blessing of the sun':
            self.damage *= 1.17
            self.max_hp *= 1.12
            self.defense += 10
            print(f"You have absorbed some of the sun's energy, You feel powerful")

        elif chosen_buff == 'Blessing of demon':
            self.damage *= 1.25
            self.max_hp *= 1.55
            self.defense -= 100
            self.dodge_chance = 0.1
            print(f'You have made a deal with the devil. You have become unbelievably strong, but at what cost?!.....')

        elif chosen_buff == 'Unknown Blessing':
            self.damage += random.randint(0, 50)
            self.defense += random.randint(0, 50)
            self.dodge_chance = 0.75
            self.max_hp *= 1.5
            print(f'yOUOUou AreeeEEe The bLesSed ONe................')

        elif chosen_buff == 'Cursed being':
            self.defense = 0
            self.max_hp *= 5
            self.damage *= 3
            self.dodge_chance -= 0.15
            print(f'This will be a wonderful gamble, what do you say !>?')

        elif chosen_buff == 'Gods favor':
            self.defense += 130
            self.max_hp *= 5
            self.damage *= 10
            self.dodge_chance = 0.75
            print(f'You have been blessed by Gods, May your journey be full of success')
    
    def is_alive(self):
        return self.health > 0
    
    def open_chest(self, chest):
        drop = chest.get_drop()

        if isinstance(drop, Weapon):
            new_weapon = drop
            print("A chest has been opened!")
            print(f"Inside, you find a new weapon: {new_weapon.name} - Damage: {new_weapon.damage}")
            print(f"Your current weapon: {self.current_weapon.name} - Damage: {self.current_weapon.damage}")

            choice = None
            while choice not in ["yes", "no"]:
                choice = input("Do you want to replace your current weapon with this one? (yes/no): ").lower()
                if choice not in ["yes", "no"]:
                    print("Please respond with 'yes' or 'no'.")

            if choice == "yes":
                self.current_weapon = new_weapon
                print(f"You have equipped the new weapon: {self.current_weapon.name} - Damage: {self.current_weapon.damage}")
            else:
                print(f"You decided to keep your current weapon. The {new_weapon.name} has been discarded.")

        elif isinstance(drop, dict):  
            potion = drop
            self.add_potion(potion)
            print(f"You received a {potion['name']}!")

        else:
            print("Error: The chest does not contain valid loot.")

        

            

        