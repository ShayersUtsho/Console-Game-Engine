import win32console, win32con, time
from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *

# *(©) e(¤) .( ) -(░) =(▒) x(▓) #(█)

arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height = 31
width = 31

screen = ''
screenWidth = 700
screenHeight = 180
idno = 2
name = 'texture'
directory = '..\\Resources\\'
gravity = True
jumpheight = 10

texture = {}

texturefile = open(directory+name+'-'+str((idno)//10)+str((idno)%10)+'.txt', encoding="utf-8")
readtexture = list(texturefile.read())

textureWidth = int(readtexture[0])*10 + int(readtexture[1])
line = textureWidth**2+1
key = ''
value = []

for i in range(2, len(readtexture)):
    if i%line == 2:
        key = readtexture[i]
    else:
        value.append(readtexture[i])
    if i%line == 1:
        texture[key] = value
        value = []

def coord(x, y, w=width):
    return y*w + x

def change(string, i, val):
    temp = list(string)
    temp[i] = val
    string = ''.join(temp)

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def emptyscreen():
    global screen
    screen = ''
    for i in range(screenWidth*screenHeight):
        screen += ' '

def writeToScreen():
    global board, screen, playercoord
    screen = ''
    for y in range(height):
        for j in range(textureWidth):
            for x in range(width):
                for i in range(textureWidth):
                    if x == playercoord[0] and y == playercoord[1]:
                        screen += list(texture['*'])[coord(i, j, textureWidth)]
                    else:
                        screen += list(texture[board[coord(x, y, width)]])[coord(i, j, textureWidth)]
            for a in range(700 - textureWidth*width):
                screen += ' '
    for b in range(180 - textureWidth*height):
        for a in range(600):
            screen += ' '

def findplayer(i):
    global board
    for y in range(height):
        for x in range(width):
            if board[coord(x, y, width)] == '*':
                board[coord(x, y, width)] = '.'
                return [x, y]
                break
    if i >= 7:
        # board[coord(x, y, width)] = '*'
        return [1, 1]

def make2d(board1):
    boardx = []
    for y in range(height):
        for x in range(width):
            character = board1[coord(x, y, width)]
            boardx.append(character)
    return boardx

def moveplayer(direction='', distance=1):
    global board, playercoord, height, width, block, jumping, jumped
    
    #up, down, left and right
    if direction == 'up' and board[coord(playercoord[0], playercoord[1] - distance, width)] != '#':
        if playercoord[1] > 0:
            playercoord[1] -= distance
        else: 
            player[1] = height-1
    if direction == 'down' and board[coord(playercoord[0], playercoord[1] + distance, width)] != '#':
        if playercoord[1] < height-1:
            playercoord[1] += distance
        else: 
            playercoord[1] = 0
    if direction == 'left' and board[coord(playercoord[0] - distance, playercoord[1], width)] != '#':
        if playercoord[0] > 0:
            playercoord[0] -= distance
        else: 
            playercoord[0] = width-1
    if direction == 'right' and board[coord(playercoord[0] + distance, playercoord[1], width)] != '#':
        if playercoord[0] < width-1:
            playercoord[0] += distance
        else: 
            playercoord[0] = 0
    
    #always try to fall
    if gravity and board[coord(playercoord[0], playercoord[1] + 1, width)] != '#' and not jumped:
        playercoord[1] += 1
    
    
    if direction == 'jump' and (board[coord(playercoord[0], playercoord[1] + 1, width)] == '#' or board[coord(playercoord[0] - 1, playercoord[1] + 1, width)] == '#' or board[coord(playercoord[0] - 1, playercoord[1] + 1, width)] == '#'):
        jumping = distance
        
    if jumping:
        if board[coord(playercoord[0], playercoord[1] - 1, width)] != '#':
            jumped = True
            playercoord[1] -= 1
            jumping -= 1
        else:
            jumping = 0
            jumped = False
    else:
        jumped = False

def checkmovement():
    global arrow
    if keypress(arrow['left']):
        moveplayer('left', 1)
    if keypress(arrow['right']):
        moveplayer('right', 1)
    if keypress(arrow['up']):
        moveplayer('up', 1)
    if keypress(arrow['down']):
        moveplayer('down', 1)
    if keypress(VK_SPACE):
        moveplayer('jump', jumpheight)
    moveplayer()

def checkend():
    if board[coord(playercoord[0], playercoord[1])] == 'x':
        return 'win'
    elif False:
        return 'lose'
    else:
        return ''

system('mode 700,180')
i=1
file = open('NewLevels\\level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
board = make2d(list(file.read()))
file.close()
playercoord = findplayer(i)
jumping = 0
jumped = False
end = ''

while end == '':
    # board[coord(playercoord[0], playercoord[1], width)] = '.'
    checkmovement()
    # board[coord(playercoord[0], playercoord[1], width)] = '*'
    writeToScreen()
    for newy in range(180):
        print(screen[newy*700:(newy+1)*700])

emptyscreen()
if end == 'win':
    print('Congratulations!\nYou won!\n')
else:
    print('You lost!\nBetter luck next time.\n')
input()
# for i in range(10):
#     file = open('NewLevels\\level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
#     board = make2d(list(file.read()))
#     playercoord = findplayer(i)
#     writeToScreen()
#     myConsole.WriteConsoleOutputCharacter(Characters=screen, WriteCoord=win32console.PyCOORDType(0,0))
#     file.close()
#     time.sleep(1)














