from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *
import time as tm
import random
from copy import deepcopy

# Resources
block = {'*' : '©', '.' : ' ', '-' : '░', '=' : '▒', 'x' : '▓', '#' : '█'}
arrow = {'left':    0x25, 
         'up':      0x26, 
         'right':   0x27, 
         'down':    0x28}

# Map Parameters
height= 81
width = 81
sectionheight = 21
sectionwidth = 33
sectionposX = 0
sectionposY = height - sectionheight

# Player Parameters
startPos = {'X':        width//2, 
            'Y':        height-2}
player =   {'X' :       startPos['X'], 
            'Y' :       startPos['Y'], 
            'shape' :   block['*']}

# Scoring
score = 0
scoreSystem = {'Vertical distance':     True,
               'Horizontal distance':   False,
               'Entity kill':           False}

# Map Generation
layerverticalinterval = 5
layerthickness = 1
variation = 3
platformClearance = 1
finishline = height - 2
surroundBorders = True
topFinishline = True
randomPlatforms =   {'X': False, 
                     'Y': True}
periodicPlatforms = {'X': False, 
                     'Y': True}
texturedBackground = False

# Physics
full = False
movedistance = 1
jumpheight = 11
gravity = True
movedir =   {'up':      True, 
             'down':    True, 
             'left':    True, 
             'right':   True,
             'jump':    True}
scrolling = {'up':      False, 
             'down':    False, 
             'left':    False, 
             'right':   False}

gamearea = []

def reset():
    global gamearea, height, width, block
    gamearea.clear()
    prevm = int(width/3)
    prevn = int(width*2/3)
    for y in range(height-1, -1, -1):
        newline = []
        if y%layerverticalinterval==0:
            m = random.randint(prevm-variation,prevm+variation)
            n = random.randint(prevn-variation,prevn+variation)
        for x in range(width):
            if topFinishline and y == finishline:
                newline.append(block['x'])
                
            elif surroundBorders and (y == 0 or y == height-1 or x == 0 or x == width-1):
                newline.append(block['#'])
                
            elif randomPlatforms['Y'] and ((y%(layerverticalinterval*2) == 0 and (x <= m or x >= n)) or (y%(layerverticalinterval*2) == layerverticalinterval and (x > m and x < n))):
                newline.append(block['#'])
                
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*0 and x-(platformClearance-1)*7 <= width*1/7):
                newline.append(block['#'])
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*1 and x+platformClearance*7 >= width*2/7 and x+platformClearance*7 <= width*3/7):
                newline.append(block['#'])
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*2 and x+platformClearance*7 >= width*4/7 and x+platformClearance*7 <= width*5/7):
                newline.append(block['#'])
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*3 and x+(platformClearance-1)*7 >= width*6/7):
                newline.append(block['#'])
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*4 and x-platformClearance*7 >= width*4/7 and x-platformClearance*7 <= width*5/7):
                newline.append(block['#'])
            elif periodicPlatforms['Y'] and (y%(layerverticalinterval*6) == layerverticalinterval*5 and x-platformClearance*7 >= width*2/7 and x-platformClearance*7 <= width*3/7):
                newline.append(block['#'])
                
            elif texturedBackground and (y%4 == 0 or x%4 == 0):
                newline.append(block['='])
            elif texturedBackground and (y%2 == 0 and x%2 == 0):
                newline.append(block['-'])
                
            else:
                newline.append(block['.'])
        gamearea.append(newline)

def putplayer(x,y):
    global displayarea, player
    displayarea[y][x] = player['shape']

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def fulldisplay():
    global height, width, displayarea
    for y in range(height):
        for x in range(width):
            gotoxy(x+1,y+1)
            print(displayarea[y][x], end='')
        print('')

def sectiondisplay():
    global sectionposX, sectionposY
    
    #left-right scroll
    if player['X'] < sectionwidth/2:
        sectionposX = 0
    elif player['X'] > width-sectionwidth/2:
        sectionposX = width - sectionwidth
    elif scrolling['right']:
        sectionposX += 1
    elif scrolling['left']:
        sectionposX -= 1
    else:
        sectionposX = player['X'] - sectionwidth//2
        
    #up-down scroll
    if player['Y'] < sectionheight/2 and not scrolling['up']:               # Top
        sectionposY = 0
    elif player['Y'] > height-sectionheight/2 and not scrolling['down']:    # Bottom
        sectionposY = height - sectionheight
    elif scrolling['down']:
        sectionposY += 1
    elif scrolling['up']:
        sectionposY -= 1
    elif player['Y'] <= playerprev['Y']:
        sectionposY = player['Y'] - sectionheight//2
    else:
        sectionposY = player['Y'] - sectionheight//2

    for y in range(sectionheight):
        for x in range(sectionwidth):
            gotoxy(x+1,y+1)
            print(displayarea[sectionposY+y][sectionposX+x], end='')
        print('')
        
    print('Score:', score)

def moveplayer(direction='', distance=movedistance):
    global displayarea, gamearea, player, height, width, block, jumping, jumped
    displayarea[player['Y']][player['X']] = gamearea[player['Y']][player['X']]
    
    #up, down, left and right
    if direction == 'up':
        if displayarea[player['Y'] - distance][player['X']] != block['#']:
            if player['Y'] > 0:
                player['Y'] -= distance
            else: 
                player['Y'] = height-1
        elif distance != 1:
            raise Exception()
    if direction == 'down':
        if displayarea[player['Y'] + distance][player['X']] != block['#']:
            if player['Y'] < height-1:
                player['Y'] += distance
            else: 
                player['Y'] = 0
        elif distance != 1:
            raise Exception()
    if direction == 'left':
        if displayarea[player['Y']][player['X'] - distance] != block['#']:
            if player['X'] > 0:
                player['X'] -= distance
            else: 
                player['X'] = width-1
        elif distance != 1:
            raise Exception()
    if direction == 'right':
        if displayarea[player['Y']][player['X'] + distance] != block['#']:
            if player['X'] < width-1:
                player['X'] += distance
            else: 
                player['X'] = 0
        elif distance != 1:
            raise Exception()
    
    #always try to fall
    if gravity and displayarea[player['Y'] + 1][player['X']] != block['#'] and not jumped:
        if displayarea[player['Y'] + movedistance][player['X']] != block['#']:
            player['Y'] += movedistance
        else:
            player['Y'] += 1
    
    
    if direction == 'jump' and (displayarea[player['Y'] + 1][player['X']] == block['#'] or displayarea[player['Y'] + 1][player['X']-1] == block['#'] or displayarea[player['Y'] + 1][player['X']+1] == block['#']):
        jumping = distance
        
    if jumping:
        if displayarea[player['Y'] - 1][player['X']] != block['#']:
            jumped = True
            player['Y'] -= 1
            jumping -= 1
        else:
            jumping = 0
            jumped = False
    else:
        jumped = False
    displayarea[player['Y']][player['X']] = block['*']

def checkmovement():
    global arrow
    for direction in ['up', 'down', 'left', 'right']:
        if movedir[direction] and keypress(arrow[direction]):
            try:
                moveplayer(direction, movedistance)
            except:
                moveplayer(direction, 1)
    if movedir['jump'] and keypress(VK_SPACE):
        moveplayer('jump', jumpheight)
    moveplayer()

def checkend():
    if gamearea[player['Y']][player['X']] == block['x']:
        return 'win'
    elif scrolling['up'] and sectionposY+sectionheight <= player['Y']:
        return 'lose'
    else:
        return ''

def updateScore():
    global score
    if scoreSystem['Vertical distance']:
        score = startPos['Y'] - player['Y']
    if scoreSystem['Horizontal distance']:
        score = player['X'] - startPos['X']

reset()
displayarea = deepcopy(gamearea)
putplayer(player['X'],player['Y'])
jumping = 0
jumped = False
end = ''
playerprev = player
while end == '':
    system('cls')
    checkmovement()
    updateScore()
    end = checkend()
    if keypress(ord('F')):
        full = not full
    if full:
        fulldisplay()
    else:
        sectiondisplay()
    tm.sleep(0.05)

system('cls')
if end == 'win':
    print('Congratulations!\nYou won!')
else:
    print('You lost!\nBetter luck next time.')
print('Score:', score)
input()













