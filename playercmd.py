import libtcodpy as libtcod
import interface as i
import main_functions as mf
import enchantments as en
from image_gestor import *
from audio import PlaySound
class cmd:
    def __init__(self,name,key,func):
        self.name=name
        self.key=key
        self.func=func

def look_around(self):
        ob=mf.getsingletarget("You see:")
        
        
def usestairs(game):    
        if game.map[game.p.x][game.p.y].stairs:

            # remove all enchantments
            for enchant in game.p.enchantments:
                enchant.loseEnchantment(game.p)

            #heal some hp
            game.p.heal(1)
            game.p.healmana(1)

            game.currentLoc.duration-=1
            if game.currentLoc.duration == 0:
                        game.locations.current+=1
                        game.currentLoc=game.locations.stages[game.locations.current]()
            mf.new_game(game,1)

def close_doors(self):
        tiles=mf.closetiles((self.p.x,self.p.y))
        for el in tiles:
            x,y=el
            d=self.map[x][y].door
            if d:
                if d.status=="open":
                    d.close()
                    self.p.wait+=2
                    
def pickupitem(self):
        l=mf.get_objects_here(self.p.x,self.p.y)#things under player
        l.remove(self.p)
        if len(l)==1:
            el=l[0]
        if len(l)>1:
            n=[]
            for el in l:
                if el.quivered:
                    n.append(el.name+'(quivered)')
                else:
                    n.append(el.name)
            key=i.menu("pick up what?",n)
            try:
                el=l[key]
            except:
                return
        if len(l)<1:
            self.p.walk( 0, 0)
            return
        if el.canpickup:
            PlaySound('pickup')
            el.pickup()
            self.p.wait+=2
            if "dagger" in el.name or "spear" in el.name:
                el.quivered=1;

            currEquipement = None
            if hasattr(el, 'slot'):
                currEquipement = self.p.GetItemOnSlot(el.slot)
            if currEquipement != None:

                c = currEquipement
                comp = ["Comparison with your "+currEquipement.name +":"]
                
                if el.maxhp-c.maxhp != 0:
                    comp.append("  Max HP "+str(el.maxhp-c.maxhp))
                if el.maxmana-c.maxmana != 0:
                    comp.append("  Max Mana "+str(el.maxmana-c.maxmana))
                if el.damage-c.damage != 0:
                    comp.append("  Damage "+str(el.damage-c.damage))
                if el.hit-c.hit != 0:
                    comp.append("  Hit bonus "+str(el.hit-c.hit))
                if el.defense-c.defense != 0:
                    comp.append("  Defense bonus "+str(el.defense-c.defense))
                if el.resis-c.resis != 0:
                    comp.append("  Damage Resistance " +str(el.resis-c.resis))
                if el.speed-c.speed != 0:
                    comp.append("  Speed "+str(-el.speed+c.speed))
                #if el.weight-c.weight != 0:
                #    comp.append("  Weight "+str(el.weight-c.weight))

                #if(currEquipement.name == el.name):
                 #   comp.append("No differences...")

                comp.append(" ")
                comp.append("Do you want to equip it?")

                shouldEquip = i.menu("You find a "+el.name,['yes','no'],0,comp)

                # = #i.menu("Do you want to equip "+el.name+'?',["yes",'no'])

                
                if(shouldEquip==0):

                    
                    currEquipement.on_unequip(self.p)
                    
                    el.on_equip(self.p)
                    el.quivered=0;
                    self.p.wait+=2

                    #drop old equip if is not a dagger or spear
                    if "dagger" in c.name or "spear" in c.name:
                        c.quivered = 1
                        i.s(c.name +" quivered.")
                    else:


                        c.x,c.y=self.p.x,self.p.y
                        self.p.inv.remove(c)
                        #objects.insert(0, self)
                        mf.put_in_tile(c,self.p.x,self.p.y)
                        i.s(c.name+" dropped.")
                else:
                    if "dagger" in el.name or "spear" in el.name or "sword" in el.name:
                        i.s("You put the "+ el.name+ " in your inventory.")
                    else:
                        el.x,el.y=self.p.x,self.p.y
                        self.p.inv.remove(el)
                        #objects.insert(0, self)
                        mf.put_in_tile(el,self.p.x,self.p.y)
                        i.s(el.name+" dropped.")


            else:
                if el.canequip:
                    el.on_equip(self.p)
                    el.quivered=0;
                    self.p.wait+=2

            self.p.updateimage()

                



            return


                             
                
        i.s("There is nothing to pick up!")
        return 1
    
def seeinv(self):
        it=mf.chosefrominv("What do you want to examine?")
        try:
            it.showdescription()
        except:
            pass
def quiveritems(self):
        it=mf.chosefrominv("What do you want to quiver?")
        if it:
            PlaySound("equip_item")
            if it.quivered:
                it.quivered=0
                i.s(it.name+' dequivered.')
            else:
                it.quivered=1
                i.s(it.name+' quivered.')

def firequivered(self):
    for el in self.p.inv:
        if el.quivered:
            throw(self,el)
            return
    i.s('Quiver something first!')
    


def throw(self,item=None):
    if item==None:        
        item=mf.chosefrominv("Throw what?")
    if item==None:
        return
    if item.isEquipped:
        item.on_unequip(self.p)
    tar=mf.getsingletarget("Choose target:",1,1)
    if tar==None:
        return
    i.s("You throw a "+item.name+" to "+tar.name+'!')
    PlaySound("throw")
    self.p.inv.remove(item)
    tarlist=[tar]
    
    if item.DestroyWhenThrown==0:
        item.x,item.y=tar.x,tar.y 
        mf.put_in_tile(item,item.x,item.y)
    else:
        PlaySound("glass")
        i.showhit(tar,None,LI('special/explo',1))
        for el in mf.closetiles((tar.x,tar.y)):
            
            for mon in self.map[el[0]][el[1]].inv:
                if mon.isFighter:
                    tarlist.append(mon)
        tarlist.remove(tar)

    for el in tarlist:
        item.ThrownEffect(el)
    self.p.wait+=self.p.speed+1
    self.p.updateimage()
    
def drop(self):
    item=mf.chosefrominv("drop what?")
    if item==None:
        return
    if item.isEquipped:
        item.on_unequip(self.p)
        self.p.updateimage()
    PlaySound("walking_on_item")
    item.x,item.y=self.p.x,self.p.y
    self.p.inv.remove(item)
    #objects.insert(0, self)
    mf.put_in_tile(item,self.p.x,self.p.y)
##    self.inv.insert(0,item)
    i.s('You drop a '+item.name)
    self.p.wait+=1

def drink(self):
    el=mf.chosefrominv("drink what?")
    if el!= None:
        if el.candrink:
            i.s('You drink a '+el.name+'.')
            el.drink(self.p)
            
            self.p.inv.remove(el)
            self.p.wait+=2
            return
    else:
        i.s('You can not drink that!')

def equip(self):
    item=mf.chosefrominv("Choose item to equip/use.")
    if item==None:
        return
    if item.canequip==0:
        el = item
        if el.candrink:
            i.s('You drink a '+el.name+'.')
            el.drink(self.p)
            
            self.p.inv.remove(el)
            self.p.wait+=2

        return
    prev = self.p.GetItemOnSlot(item.slot)
    if prev!=None:
        prev.on_unequip(self.p)
        if "dagger" in prev.name or "spear" in prev.name:
                prev.quivered=1;
    item.on_equip(self.p)
    item.quivered=0;
    self.p.wait+=2
    self.p.updateimage()

def unequip(self):
    item=mf.chosefrominv("Remove what?")
    if item==None:
        return
    if item.canequip==0:
        return
    if item.isEquipped==0:
        return
    
    item.on_unequip(self.p)
    self.p.wait+=2
    self.p.updateimage()
    
def castspell(self):
    PlaySound('prepare_magic')
    ss=[]
    for el in self.p.spells:
        ss.append(el.name+'('+str(el.manacost)+' mana)')
    cho=i.menu("which spell you want to cast?",ss)
    if cho==None:
        return
    self.p.spells[cho].cast(self.p)
def showhelp(foo=None):
    op=[' * Use arrows or numpad to move']
    for el in cmdlist:
        op.append('  '+el.key+' - '+el.name)    
    
    i.menu('List of commands:',op,noletter=1)

    op=[]
    op.append(' * Walk into a monster to attack it')
##    op.append(' * Some walls are secret doors')
    op.append(' * Potions and weapons can be thrown to monsters')
    op.append(' * Examine item bonuses with "i" command')
    op.append(' * Quiver items with "y" and fire them with "f"')
    op.append(' * Wait one turn with "5"')
    

    i.menu('Pro tips',op,noletter=1)
    
    
    return
cmdlist=[cmd('look around','l',look_around),         
         cmd('close door','c',close_doors),
         cmd('pick up items','SPACE',pickupitem),
         cmd('examine your inventory','i',seeinv),
         cmd('drink potion','q',drink),
         cmd('throw something','t',throw),
         cmd('equip items','e',equip),
         #cmd('take off items','r',unequip),
         cmd('drop items','d',drop),
         cmd('cast magic spell','z',castspell),
         cmd('quiver items to fire','y',quiveritems),
         cmd('fire quivered items','f',firequivered),
         cmd('climb stairs','ENTER',usestairs),
         cmd('show help','h',showhelp)]


    
def exitmenu(s):
    S=i.menu("",['Continue Game','Help','Quit Game'])
    if S==0:        
        return
    if S==1:
        showhelp()
        return
    elif S==2:
        s.p.hp=0
        s.p.wait=1
    else:
        exitmenu(s)
    
def handlekeys(self):    
    key_char = i.wait_for_letter()
    
##    if int(key.c)<0:
##        key_char=None
##    else:
##        key_char = chr(key.c)


    if key_char == '8':
        self.p.walk(0, -1)            
    elif  key_char == '2':
        self.p.walk( 0, 1)

    elif  key_char == '4':
        self.p.walk( -1, 0)

    elif  key_char == '6':
        self.p.walk( 1, 0)
    elif key_char=='5':            
        self.p.walk( 0, 0)            

    elif key_char == '1':
        self.p.walk( -1, +1)
    elif  key_char == '3':
        self.p.walk( 1, +1)
    elif  key_char == '7':
        self.p.walk( -1, -1)
    elif  key_char == '9':
        self.p.walk( 1, -1)

    elif key_char=='esc':
        exitmenu(self)

    #if key_char == 'v':
     #   self.p.gainlevel()
        
    for el in cmdlist:
        if el.key==key_char:            
            el.func(self)




