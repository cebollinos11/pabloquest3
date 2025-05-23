import libtcodpy as libtcod
from gameclass import *
import textwrap
import fov
import powers as p
import pygame, random
from pygame.locals import *
from audio import PlaySound




##SCREEN_WIDTH = 80
##SCREEN_HEIGHT = 24

FONT_Y=16

GAME_SCREEN_TILES_X=18
GAME_SCREEN_TILES_Y=13

TILESIZE=32
UIWIDTH = 300

SCRW=GAME_SCREEN_TILES_X * TILESIZE  + UIWIDTH
SCRH=(GAME_SCREEN_TILES_Y) * TILESIZE + TILESIZE/2

pygame.init()
##libtcod.console_set_custom_font('terminal.png',libtcod.FONT_LAYOUT_ASCII_INROW)
##print libtcod.console_init_root(20, 20, 'Danish adventures', False)

#screen = pygame.display.set_mode((SCRW,SCRH),pygame.FULLSCREEN )
screen = pygame.display.set_mode((SCRW,SCRH) )
font=pygame.font.Font("font.ttf", FONT_Y)
fontbig=pygame.font.Font("font.ttf", FONT_Y*2)
pygame.display.set_caption("PabloQuest")
#font=pygame.font.SysFont("courier", FONT_Y,bold=0) #courier,monospace,arial

pygame.key.set_repeat(500,100)


messages=""
oldmsg=[]
def init():
    messages=""
    oldmsg=[]
def s(text):
    global messages
    messages+=text+' '
def d(maxi=100):
    if maxi<2:
        return 1
    return random.randint(1,maxi)
def speed2word(s):
    if s<2: return 'Very fast'
    if s<3: return 'Fast'
    if s<4: return 'Quick'
    if s <5: return 'Normal'
    if s <6: return 'Slow'
    
    return 'very slow'

def imagewcaption(imagename,caption,wait=1):
    img=pygame.image.load('images/'+imagename+'.png').convert()
    scaled=pygame.transform.scale(img, (SCRW,SCRH))   
    
    screen.blit(scaled,scaled.get_rect())

##    text = font.render(caption,0,(0,0,0))
##    screen.blit(text,text.get_rect())
##    text = font.render(caption,0,(255,255,255),(0,0,0))
##    screen.blit(text,(1,1))
    
    pygame.display.update(pygame.Rect(0, 0, SCRW, SCRH))
    global messages
    messages = caption
    
    if wait:
        pygame.time.delay(500)
        draw_msg()
        wait_for_letter()
    else:
        text = font.render(caption,0,(255,255,255),(0,0,0))
        screen.blit(text,(1,1))
        
        
    


def draw_hud(g):
    img=pygame.image.load('images/special/hud.png').convert()
##    img.set_colorkey(img.get_at((0,0)))
    things=[str(g.p.hp)+'/'+str(g.p.maxhp),
            str(g.p.mana)+'/'+str(g.p.maxmana),
            '1d'+str(g.p.damage)+'+'+str(g.p.hit),
            str(g.p.defense)+'('+str(g.p.resis)+')  Speed: '+speed2word(g.p.speed)]
            
    i=25
    for el in things:        
        img.blit(font.render(el,1, (255, 255, 255)),(i,0))
        i+=85
    screen.blit(img,(0,GAME_SCREEN_TILES_Y*TILESIZE))
    pygame.display.update(pygame.Rect(0, (GAME_SCREEN_TILES_Y)*TILESIZE, GAME_SCREEN_TILES_X*TILESIZE, TILESIZE/2))








##def draw_hud1(g):
##      
##        height=1     
##        
##        hud=""
##        
##        hud+=' HP:'+str(g.p.hp)+'/'+str(g.p.maxhp)+' MP:'+str(g.p.mana)+'/'+str(g.p.maxmana)
##        hud+=' 1d'+str(g.p.damage)+'+'+str(g.p.hit)
##        hud+=' AC:'+str(g.p.defense)+'('+str(g.p.resis)+')'
##        hud+=' S:'+speed2word(g.p.speed)
##        hud+=' Lvl:'+str(g.p.level)+'               '
##
##
##        if g.p.hp<5:
##            
##            text = font.render(hud,1, (255, 0, 0))
##        else:
##            text = font.render(hud,1, (255, 255, 255))
##
##        textpos = text.get_rect()
##        textpos.left=0
##        textpos.top=GAME_SCREEN_TILES_Y*TILESIZE
##        back=text.copy()
##        
##        back.fill((0,0,0))
##        back.blit(text,(0,0) )
##        screen.blit(back,textpos )
##        
##        pygame.display.update(pygame.Rect(0, (GAME_SCREEN_TILES_Y)*TILESIZE, GAME_SCREEN_TILES_X*TILESIZE, FONT_Y))



def showhit(who,dmg,damage_img):
    pic_rec=damage_img.get_rect()
    relx,rely=who.x-DB.p.x+GAME_SCREEN_TILES_X/2,who.y-DB.p.y+GAME_SCREEN_TILES_Y/2
    screen.blit(damage_img,((relx)*TILESIZE+TILESIZE/2-pic_rec.width/2,(rely)*TILESIZE+TILESIZE/2-pic_rec.height/2))
    txt=" "
    if dmg!=None:
        txt=str(dmg)
        text = font.render(txt,1, (255, 255, 255), (255,0,0))
        screen.blit(text,((relx+0.3)*TILESIZE,(rely+0.3)*TILESIZE))
    pygame.display.update(pygame.Rect((relx)*TILESIZE+TILESIZE/2-pic_rec.width/2,(rely)*TILESIZE+TILESIZE/2-pic_rec.height/2, pic_rec.width, pic_rec.height))
    pygame.time.delay(250)
    
    
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext
def draw_msg():
    global messages
    if messages=="":
                return
    y=0
##    print SCRW,len(wrapline(messages,font,SCRW))*FONT_Y
    temporal=pygame.Surface((SCRW-UIWIDTH,len(wrapline(messages,font,SCRW-UIWIDTH))*FONT_Y))
    for line in wrapline(messages,font,SCRW-UIWIDTH):
        text = font.render(line,1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.left=0
        textpos.top=y
        temporal.blit(text,textpos )
        y+=FONT_Y
    messages=""
    screen.blit(temporal,(0,0))
    pygame.display.update(pygame.Rect(0, 0, SCRW-UIWIDTH, y+10))


paperdoll = pygame.image.load("images/special/paperdoll.png").convert()
paperdoll2 = pygame.image.load("images/special/paperdoll2.png").convert()
paperdollred = pygame.image.load("images/special/paperdoll_red.png").convert()

def draw_new_hud():
    
    DB.p.sortInv()
    

    C_NORMAL = (50, 50,50)
    C_EQ = (1,2,225)

    uiText = []

    for el in DB.p.inv:
                    color = C_NORMAL 
                    
                    if el.isEquipped:
                        color = C_EQ
                        #name+=' - on '+el.slot
                    uiText.append([el.name.capitalize(),color])
    
    y=45
##    print SCRW,len(wrapline(messages,font,SCRW))*FONT_Y
    
    temporal = paperdoll
    if(DB.p.hp<5):
        temporal=paperdollred


    temporal=pygame.transform.scale(temporal, (UIWIDTH,SCRH))  

    
    
    #dye red
    if(DB.p.hp<5):
        #temporal = colorize(temporal,(255,0,0))
        #add Danger sign stones
        text = font.render("DANGER - LOW HP",1,(1,1,1))
        textpos = text.get_rect()
        textpos.left=80
        textpos.top=10
        temporal.blit(text,textpos )



    
    #temporal=pygame.Surface((SCRW,SCRH))
    for line in uiText:
        print(line)
        text = font.render(line[0],1,line[1])
        textpos = text.get_rect()
        textpos.left=40
        textpos.top=y
        temporal.blit(text,textpos )
        y+=FONT_Y

    #add stones
    text = font.render("Stones " +str(DB.p.gettotalweigh() )+"/"+str(DB.p.invsize),1,(1,1,1))
    textpos = text.get_rect()
    textpos.left=40
    textpos.top=400
    temporal.blit(text,textpos )

    uiText=""
    screen.blit(temporal,(SCRW-UIWIDTH,0))
    pygame.display.update(pygame.Rect(0, 0, SCRW, SCRH))

def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    #image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image
    

def draw_game(self,drawmsg = 1):
    #draw terrain       
    
##    window = libtcod.console_new(MAP_WIDTH,MAP_HEIGHT)
    temporal = pygame.Surface((GAME_SCREEN_TILES_X*TILESIZE,GAME_SCREEN_TILES_Y*TILESIZE))
    
    ma=self.map
    temporal.fill((0,0,0))
    
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):                   

                if abs(x-self.p.x)<=GAME_SCREEN_TILES_X/2 and abs(y-self.p.y)<=GAME_SCREEN_TILES_Y/2 and x-self.p.x+GAME_SCREEN_TILES_X/2>-1 and y-self.p.y+GAME_SCREEN_TILES_Y/2>-1:
                    relx=x-self.p.x+GAME_SCREEN_TILES_X/2
                    rely=y-self.p.y+GAME_SCREEN_TILES_Y/2            

                    if fov.fov_check(x,y):#is in fov
                            ma[x][y].explored=1
                            
                            temporal.blit(ma[x][y].image,(relx*TILESIZE,rely*TILESIZE))                          
                            
                                
                    elif ma[x][y].explored==1 or p.MapEye in self.p.powers:

                        ma[x][y].image.set_alpha(100)
                        temporal.blit(ma[x][y].image,(relx*TILESIZE,rely*TILESIZE))
                        ma[x][y].image.set_alpha(255)

                        
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):                   

                if abs(x-self.p.x)<=GAME_SCREEN_TILES_X/2 and abs(y-self.p.y)<=GAME_SCREEN_TILES_Y/2 and x-self.p.x+GAME_SCREEN_TILES_X/2>-1 and y-self.p.y+GAME_SCREEN_TILES_Y/2>-1:
                    relx=x-self.p.x+GAME_SCREEN_TILES_X/2
                    rely=y-self.p.y+GAME_SCREEN_TILES_Y/2            
                      
                 
                    for el in ma[x][y].inv:
                                #draw items, fighters...
                        if fov.fov_check(x,y):
                            v,w=el.image.get_size()        
                            temporal.blit(el.image,((relx)*TILESIZE-(v/2-TILESIZE/2),
                                    (rely)*TILESIZE-w+TILESIZE)) 

                        else:
                            if el.isFighter==0 and p.ItemEye in self.p.powers:
                            
                                v,w=el.retEye().get_size()        
                                temporal.blit(el.retEye(),((relx)*TILESIZE-(v/2-TILESIZE/2),
                                        (rely)*TILESIZE-w+TILESIZE))
                            if el.isFighter and p.MonsterEye in self.p.powers:
                                v,w=el.retEye().get_size()        
                                temporal.blit(el.retEye()   ,((relx)*TILESIZE-(v/2-TILESIZE/2),
                                        (rely)*TILESIZE-w+TILESIZE)) 
                                
                            
            
        

    screen.blit(temporal,(0,0))
    pygame.display.update(pygame.Rect(0, 0, GAME_SCREEN_TILES_X*TILESIZE, GAME_SCREEN_TILES_Y*TILESIZE))

    if drawmsg:
        draw_msg()
    draw_new_hud()
    draw_hud(self)




	
def menu(header,options=None,noletter=0,extraHeader=[]):
    size=15   
    if options==None or len(options)<1:
        return menu(header,[''],noletter=1)        
    lists=chunks(options,size)    
    i=0
    for el in lists:
            if len(options)/size+1 == 1:
                ret=menu_graphic(header,el,noletter,extraHeader)
            else:
                
                ret=menu_graphic(header+' '+str(i+1)+'/'+str(len(options)/size+1),el,noletter,extraHeader)
            if ret=='escape':
                    return None
            if ret=='next':
                    i+=1
            else:
                k=ret+i*size
                
                return k
    return menu(header,options,noletter,extraHeader)       

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]
                


def menu_graphic(header,options,noletter,extraHeader = []):
    #print header

    OFFSET = 100
    heightheader=len(wrapline(messages,font,SCRW-UIWIDTH-2))    
    temporal = paperdoll2
    #temporal = pygame.Surface((SCRW-UIWIDTH,(len(options)+heightheader)*FONT_Y+30))
    temporal=pygame.transform.scale(temporal, (SCRW-UIWIDTH,((len(options)+2)+heightheader+len(extraHeader)/2)*FONT_Y+30+OFFSET))  
    #pygame.draw.rect(temporal, (100,100,100), temporal.get_rect(),10)
    

    ###
    y=50

    
    for line in wrapline(header,font,SCRW-UIWIDTH-200):
        text = font.render(line,1, (0,0,200))
        textpos = text.get_rect()
        textpos.left=15+temporal.get_rect().width*0.14
        textpos.top=y
        temporal.blit(text,textpos )
        y+=FONT_Y

    if(len(extraHeader)>0):
        for line in extraHeader:
            text=line
            text = font.render(text,1, (1,1,1))
            textpos = text.get_rect()
            textpos.left=15+temporal.get_rect().width*0.12
            textpos.top=y+textpos.height*0.05
            temporal.blit(text,textpos )
            y+=FONT_Y

    
    
    #print options
    
    letter_index=ord('a')
    for line in options:
        text=""
        if noletter==0:
                text = '' + chr(letter_index) + ') '
                letter_index+=1
        text+= line.capitalize()
        text = font.render(text,1, (1,1,1))
        textpos = text.get_rect()
        textpos.left=15+temporal.get_rect().width*0.12
        textpos.top=y+textpos.height*0.05
        temporal.blit(text,textpos )
        y+=FONT_Y
    original_back = screen.copy()
    screen.blit(temporal,(UIWIDTH/2,SCRH/2-temporal.get_rect().height/2))
    pygame.display.update(pygame.Rect(0, 0, SCRW, SCRH))
##    pygame.display.update(pygame.Rect(0, 0, GAME_SCREEN_TILES_X*TILESIZE, TILESIZE))


    #wait for answer
    key = wait_for_letter()

    
    pygame.display.update(pygame.Rect(0, 0, SCRW, y+100))

    screen.blit(original_back,(0,0))
    pygame.display.update(pygame.Rect(0, 0, SCRW, SCRH))
    #convert the ASCII code to an index; if it corresponds to an option, return it

    if key == 'esc' or noletter==1:
        
        return 'escape'
    try:     
        index = ord(key) - ord('a')
    except:
        index = 0
    if index >= 0 and index < len(options): return index
    return 'next'

def wait_for_letter():
    done = False
    while not done:
        for event in pygame.event.get():            
            if (event.type == KEYDOWN):                    
                    if (event.key==K_DOWN): return '2'
                    elif (event.key==K_UP): return '8'                   
                    elif (event.key==K_RIGHT):  return '6'                  
                    elif (event.key==K_LEFT): return '4'                   
                    elif (event.key == K_ESCAPE):return 'esc'
                    elif (event.key == K_RETURN):return 'ENTER'
                    elif (event.key == K_SPACE):return 'SPACE'
                    elif event.key == K_a : return 'a'  
                    elif event.key == K_b : return 'b'  
                    elif event.key == K_c : return 'c'  
                    elif event.key == K_d : return 'd'  
                    elif event.key == K_e : return 'e'  
                    elif event.key == K_f : return 'f'  
                    elif event.key == K_g : return 'g' 
                    elif event.key == K_h : return 'h'  
                    elif event.key == K_i : return 'i'  
                    elif event.key == K_j : return 'j'  
                    elif event.key == K_k : return 'k'  
                    elif event.key == K_l : return 'l'  
                    elif event.key == K_m : return 'm'  
                    elif event.key == K_n : return 'n'  
                    elif event.key == K_o : return 'o'  
                    elif event.key == K_p : return 'p'  
                    elif event.key == K_q : return 'q'  
                    elif event.key == K_r : return 'r'  
                    elif event.key == K_s : return 's'  
                    elif event.key == K_t : return 't'  
                    elif event.key == K_u : return 'u'  
                    elif event.key == K_v : return 'v'  
                    elif event.key == K_w : return 'w'  
                    elif event.key == K_x : return 'x'  
                    elif event.key == K_y : return 'y'  
                    elif event.key == K_z : return 'z'  
                    elif event.key == K_0 : return '0'  
                    elif event.key == K_1 : return '1'  
                    elif event.key == K_2 : return '2'  
                    elif event.key == K_3 : return '3'  
                    elif event.key == K_4 : return '4'  
                    elif event.key == K_5 : return '5'  
                    elif event.key == K_6 : return '6'  
                    elif event.key == K_7 : return '7'  
                    elif event.key == K_8 : return '8'  
                    elif event.key == K_9 : return '9'
                    elif event.key == K_KP1 : return '1'  
                    elif event.key == K_KP2 : return '2'  
                    elif event.key == K_KP3 : return '3'  
                    elif event.key == K_KP4 : return '4'  
                    elif event.key == K_KP5 : return '5'  
                    elif event.key == K_KP6 : return '6'  
                    elif event.key == K_KP7 : return '7'  
                    elif event.key == K_KP8 : return '8'  
                    elif event.key == K_KP9 : return '9'
                    elif event.key == K_LESS : return '<'
                    return '>'
                

