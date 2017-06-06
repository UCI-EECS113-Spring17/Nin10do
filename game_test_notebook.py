import pygame
from pynq import Overlay
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

lvl = 1
#curmap = Map().get_lvl(lvl-1)
curmap = Map()
boxes = []
walls = []
dots = []
player = Player(0,0)

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
    
x_move = 0
y_move = 0
k = 0
nothing = 0
tmp = 0
start = 1

crashed = False

# Initialize HDMI as an input device
hdmi_out = HDMI('out')
hdmi_out.mode(0)
hdmi_out.start()

while not crashed:
    
    print("waiting")
    while True:
        if buttons[0].read():
            if switches[1].read():
                x_move = 0
            elif switches[0].read():
                x_move = -40 #left
            else:
                x_move = 40 #right
            break
            
        if buttons[1].read():
            if switches[1].read():
                y_move = 0
            elif switches[0].read():
                y_move = -40 #up
            else:
                y_move = 40 #down
            break
            
        if start==1:
            start=0
            break

    print("updating")
    
    player.set_x(player.get_x()+x_move)
    player.set_y(player.get_y()+y_move)
    
    x_move = 0
    y_move = 0
    
    gameDisplay.fill(white)
    draw_player(player.get_x(),player.get_y())
    for i in range(len(walls)):
        draw_wall(walls[i].get_x(), walls[i].get_y())
    for i in range(len(boxes)):
        draw_box(boxes[i].get_x(), boxes[i].get_y())
    for i in range(len(dots)):
        draw_dot(dots[i].get_x(), dots[i].get_y())

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
    
    k=k+1
    if k==10:
        crashed = True
        


pygame.quit()
hdmi_out.stop()
del hdmi_out
quit()
