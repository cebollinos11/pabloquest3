from gameclass import *
from objects import *
from playercmd import *
import interface as i
import enchantments as en
import ai
import items
import random
import fov
import monsters

import maps
from image_gestor import *
from audio import PlaySound





def getfromreg(l):
    nl=[]
    for el in l:
        if el.name!='noname':
            nl.append(el)
    return random.choice(nl)

def d(maxi=100):
    if maxi<1: return 0
    if maxi==1: return 1
    return random.randint(1,maxi)
def get_objects_here(x,y):
    l=[]
    for el in DB.map[x][y].inv:
                    l.append(el)
    return l
def createnewplayer(self):    
    newchar=Player()
    newchar.inv=[items.retitem(0,0),items.retitem(0,0),items.Dagger(),items.HealingPotion()]
    newchar.inv = [items.HealingPotion()]

    #newchar.inv += [items.retitem(0,0),items.retitem(0,0),items.retitem(0,0),items.retitem(0,0),items.retitem(0,0)]
    

    for el in newchar.inv:
        try:
            prev = newchar.GetItemOnSlot(el.slot)
            if prev==None:
                el.on_equip(newchar,msg=0)
        except:pass
        
    newchar.updateimage()
    self.p=newchar

def generateitem(x,y):
    return items.retitem(x,y)

def put_in_tile(who,x,y):
    global DB
    DB.inv.append(who)
    if who.isFighter:
        DB.map[x][y].inv.append(who)
    else:
        DB.map[x][y].inv.insert(0,who)
    who.x,who.y=x,y
def remove_from_tile(who):
    global DB
    if who in DB.inv:  DB.inv.remove(who)
    if who in DB.map[who.x][who.y].inv: DB.map[who.x][who.y].inv.remove(who)
def distance(n,v):
    x,y=n
    i,j=v
    dx = x-i
    dy = y-j
    return math.sqrt(dx ** 2 + dy ** 2)
def isblocked(x,y):
    try:
        if DB.map[x][y].wall:
            return 1
    except:
        return 1

    for el in DB.inv:
        if el.blocks and el.x==x and el.y==y:
            return 1
    return 0

def getallenemies():
    tar=[]
    who=DB.p
    
    for el in DB.inv:
            if fov.fov_check(el.x,el.y):
                
                    if ai.is_enemy(who,el):
                        
                        tar.append(el)
    return tar
    
def getsingletarget(header,onlyfighters=0,fastenemy=0):
    
        obj=[]
        nam=[]
        
        for el in DB.inv:
            if fov.fov_check(el.x,el.y):
                if onlyfighters:
                    if el.isFighter:
                        nam.append(el.name)
                        obj.append(el)
                        

                else:
                    nam.append(el.name)
                    obj.append(el)

        if fastenemy:
            while DB.p in obj:
                obj.remove(DB.p)
                nam.remove(DB.p.name)
            
            if len(obj)==1:
                return obj[0]
            if len(obj)==0:
                return None
        key=i.menu(header,nam)
        
        try:
            return obj[key]
        except:
            return

def createEpicMap(self):
    #load map layout
    global map

    



    mapArr = DB.currentLoc.custom.layout
    
    map = fromArrayToMap(self,mapArr)  
    numroom=0
    self.map=map

    #place player

    

    #place enemies



    #special monsters 

    for y in range(MAP_HEIGHT):        
            for x in range(MAP_WIDTH):
                try:
                    if mapArr[y][x] == 6:
                            mon=monsters.retmonster(x,y,[DB.currentLoc.special_monsters[0]])
                            put_in_tile(mon,mon.x,mon.y)

                    if mapArr[y][x] == 7:
                        mon=items.retitem(x,y)                   
                        put_in_tile(mon,mon.x,mon.y)

                    if mapArr[y][x] == 8:
                            mon=monsters.retmonster(x,y,DB.currentLoc.monsters)
                            put_in_tile(mon,mon.x,mon.y)

                    if mapArr[y][x] == 9:            
                            self.exit=(x,y)
                            self.map[x][y]=maps.retTile("stairs")

                    if mapArr[y][x] == "p":
                            self.entrance=(x,y)
                    if mapArr[y][x] == "d":
                            mon=items.Dagger()    
                            mon.x=x
                            mon.y=y             
                            put_in_tile(mon,mon.x,mon.y)
                except:
                    pass
                    




        
    


    #place items

def fromArrayToMap(self,mapArr):
    map = [[ 0
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            try:
                if mapArr[y][x] == 2 or mapArr[y][x]==1 :
                    map[x][y]=maps.retTile("wall")
                if mapArr[y][x] != 2 and mapArr[y][x]!=1 :
                        map[x][y]=maps.retTile("floor")
                    
                        
                        if map[x][y-1].wall and map[x][y-1].door==None:
                            if 20>d():
                                if len(self.currentLoc.wall_decoration):
                                    deco=LI(random.choice(self.currentLoc.wall_decoration),1)
                                    map[x][y-1].image.blit(deco,(0,0))

                    
                if mapArr[y][x] == 4 :
                    map[x][y]=maps.retTile("door")
                if mapArr[y][x] == 5 :
                    map[x][y]=maps.retTile("secret door")

                

                    
            except:
                map[x][y]=maps.retTile("wall")


    return map

def generatemap(self,level):        
    size=200
    p_corr=10
    n_rooms=20
    numroom=0
    obj=[]
    
    
    while numroom<3:
        somename=dung_gen.dMap(MAP_WIDTH,MAP_HEIGHT)
        somename.makeMap(MAP_WIDTH,MAP_HEIGHT,size,p_corr,n_rooms) #prob corr, number rooms
        numroom=len(somename.roomList)
    map = fromArrayToMap(self,somename.mapArr);
    
    numroom=0

    self.map=map



    for element in somename.roomList:
        numroom+=1
        h=element[0]
        w=element[1]
        x=element[2]
        y=element[3]
        xcenter=int((2*x+w)/2)
        ycenter=int((2*y+h)/2)
        
        
        
        if numroom==1:#place player

            self.entrance=(xcenter,ycenter)
            
            
        else:
                
                            

                if d()<50:
                        x,y=get_random_free_tile()
                        
                        if isblocked(x,y)==0:
                            mon=items.retitem(x,y)                   
                        
                            put_in_tile(mon,mon.x,mon.y)
                            #self.inv.append(mon)

                if d()<50:
                        x,y=free_tile_away_from(self.entrance)
                        if isblocked(x,y)==0:
                            mon=monsters.retmonster(x,y,DB.currentLoc.monsters)
##                            self.inv.append(mon)
                            put_in_tile(mon,mon.x,mon.y)
                            
            
        if numroom==len(somename.roomList)-1:
            self.exit=(xcenter,ycenter)
            if DB.currentLoc.hasExit:
                self.map[xcenter][ycenter]=maps.retTile("stairs")
                
    #special monsters
    for el in DB.currentLoc.special_monsters:
        x,y=free_tile_away_from(self.entrance)
        if isblocked(x,y)==0:
            mon=monsters.retmonster(x,y,[el])
            put_in_tile(mon,mon.x,mon.y)
            
    return
def retCorpse(name,x,y):
    return items.Corpse(name,x,y)



def chosefrominv(header):
        PlaySound("inventory")
        lis=[]
        for el in DB.p.inv:
                
                    name=el.name
                    if el.isEquipped:
                        name+=' - on '+el.slot
                    if el.quivered:
                        name+='(quivered)'
                    
                    lis.append(name)
                                   

                
        key=i.menu(header,lis)

        try:
            return DB.p.inv[key]
            
        except:
            return None
def free_tile_away_from(cent):
    while 1:
        X,Y=get_random_free_tile()
        if distance((X,Y),cent)>8:
            return X,Y
            
def get_random_free_tile():
    while 1:
        x,y=d(MAP_WIDTH),d(MAP_HEIGHT)
        if isblocked(x,y)==0:
            return x,y
def get_closest_free_tile(X,Y):
    dis=999
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if isblocked(x,y)==0:
                if dis>distance((x,y),(X,Y)):
                    dis=distance((x,y),(X,Y))
                    good=x,y
    return good
            
def closetiles(coor):
        x,y=coor
        tiles=[]
        for j in range(3):
            for i in range(3):
                tiles.append((x+1-j,y+1-i))
        return tiles       



def new_game(self,newgame=0):
    i.init()

    PlaySound("tension")
    
    
    if newgame==0:    
        createnewplayer(self)
        self.locations=maps.Locations()
        self.currentLoc=self.locations.stages[0]()
        showhelp()
    self.inv=[]
##    self.inv.append(self.p)
    #generatemap(self,self.p.currentlevel)
    if self.currentLoc.duration == 1 and self.currentLoc.custom!=None:
        createEpicMap(self)
        
    else:
        generatemap(self,self.p.currentlevel)

    fov.new_fov(self.map)
    fov.fov_comp(self.entrance)
##    self.p.x,self.p.y=self.entrance

    put_in_tile(self.p,self.entrance[0],self.entrance[1])

    if self.currentLoc.duration == 1 and self.currentLoc.custom!=None:
        i.draw_game(DB)
        i.menu(DB.currentLoc.custom.message,[],noletter=1)
        

    playgame(self)
    

def playerturn(pl):
    if pl.computeFov:
                pl.computeFov=0
                fov.fov_comp((pl.x,pl.y))
                
    i.draw_game(DB)
    if DB.p.exp<1:
                DB.p.gainlevel()
                i.draw_game(DB)
    
    handlekeys(DB)




def computerturn(el):
    if el.ai:
        ai.take_turn(el)
    
def playgame(self):    
        while 1:
            
            for el in DB.inv:
                if DB.p.hp<1:
                    return
                if el.isFighter:
                    for ench in el.enchantments:
                        ench.execEnchantment(el)

                    if el.wait>0:
                        el.wait-=1
                    else:
                        
                        
                        if el!=self.p:
                            computerturn(el)
                        else:
                            while el.wait==0:
                                
                                playerturn(el)
                                

            
           
        
   


    

   





