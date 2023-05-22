import win32console, win32con, time
from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *

# *(©) e(¤) .( ) -(░) =(▒) x(▓) #(█)

arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height = 31
width = 31

screen = ''
# idno = 1
# name = 'texture'
# maptype = 'level'
# mapnum = 16
# directory = '..\\Resources\\'
gravity = False
jumpheight = 10
movedistance = 1
movedir =   {'up':      True, 
             'down':    True, 
             'left':    True, 
             'right':   True,
             'jump':    False}

texture = {}

namefile = open('..\\3D_CLI_ASCII\\mapname.txt')
mapname = ''.join(list(namefile.readline())[:-1])
texturename = namefile.readline()

texturefile = open(texturename, encoding="utf-8")
readtexture = list(texturefile.read())

textureWidth = int(readtexture[0])*10 + int(readtexture[1])
screenHeight = height*textureWidth
screenWidth = width*textureWidth
line = textureWidth**2+1
key = ''
value = []

if textureWidth == 1:
    for i in range(2, len(readtexture)):
        if i%2 == 0:
            key = readtexture[i]
        else:
            texture[key] = readtexture[i]
else:
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

def findplayer(i):
    global board
    for y in range(height):
        for x in range(width):
            if board[coord(x, y, width)] == '*':
                board[coord(x, y, width)] = '.'
                return [x, y]
                break

def make2d(board1):
    boardx = []
    for y in range(height):
        for x in range(width):
            character = board1[coord(x, y, width)]
            boardx.append(character)
    return boardx

def moveplayer(direction='', distance=movedistance):
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
        if board[coord(playercoord[0], playercoord[1] + movedistance, width)] != '#':
            playercoord[1] += movedistance
        else:
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
    if board[coord(playercoord[0], playercoord[1])] == 'x':
        return 'win'
    elif False:
        return 'lose'
    else:
        return ''

system('mode ' + str(screenWidth) + ',' + str(screenHeight))
myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
myConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active

file = open(mapname)
# try:
#     file = open(mapname)
# except:
#     file = open('..\\' + mapname)
board = make2d(list(file.read()))
file.close()
playercoord = findplayer(i)
jumping = 0
jumped = False
end = ''
# elapsedTime = 0.0
# time1 = time.perf_counter_ns()
# time2 = time.perf_counter_ns()

delay = 1/textureWidth**5
while end == '':
    # time2 = time.perf_counter_ns()
    # elapsedTime = time2-time1
    # movedistance *= elapsedTime
    # time1 = time2
    checkmovement()
    end = checkend()
    writeToScreen()
    myConsole.WriteConsoleOutputCharacter(Characters=screen, WriteCoord=win32console.PyCOORDType(0,0))
    time.sleep(delay)

emptyscreen()

if end == 'win':
    print('Congratulations!\nYou won!\n')
else:
    print('You lost!\nBetter luck next time.\n')
time.sleep(2)
input()








