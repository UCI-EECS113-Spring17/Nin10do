import pygame
from pynq import Overlay
from pynq.iop import Pmod_JYSK
from pynq.iop import PMODA
# Download bitstream
Overlay("base.bit").download()
from pynq.drivers.video import HDMI
from PIL import Image
import time
from pynq.board import Button
from pynq.board import Switch
from pynq import Map
from pynq import Box
from pynq import Player
from pynq import Wall
from pynq import Dot


MAX_SWITCHES = 2
MAX_BUTTONS = 4
switches = [0] * MAX_SWITCHES
buttons = [0] * MAX_BUTTONS
for i in range(MAX_BUTTONS):
    buttons[i] = Button(i)
for i in range(MAX_SWITCHES):
    switches[i] = Switch(i)
    
pygame.init()

display_width = 640
display_height = 480

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Nin10do test')
clock = pygame.time.Clock()

playerimg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/player.png')
wallimg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/wall.png')
boximg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/box.png')
dotimg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/dot.png')
stopimg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/stop.png')
winimg = pygame.image.load('/home/xilinx/jupyter_notebooks/Getting_Started/images/win.png')

lvl = 1
#curmap = Map().get_lvl(lvl-1)
curmap = Map()
boxes = []
walls = []
dots = []
player = Player(0,0)

#joystick
jysk = Pmod_JYSK(PMODA)

def read_jysk():
    i = 0
    upcount = 0
    downcount = 0
    first = 0
    while True:
        tmp = jysk.read()
        if tmp>=120 and tmp<=130:
            downcount=downcount+1
            if first==0:
                first = -1
        elif tmp>=160 and tmp<=170:
            upcount=downcount+1
            if first==0:
                first = 1
        time.sleep(0.05)
        i=i+1
        if i==20:
            if downcount==upcount:
                if downcount==0:
                    print("nothing")
                    return 0
                else:
                    print(first)
                    return first
            elif downcount>upcount:
                print("down")
                return -1
            else:
                print("up")
                return 1


def gather(lvl):
    print("gathering")
    for i in range(12):
        for j in range(16):
            if curmap.detail[lvl-1][i][j]==1:
                walls.append(Wall(j*40,i*40))
            elif curmap.detail[lvl-1][i][j]==2:
                boxes.append(Box(j*40,i*40))
            elif curmap.detail[lvl-1][i][j]==3:
                dots.append(Dot(j*40,i*40))
            elif curmap.detail[lvl-1][i][j]==4:
                player.set_x(j*40)
                player.set_y(i*40)
        

def draw_player(x,y):
    gameDisplay.blit(playerimg,(x,y))
def draw_wall(x,y):
    gameDisplay.blit(wallimg,(x,y))
def draw_box(x,y):
    gameDisplay.blit(boximg,(x,y))
def draw_dot(x,y):
    gameDisplay.blit(dotimg,(x,y))
    
def check_box(x,y,x_move,y_move):
    if x+x_move>560 or x+x_move<40 or y+y_move>400 or y+y_move<40:
        return 9 #hit boundery
    for i in range(len(walls)):
        if walls[i].get_x()==x+x_move*2 and walls[i].get_y()==y+y_move*2:
            return 8 #hit wall
    return 1 #permission granted
    
#movement permission
def check_player(x,y,x_move,y_move):
    if x+x_move>600 or x+x_move<0 or y+y_move>440 or y+y_move<0:
        return 9 #hit boundery
    for i in range(len(walls)):
        if walls[i].get_x()==x+x_move and walls[i].get_y()==y+y_move:
            return 8 #hit wall
    for i in range(len(boxes)):
        if boxes[i].get_x()==x+x_move and boxes[i].get_y()==y+y_move:
            if boxes[i].get_can_move()==0:
                return 11 #box fixed with a dot
            if check_box(x,y,x_move,y_move)==1:
                boxes[i].set_x(x+x_move*2)
                boxes[i].set_y(y+y_move*2)
                return 0
            return 10
    return 0 #permission granted

def check_dot():
    for i in range(len(dots)):
        for j in range(len(boxes)):
            if boxes[j].get_can_move()==1 and dots[i].get_x()==boxes[j].get_x() and dots[i].get_y()==boxes[j].get_y() and dots[i].get_occupied()==0:
                boxes[j].set_can_move(0)
                dots[i].set_occupied(1)
    for i in range(len(dots)):
        if dots[i].get_occupied()==0:
            return 0
    return 1
                
    
x_move = 0
y_move = 0
k = 0
nothing = 0
tmp = 0
start = 1
gotonext = 0
illegal = 0
over = 0

crashed = False

# Initialize HDMI as an input device
hdmi_out = HDMI('out')
hdmi_out.mode(0)
hdmi_out.start()

while not crashed:
    
    print("waiting")
    while True:
        if buttons[0].read():
            readval = read_jysk()
            if readval==0:
                x_move = 0
            elif readval==1:
                x_move = -40 #left
            else:
                x_move = 40 #right
            break
            
        if buttons[1].read():
            readval = read_jysk()
            if readval==0:
                y_move = 0
            elif readval==1:
                y_move = -40 #up
            else:
                y_move = 40 #down
            break
            
        #next_lvl
        if gotonext==1 or buttons[2].read():
            boxes = []
            walls = []
            dots = []
            player = Player(0,0)
            lvl = lvl+1
            gotonext = 0
            if lvl-1==curmap.get_max_lvl():
                over = 1
                break
            gather(lvl)
            break
            
        #reset
        if buttons[3].read():
            boxes = []
            walls = []
            dots = []
            player = Player(0,0)
            lvl = 1
            gather(lvl)
            break
            
        if start==1:
            gather(lvl)
            start=0
            break

    print("updating")
    
    if not x_move==0 or not y_move==0:
        if check_player(player.get_x(),player.get_y(),x_move,y_move)==0:
            player.set_x(player.get_x()+x_move)
            player.set_y(player.get_y()+y_move)
        else:
            illegal = 1
    
    x_move = 0
    y_move = 0
    
    gotonext = check_dot()
    
    if over==1:
        gameDisplay.blit(winimg,(0,-80))
    else:
        gameDisplay.fill(white)
        draw_player(player.get_x(),player.get_y())
        for i in range(len(walls)):
            draw_wall(walls[i].get_x(), walls[i].get_y())
        for i in range(len(dots)):
            draw_dot(dots[i].get_x(), dots[i].get_y())
        for i in range(len(boxes)):
            draw_box(boxes[i].get_x(), boxes[i].get_y())
    
        if illegal==1:
            gameDisplay.blit(stopimg,(560,0))
            illegal = 0

    pygame.display.update()
    clock.tick(60)
    pygame.image.save(gameDisplay, "/home/xilinx/jupyter_notebooks/Getting_Started/images/gametovideo.png")
    
    img_path = '/home/xilinx/jupyter_notebooks/Getting_Started/images/gametovideo.png'
    img = Image.open(img_path)
    img = img.convert('RGB')

    frame_raw = hdmi_out.frame_raw()
    index = hdmi_out.frame_index()
    #hdmi_out.frame_index_next()
    print("drawwing")

    for i in range(0,display_width):
        for j in range(0,display_height):
            r,g,b = img.getpixel((i,j))
            tmp = (display_width*j*3+i)*3
            frame_raw[tmp+1] = g
            frame_raw[tmp] = b
            frame_raw[tmp+2] = r 
#             frame[i,j] = (b,g,r)
            
    print("finished")        
            

    hdmi_out.frame_raw(index, frame_raw)
    hdmi_out.frame_index(index)
    
    if over==1:
        time.sleep(5)
        crashed = True
        


pygame.quit()
hdmi_out.stop()
del hdmi_out
quit()
