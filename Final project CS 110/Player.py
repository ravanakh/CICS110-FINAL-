import random
from Enemy_Boss import Enemy
from Weapon import Weapon

class Player():
    health = 100
    damage = 10
    defense = 0
    buffs = ['Blessing of earth',"Blesssing of wind",'Blessing of strength', 'Blessing of soul', 'Blessing of iron', 'Blessing of the moon','Blessing of the sun', 'Blessing of demon', 'Unknown Blessing','Cursed being', 'Gods favor' ]

    
    def __init__ (self,health,damage,max_hp,defense):
        self.health = health
        self.max_hp = max_hp
        self.damage = damage 
        self.current_hp = max_hp
        self.defense = defense
        self.inventory = []
        self.is_blocking = False
        self.stage = 1
        self.dodge_chance = 0.25
        self.blessing = {}
        self.ultimate_ready = False
        self.ultimate_used = False
        self.turns_charging = 0
        self.current_weapon = Weapon("Basic Sword",'common',5,1)
        self.alive = True
        

    def got_hit(self,enemy_damage):
        if self.is_blocking == True:
            reduce_damage = max(0,enemy_damage//2)
            reduce_damage = max(0,reduce_damage - self.defense)
            self.health -= reduce_damage
            self.is_blocking = False
            return f"You blocked! Took only {reduce_damage} damage."
        else:
            reduce_damage = max(0,reduce_damage - self.defense)
            self.health -= enemy_damage
            return f"You took {enemy_damage} damage."
    
    def add_potion(self,potion):
        self.inventory.append(potion)
        
    def use_potion(self):
        if self.inventory:
            potion_hp = self.inventory.pop(0)
        else:
            return "No potions left in your inventory!"

        if self.inventory:
            potion_hp = self.inventory.pop(0)
            healed_amount = min(potion_hp,self.max_hp - self.current_hp)
            self.current_hp += healed_amount
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            return f"You have used a potion and heled for {healed_amount} HP. Current health: {self.current_hp}/{self.max_hp}"
        else:
            return "No potions left in your inventory!"
            
    def block(self):
        self.is_blocking = True
        return "You raise your guard, preparing to block the next attack!"
    
    def dodge(self,enemy_damage):
        if self.dodge_chance <= 0:
            return f'You can not evade'
        if random.random() < self.dodge_chance:
            return f' You have successfully dodged the attack!'
        else:
            enemy_damage *= 1.25
            self.health -= enemy_damage
            return f' You have failed to dodge the attack, and have taken {enemy_damage}'

    def attack(self,enemy):
        damamge_dealt = max(0,self.damage-enemy.defense)
        enemy.take_damage(damamge_dealt)
        self.increment_turn()
        return f"You attacked {enemy.name} and dealt {damamge_dealt} damage!"
    
    def increment_turn(self):
        self.turns_charging += 1
        if self.turns_charging > 8 and self.damage >= 100:
            self.ultimate_ready = True
            print('Your ultimate has been charged!')
            
            
    def ultimate_attack(self, enemy):
        if not self.ultimate_ready:
            return "Your ultimate attack is not ready yet!"
        if self.ultimate_used:
            return "You can only use your ultimate once per room."

        multiplier = random.randint(2, 10)
        ultimate_damage = max(0, self.damage * multiplier - enemy.defense)
        
        enemy.take_damage(ultimate_damage)
        self.reset_ultimate_attack()
        
        return f"You used your ultimate and dealt {ultimate_damage} damage!"
    
    def reset_ultimate_attack(self):
        self.ultimate_used = False
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
            choice = input('Please announce your choice: 1 or 2')
            
        if choice == '1':
            chosen_buff = buff1
        else:
            chosen_buff = buff2
        self.apply_buff(chosen_buff)
            
        if chosen_buff in self.blessing:
            self.blessing[chosen_buff] += 1
        else:
            self.blessing[chosen_buff] = 1
        print(f"You have chosen: {chosen_buff}. You now have {self.blessing[chosen_buff]} of this blessing.")     
    
        self.stage +=1
        print(f"Stage {self.stage} completed! You gained a new blessing, the blessing is: {self.blessing}.")
    
    def random_buff_apply(self):      
        chance = [0.25,0.20,0.15,0.10,0.10,0.05,0.05,0.03,0.03,0.3,0.01]
        
        buff_choices = random.choices(self.buffs, weights=chance, k=2)
        while buff_choices[0] == buff_choices[1]: 
            buff_choices = random.choices(self.buffs, weights=chance, k=2)
        
        return buff_choices[0], buff_choices[1]
    
    
    def apply_buff(self,chosen_buff):
        if chosen_buff == 'Blessing of earth':
            health_boost = random.randint(10,30)   
            self.max_hp += health_boost
            self.defense += 5
            self.dodge_chance -= 0.05
            print(f'You have gained {health_boost} amount of health, But you got slower')
     
        elif chosen_buff == "Blessing of wind":
            self.dodge_chance += 0.15
            self.max_hp -= 10
            self.defense -= 3
            if self.dodge_chance > 0.75:
                self.dodge_chance = 0.75
                self.buffs.remove("Blessing of wind")
                print(f'Dodge chance has reached the max, can not increase any further, this buff can no longer be obtained')
            else:
                print('You have become faster, but you are more vunerable to attacks')
        elif chosen_buff == 'Blessing of strength':
            self.damage += random.randint(10,15)
            self.max_hp += random.randint(10,15)
            self.defense += 5
            self.dodge_chance -= random.randint(0,.03)
            print('You have become stronger, but have become slower')
      
        elif chosen_buff == 'Blessing of soul':
            self.damage += random.randint(5,10)
            self.max_hp += random.randint(10,20)
            self.defense += 10
            self.dodge_chance += random.randin(0,.03)
            print('Overall boost have applied')
       
        elif chosen_buff == 'Blessing of iron':
            self.max_hp += 40
            self.defense += 10
            self.damage += random.randint(10,20)
            self.dodge_chance -= 0.15
            print(f'You have gained large amounts of strength, but gotten much slower')
      
        elif chosen_buff == 'Blessing of the moon':
            damage_boost = 30
            self.damage += damage_boost
            self.defense -= 10
            self.max_hp += 10
            self.dodge_chance = min(0.75, self.dodge_chance + 0.05)
            print(f"You have gained {damage_boost} damage but sacrificed some defense.")
            
        elif chosen_buff == 'Blessing of the sun':
            self.damage *= 1.25
            self.max_hp *= 1.15
            self.defense += 10
            print(f"You have absorbed some of the sun's energy, You feel powerful")
            
        elif chosen_buff == 'Blessing of demon':
            self.damage *= 1.75
            self.max_hp *= 2
            self.defense -= 100
            self.dodge_chance = 0.1
            print(f'You have made a deal with the devil. You have became unbelievablely strong, but at what cost?!.....')
        
        elif chosen_buff == 'Unknown Blessing':
            self.damage += random.randint(0,50)
            self.defense += random.randint(0,100)
            self.dodge_chance = 0.75
            self.max_hp *= 1.5
            print(f'yOUOUou AreeeEEe The bLesSed ONe................')
        
        elif chosen_buff == 'Cursed being':
            self.defense = 0
            self.max_hp *= 5
            self.damage *= 3
            self.dodge_chance -= 0.05
            print(f'This will be a wonderful gamble, what do you say !>?')
            
        elif chosen_buff == 'Gods favor':
            self.defense += 150
            self.max_hp *= 5
            self.damage *= 10
            self.dodge_chance = 0.75
            print(f'You have been blessed by Gods, May your journy be full of success')
    
    def is_alive(self):
        self.alive = self.health > 0 
        return self.alive
    
    def open_chest(self, chest):
        new_weapon = chest.weapon  
        new_weapon_damage = new_weapon.calculate_damage()

        current_weapon_damage = self.current_weapon.calculate_damage()
        print("A chest has been opened!")
        print(f"Inside, you find a new weapon: {new_weapon} - Damage: {new_weapon_damage}")
        print(f"Your current weapon: {self.current_weapon} - Damage: {current_weapon_damage}")
        choice = None
        while choice not in ["yes", "no"]:
            choice = input("Do you want to replace your current weapon with this one? (yes/no): ").lower()
            if choice not in ["yes", "no"]:
                print("Please respond with 'yes' or 'no'.")


        if choice == "yes":
            self.current_weapon = new_weapon
            print(f"You have equipped the new weapon: {self.current_weapon} - Damage: {new_weapon_damage}")
        else:
            print(f"You decided to keep your current weapon. The {new_weapon} has been discarded.")
        

    

           

    