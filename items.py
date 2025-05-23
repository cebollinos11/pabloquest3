import libtcodpy as libtcod
from gameclass import *
import interface as i
import ai
from objects import Object
import main_functions as mf
import random
import enchantments as en
import powers as p
from image_gestor import *
from audio import PlaySound

LOOTCNT=3

def d(maxi=100):
    if maxi<2:
        return 1
    return random.randint(1,maxi)
class Register(type):
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)        
        cls.ALL.append(cls)
        return cls

def normal_projectile(self,who):
    if d(20)+5>who.defense:
        i.s(who.name+' is hit!')
        who.receivedmg(d(self.projectileDmg))


class Item(Object):   
    candrink=0
    canequip=0
    canpickup = 1
    isEquipped=0
    DestroyWhenThrown = 0
    canbeenchanted = 0
    enchantments=0
    ThrownEffect=normal_projectile
    projectileDmg=1
    quivered=0
    weight=1
    def retEye(self):
        return iInvTreasure
    def pickup(self):
        DB.p.inv.append(self)
        mf.remove_from_tile(self)
        i.s("You pick up a "+self.name+".")        
        return 0
    def showdescription(self):
        i.menu("You dont know anything about this item",[],1)

class Equipable(Item,metaclass=Register):
    canequip=1
    ALL=[]    
    isEquipped=0
    hit=0
    maxhp=0
    damage=0
    defense=0
    
    speed=0
    luck=0
    maxmana=0
    resis=0
    originalname=""
    
    def __init__(self):
        self.powers=[]
        if d()<10:
            self.name='holy '+self.name
            self.defense+=1
            self.color=libtcod.white
        if d()<10:
            self.name='magic '+self.name
            self.maxmana=5
            self.color=libtcod.blue
        if d()<10:
            self.name='light '+self.name
            if self.speed>0:
                self.speed-=1
            
        if d()<10:
            self.name='runic '+self.name
            self.damage+=1
            self.color=libtcod.red
            
        self.originalname=self.name

        for el in range(d(LOOTCNT)):
            if d()<LOOTCNT*10:
                self.enchant()

    def get_description(self,d):
    
        if self.maxhp!=0:
            d.append("Health: "+str(self.maxhp))
        if self.maxmana!=0:
            d.append("Mana: "+str(self.maxmana))
        if self.damage!=0:
            d.append("Damage: "+str(self.damage))
        if self.hit!=0:
            d.append("Hit bonus: "+str(self.hit))

        if self.defense!=0:
            d.append("Defense bonus: "+str(self.defense))
        if self.resis!=0:
            d.append("Resistance bonus: "+str(self.resis))
        
        if self.speed!=0:
            d.append("Speed: "+str(-self.speed))

        d.append('Weight: '+str(self.weight))

        for el in self.powers:
            d.append("Magic Power: "+el.name)

        
    
    

    def showdescription(self):
        d=[]
        if self.maxhp!=0:
            d.append("Health: "+str(self.maxhp))
        if self.maxmana!=0:
            d.append("Mana: "+str(self.maxmana))
        if self.damage!=0:
            d.append("Damage: "+str(self.damage))
        if self.hit!=0:
            d.append("Hit bonus: "+str(self.hit))

        if self.defense!=0:
            d.append("Defense bonus: "+str(self.defense))
        if self.resis!=0:
            d.append("Resistance bonus: "+str(self.resis))
        
        if self.speed!=0:
            d.append("Speed: "+str(self.speed))

        d.append('Weight: '+str(self.weight))

        for el in self.powers:
            d.append("Magic Power: "+el.name)
        i.menu("Description of "+self.name,d,1)
        
    def enchant(self):
        pass
        
    def on_equip(self,who,msg=1):
        quivered = 0;
        PlaySound('equip_item')
        who.maxhp+=self.maxhp
        who.damage+=self.damage
        who.defense+=self.defense
        who.hit+=self.hit
        who.luck+=self.luck
        
        who.speed+=self.speed
        who.resis+=self.resis

        if(self.speed or self.hit):
            PlaySound('equip_jewel')

        if(self.defense):
            PlaySound('holy')
        
        who.maxmana+=self.maxmana
        if who.maxmana<who.mana:
            who.mana=who.maxmana
        for el in self.powers:
            who.powers.append(el)
        if msg:
            i.s(who.name+' equips '+self.name+' on '+self.slot+'.' )
        self.isEquipped=1

    def on_unequip(self,who,showmsg=1):
        who.maxhp-=self.maxhp
        if who.hp>who.maxhp:
            who.hp=who.maxhp
        who.maxmana-=self.maxmana
        if who.mana>who.maxmana:
            who.mana=who.maxmana
        if who.mana<1:
            who.mana=0
        who.damage-=self.damage
        who.resis-=self.resis
        who.defense-=self.defense
        who.hit-=self.hit
        who.luck-=self.luck
        who.speed-=self.speed
        
        for el in self.powers:
            for le in who.powers:
                if le==el:
                    who.powers.remove(le)
                    break
        if showmsg:
            i.s(who.name+' removes '+self.name+'.' )
        self.isEquipped=0


    

class Helmet(Equipable):
    
    icon='^'
    color=libtcod.grey
    name='helm'
    slot="head"
    maxhp=2
    image=iHelm
    image_eq=iHelmEq

    def __init__(self):
        Equipable.__init__(self)

    def enchant(self):        
        self.enchantments+=1        
        self.maxhp+=1
        self.name=self.originalname+' +'+str(self.enchantments)

class BodyArmor(Equipable):
    icon='['
    slot='body'
    image=iArmor
    image_eq=iTunicEq

    def __init__(self):
        Equipable.__init__(self)
        

    def enchant(self):        
        self.enchantments+=1 
        self.resis+=1
        self.name=self.originalname+' +'+str(self.enchantments)
        if self.enchantments == 3:
            self.defense+=1
        
class Robe(BodyArmor):    
    color=libtcod.dark_green
    name='tunic'    
    resis=1
    image_eq=iTunicEq
    maxmana=1
    

class LArmor(BodyArmor):    
    color=libtcod.darker_green
    name='leather armor'    
    resis=2
    weight=2    
    
    
    
    image_eq=iLarmorEq

class HArmor(BodyArmor):
    color=libtcod.dark_grey
    name='metal armor'
    image_eq=iMarmorEq
    resis=5
    speed=1    
    weight=5
    maxmana=-2
    
    
class Jewelry(Equipable):
    image=iAmulet
    def __init__(self):
        self.powers=[]
        c=random.choice(['fury','speed','mana','protection'])
        
        

        if c=='protection':
            self.name=self.name+' of protection'
            self.defense+=1
            self.resis+=2 
        

        

        if c == 'fury':
            self.name=self.name+' of fury'
            self.hit+=2
            self.damage+=2
            self.color=libtcod.red

        if c == 'speed':
            self.name=self.name+' of speed'
            self.speed-=1
            
            self.color=libtcod.light_blue
            
        if c=='mana':
            self.name=self.name+' of mana'
            self.color=libtcod.blue
            self.maxmana=5
        
        
        

            
class Ring(Jewelry):    
    icon='='
    name='ring'
    slot='finger'
    def __init__(self):
        Jewelry.__init__(self)
        
class Amulet(Jewelry):
    icon='"'
    slot='neck'
    name='amulet'
    def __init__(self):
        Jewelry.__init__(self)
    
    
class FootGear(Equipable):
    image=iBoots
    icon=':'
    color=libtcod.green
    slot='footgear'
    image_eq=iBootsEq
    
    def __init__(self):
        Equipable.__init__(self)
               

        if d()<10:
            self.name='winged '+self.name
            
            self.speed-=1

        if d()<10:
            self.name='reforced '+self.name
            self.maxhp+=2

    def enchant(self):        
        self.enchantments+=1        
        self.maxhp+=1
        self.name=self.originalname+' +'+str(self.enchantments)
    
    
class Boots(FootGear):
    name='pair of boots'
    maxhp=2

class Sandals(FootGear):
    name='pair of sandals'
    maxhp=1
    color=libtcod.light_green
    
class Shield(Equipable):
    image=iShield
    image_eq=iShieldEq
    icon='{'
    color=libtcod.grey
    slot='left hand'
    maxmana=-1
    def __init__(self):
        Equipable.__init__(self)


    def enchant(self):        
        self.enchantments+=1        
        self.defense+=1
        self.name=self.originalname+' +'+str(self.enchantments)
    

class SmallShield(Shield):
    name='small shield'
    defense=1
class BigShield(Shield):
    name='big shield'
    defense=2
    speed=1
    weight=2
    image_eq=iBShieldEq

    
class Weapon(Equipable):
    icon='('
    color=libtcod.grey
    slot='right hand'
    canbeenchanted=1
    image_eq=iDaggerEq
    def __init__(self):
        Equipable.__init__(self)

    def enchant(self):        
        self.enchantments+=1        
        self.damage+=1
        self.name=self.originalname+' +'+str(self.enchantments)
            

class Dagger(Weapon):
    image=iDagger
    name='dagger'
    damage=2
    projectileDmg=4
    speed=-1
    quivered = 1

    
class Sword(Weapon):
    image=iSword
    name='sword'
    image_eq=iSwordEq
    damage=5
    

class Spear(Weapon):
    icon='/'
    image=iSpear
    image_eq=iSpearEq
    name='spear'
    damage=7
    projectileDmg=6
    speed=1
    weight=4
    quivered = 1

class Corpse(Item):
    def __init__(self,name,x,y):
        self.name=name+' corpse'
        self.x,self.y=x,y
        self.icon='%'
        self.color=libtcod.red

        


    

    
class Potion(Item,metaclass=Register):
    ALL=[]    
    candrink=1
    icon='!'
    DestroyWhenThrown=1
    image = iPotion
    weight = 0.5
    
    enchantments = 0
    drink_effect=None
    def __init__(self):
        self.ThrownEffect=self.drink
        self.originalname=self.name

        
        for el in range(d(LOOTCNT)):
            if d()<LOOTCNT*10:
                self.enchant()

    def drink(self,who):
        PlaySound("drink")
        for el in range(self.enchantments+1):
                        self.drink_effect(who)

    def enchant(self):        
        self.enchantments+=1        
##        self.maxhp+=1
        self.name=self.originalname+' +'+str(self.enchantments)

            


def potion_heal(self,who):
    who.heal(d(15))
def potion_teleport(self,who):
    x,y=mf.free_tile_away_from((who.x,who.y))
    mf.remove_from_tile(who)
    mf.put_in_tile(who,x,y)
    PlaySound("teleport")
    i.s(who.name+' is teleported!')
    who.computeFov=1
def potion_fire(self,who):
##    i.s(who.name+' er braendt!')
##    en.CatchOnFire().getEnchantment(who)
    who.receivedmg(5,LI('special/fire_hit',1))
    PlaySound('fire')

def potion_weak(self,who):
    en.Weaken().getEnchantment(who)

def potion_Levelup(self,who):
    who.getexp(d(15))
def potion_Paralyce(self,who):
    en.Paralyzed().getEnchantment(who)

class RagePotion(Potion):
    name = 'potion of rage'
    image = iPotionRage
    def drink_effect(self,who):
        en.Enraged().getEnchantment(who)
    
class ManaPotion(Potion):
    color=libtcod.light_blue
    name = 'mana potion'
    image=iPotionMana
    
    def drink_effect(self,who):
        if who==DB.p:
            who.healmana(d(15))
    
class HealingPotion(Potion):
    color=libtcod.blue
    drink_effect=potion_heal
    name="healing potion"
    image=iPotionHealth

class FirePotion(Potion):
    image = iPotionFire
    color=libtcod.red
    drink_effect=potion_fire
    name="potion of fire"

class WeaknessPotion(Potion):
    color=libtcod.white
    drink_effect=potion_weak
    name='potion of weakness'
class TeleportPotion(Potion):
    color=libtcod.light_green
    drink_effect=potion_teleport
    name="potion of teleport"
    image = iPotionTeleport

class LevelPotion(Potion):
    image = iPotionKnowledge
    color=libtcod.orange
    drink_effect=potion_Levelup
    name="potion of knowledge"

class ParalycePotion(Potion):
    image=iPotionParalize
    color=libtcod.yellow
    drink_effect=potion_Paralyce
    name='potion of paralysis'
    





def retitem(x,y):
    package=random.choice([Equipable,Equipable,Potion])
    e=mf.getfromreg(package.ALL)()
    #e= HArmor()
    e.x=x
    e.y=y
    return e
    
    
