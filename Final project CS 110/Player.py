import random
class Player():
    health = 100
    damage = 10
    defense = 0
    buffs = ['Blessing of earth',"Blesssing of wind",'Blessing of strength', 'Blessing of soul', 'Blessing of iron', 'Blessing of the moon','Blessing of the sun', 'Blessing of demon', 'Unknown Blessing','Cursed being', 'Gods favor' ]

    
    def __init__ (self,health,damage,max_hp,defense):
        self.health = health
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
        if self.turns_charning > 8 and self.damage >= 100:
            self.ultimate_ready = True
            print(f'Your ultimate has been charged')
            
            
    def ultimate_attack(self,enemy):
        if not self.ultimate_ready:
            return f'Your ultimate attack is not ready yet'
        if self.ultimate_used:
            return f'You can only use your ultimate once per room'
        
        n = random.randint(2,10)
        b = 1
        ultimate_damage = max(0,self.damamge*n*b - enemy.defense)
        self.ultimate_ready = False
        self.ultimate_used = True
        self.turns_charging = 0
        result = enemy.take_damage(ultimate_damage)
        return f'You have used your ultimate attack and have dealt {n} times your damage, causing {result} done on the enemy'
    
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
        print(f"You have chosen: {chosen_buff}. You now have {self.blessings[chosen_buff]} of this blessing.")     
    
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
            self.max_hp += random.randit(10,15)
            self.defense += 5
            self.dodge_chance -= random.randit(0,.03)
            print('You have become stronger, but have become slower')
      
        elif chosen_buff == 'Blessing of soul':
            self.damage += random.randint(5,10)
            self.max_hp += random.randit(10,20)
            self.defense += 10
            self.dodge_chance += random.randit(0,.03)
            print('Overall boost have applied')
       
        elif chosen_buff == 'Blessing of iron':
            self.max_hp += 40
            self.defense += 10
            self.damage += random.randint(10,20)
            self.dodge_chance -= 0.15
            print(f'You have gained large amounts of strength, but gotten much slower')
      
        elif chosen_buff == 'Blessing of the moon':
            self.b += 0.25
            self.damage += 30
            self.defense -= 10
            self.max_hp += 10
            self.dodge_chance += 0.05
            print(f'You are the one under the moon')
            
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

class Weapon ():
    
    def __init__(self,name,rarity,base_damage,room_level):
           self.name = name
           self.rarity = rarity 
           self.base_damage = base_damage
           self.room_level = room_level        
            
    def caculate_damage(self):
        rarity_multiplier = {
            'Common':  1.0,
            'Uncommon': 1.2,
            'Rare' : 1.5,
            'Epic' : 2.0,
            'Legendary' : 3.0
        }
        return int(self.base_damage*rarity_multiplier[self.rarity]*(1+self.room_level//10))
    
    def __str__(self):
        return  f"{self.name} ({self.rarity}) - Damage: {self.total_damage}"
    
    
    
class Chest():
    
    def __init__(self,room_level):
        self.room_level = room_level
        self.weapon = self.generate_random_weapon()
        self.potion = self.generate_random_potion()
        
    def generate_random_weapon(self):
        rarities  = ['Common','Uncommon','Rare',"Epic",'Legendary']
        rarity_weights = [50,30,15,4,1]
        chosen_rarity = random.choices(rarities, weights=rarity_weights, k=1)[0]
        
        weapon_names = {
            "Common": ["Rusty Sword", "Wooden Club","Wooden Sword"],
            "Uncommon": ["Iron Sword", "Steel Dagger",'Iron Staff'],
            "Rare": ["Elven Blade", "Orcish War Axe","Refined Longsword"],
            "Epic": ["Dragon Slayer", "Shadow Fang","Entangled Staff0"],
            "Legendary": ["Excalibur", "Godslayer","Demon's Lust"],
        }
        name = random.choice(weapon_names[chosen_rarity])
        base_damage = random.randint(5,20)
        return Weapon(name, chosen_rarity, base_damage, self.room_level)
        
    
           
class Enemy():
    def __init__(self, name, health, damage, defense):
        self.name = name
        self.health = health
        self.damage = damage
        self.defense = defense
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} has {self.health} HP remaining."
    