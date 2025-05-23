import libtcodpy as libtcod
from gameclass import *
import interface as i
import random
import math
import ai
import fov
import main_functions as mf
import spells as s
from image_gestor import *
from audio import PlaySound
from interface import d




class Object(object):
    icon = '?'
    color = libtcod.white
    
    original_black_color = libtcod.black
    back_color = original_black_color 
    name = 'noname'
    x,y=0,0
    blocks=0
    ai=0
    isFighter=0
    isPlayer=0
    canpickup=0

    image = iObject
    
        

    def distance_to(self, otherx,othery):
        #return the distance to another object
        dx = otherx - self.x
        dy = othery - self.y
        return math.sqrt(dx ** 2 + dy ** 2) 
        
    def walk(self,dx,dy):

        if self.isPlayer:
            
            if self.invsize<self.gettotalweigh():
                i.s('You are carrying a too much!')
                return
        
        x=self.x+dx
        y=self.y+dy

        
        
        if DB.map[x][y].wall:
            #SEE IF DOOR
            if DB.map[x][y].door:
                DB.map[x][y].door.open()
                i.s(self.name+' opens a door.')                
            return
        for el in DB.inv:
            if el.x==x and el.y==y and ai.is_enemy(self,el):
                self.attack(el)
                return
            if el.x==x and el.y==y and ai.is_enemy(self,el)==0 and el.isFighter==1:
                if self.isPlayer:
                    el.x=DB.p.x
                    el.y=DB.p.y
                    self.x=x
                    self.y=y
                    
                    self.computeFov=1
                    
                self.wait+=self.speed+1

        else:
            
            if self.isPlayer:
                    self.computeFov=1

                    if DB.map[x][y].stairs:
                        i.s("Press ENTER to use the stairs.")
                                           
                    

                    l=mf.get_objects_here(x,y)#things under player
                    if self in l: l.remove(self)
                    if len(l)==1:
                        PlaySound('walking_on_item')
                        i.s("A "+l[0].name+" lays in the ground.")
                    if len(l)>1:
                        PlaySound('walking_on_item')
                        i.s("There are "+str(len(l))+" items here.")
                    #if len(l)<1:
                    PlaySound('step'+str(d(9)));
##            self.x=x
##            self.y=y
            mf.remove_from_tile(self)
            mf.put_in_tile(self,x,y)
            
            self.wait+=self.speed




        
class Fighter(Object):
    defense=10
    maxhp=10
    hp=maxhp
    mana = 10
    maxmana=10
    damage=1
    resis=0
    hit=0    
    blocks=1
    isFighter=1
    level=1
    wait=0
    computeFov=0
    speed=4
    exp=10
    
    luck = 10
    def __init__(self):
        self.enchantments=[]

    def success_attack(self,tar):
        pass
    def meleeresponse(self,tar):
        pass
    def die(self):
                i.s(self.name+' dies!')
                
##            global DB
##            DB.inv.remove(self)
            
                DB.p.getexp(self.level)
                
                for el in range(self.level):
                    if mf.d()<15:
                        mf.put_in_tile(mf.generateitem(self.x,self.y),self.x,self.y)              
                mf.remove_from_tile(self)
        
    def attack(self,who):
        dice=i.d(20)+self.hit
        if dice<who.defense:            
##            i.s(self.name+' misses '+who.name+'!')
            PlaySound('miss')
            i.showhit(who,None,iMiss)
            
        else:
##            i.s(self.name+' hits '+who.name+'!')
            dmg=i.d(self.damage)
            #PlaySound('hit')
            if self.isPlayer:
                PlaySound("blade")
            #else:
            #    PlaySound('monster_bite')


            if who.receivedmg(dmg)==0:
                self.success_attack(who)
                who.meleeresponse(self)
                
            
        
        self.wait+=self.speed+2

    def getexp(self,exp):
        self.exp-=exp
        
    def gainlevel(self):
        self.level+=1
        
        self.exp=self.level*5

        PlaySound("levelup1")
        
        
        
        c=i.menu('CONGRATULATIONS! You have reached level '+str(self.level)+'!',
               ['+4 Health Points','+4 Mana Points','+3 Inventory slot','+1 Damage','+1 Hit Bonus','+1 Damage Resistance'])

        if c==0 or c==None:
            self.maxhp+=4            
            
        if c==1:
            self.maxmana+=4            
            
        if c==2:
            self.invsize+=3

        if c == 3:
            self.damage+=1

        if c == 4:
            self.hit+=1

        if c == 5:
            self.resis+=1

        PlaySound('levelup2')
        
    def heal(self,p):
        PlaySound('heal')
        self.hp+=p
        if self.hp>self.maxhp:
            self.hp=self.maxhp
        
        i.s(self.name+' is healed.')
        i.showhit(self,None,LI('special/healing',1))
    def healmana(self,p):
        self.mana+=p
        if self.mana>self.maxmana:
            self.mana=self.maxmana
        i.s(self.name+' looks more powerful.')
        
    def receivedmg(self,dmg,img=iHit):

        if self.isPlayer:
            PlaySound("human_get_hit")

        saved = mf.d(self.resis)
        dmg-=saved
        if dmg<1:dmg=1
        
        i.showhit(self,dmg,img)
        self.hp-=dmg
        if self.hp<1:
            self.die()

            return 1
        return 0
                

class Player(Fighter):
    
    isPlayer=1
    align = 'friend'
    icon = '@'
    name = 'Player'
    color = libtcod.white
    inv = []
    invsize = 20

    powers = []
    image=iPlayer.copy()



    currentlevel=1
    spells=[]

    
    for e in s.ALLSPELLS:
        spells.append(e())

    def sortInv(self):

        newinv = []
        eq = [] #equipped items (top)
        neq =[] #non equipped

        for el in self.inv:

            if el.isEquipped:
                
                eq.append(el)
            else:
                neq.append(el)


        newinv = eq+neq


        self.inv= newinv

    def die(self):
                PlaySound("human_die")
                i.s('You die!')
                i.draw_game(DB)
                i.menu("End game",["ok"])
                
                return                
            
        
    def gettotalweigh(self):
        w=0
        for el in self.inv:
            w+=el.weight
        return w
    def updateimage(self):
        self.image=iPlayer.copy()
        
        
        for el in ['footgear','body','head','right hand','left hand']:
            try:
                self.image.blit(self.GetItemOnSlot(el).image_eq,(0,0))
            except:
                pass
        
    def RechargeSpells(self):
        did=0
        for el in self.spells:
            if el.charged==0:
                el.charged=1
                did=1
        if did:
            i.s('The magic is recharget!')
    def GetItemOnSlot(self,slotname):
        for el in self.inv:
            if el.isEquipped and el.slot==slotname:
                return el
        return None
    
    







    
    
