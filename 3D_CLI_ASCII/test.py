import win32console, win32con, time
from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *

# *(©) e(¤) .( ) -(░) =(▒) x(▓) #(█)

arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height = 31
width = 31

screen = ''
idno = 6
name = 'texture'
maptype = 'level'
mapnum = 14
directory = '..\\Resources\\'
gravity = False
jumpheight = 10
movedistance = 1
movedir =   {'up':      True, 
             'down':    True, 
             'left':    True, 
             'right':   True}

texture = {}

texturefile = open(directory+name+'-'+str((idno)//10)+str((idno)%10)+'.txt', encoding="utf-8")
readtexture = list(texturefile.read())

textureWidth = int(readtexture[0])*10 + int(readtexture[1])
screenHeight = height*textureWidth
screenWidth = width*textureWidth
line = textureWidth**2+1
key = ''
value = []

if idno == 1:
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
    if keypress(VK_SPACE):
        moveplayer('jump', jumpheight)
    moveplayer()
    if keypress(ord('R')):
        system('mode ' + str(screenWidth) + ',' + str(screenHeight))

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

file = open(directory+maptype+'-'+str(mapnum//10)+str(mapnum%10)+'.txt')
board = make2d(list(file.read()))
file.close()
playercoord = findplayer(i)
jumping = 0
jumped = False
end = ''
# elapsedTime = 0.0
# time1 = time.perf_counter_ns()
# time2 = time.perf_counter_ns()

delay = 1/idno**10
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
myConsole.Close()
system('mode 152,20')
newConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
newConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active

if end == 'win':
    text = ''
    text += '                                                                                                                                                        '
    text += '  ,ad8888ba,                                                                                88                    88                                    '
    text += ' d8\"\'    `\"8b                                                             ,d                88              ,d    \"\"                                    '
    text += 'd8\'                                                                       88                88              88                                          '
    text += '88             ,adPPYba,  8b,dPPYba,   ,adPPYb,d8 8b,dPPYba, ,adPPYYba, MM88MMM 88       88 88 ,adPPYYba, MM88MMM 88  ,adPPYba,  8b,dPPYba,  ,adPPYba,  '
    text += '88            a8\"     \"8a 88P\'   `\"8a a8\"    `Y88 88P\'   \"Y8 \"\"     `Y8   88    88       88 88 \"\"     `Y8   88    88 a8\"     \"8a 88P\'   `\"8a I8[    \"\"  '
    text += 'Y8,           8b       d8 88       88 8b       88 88         ,adPPPPP88   88    88       88 88 ,adPPPPP88   88    88 8b       d8 88       88  `\"Y8ba,   '
    text += ' Y8a.    .a8P \"8a,   ,a8\" 88       88 \"8a,   ,d88 88         88,    ,88   88,   \"8a,   ,a88 88 88,    ,88   88,   88 \"8a,   ,a8\" 88       88 aa    ]8I  '
    text += '  `\"Y8888Y\"\'   `\"YbbdP\"\'  88       88  `\"YbbdP\"Y8 88         `\"8bbdP\"Y8   \"Y888  `\"YbbdP\'Y8 88 `\"8bbdP\"Y8   \"Y888 88  `\"YbbdP\"\'  88       88 `\"YbbdP\"\'  '
    text += '                                       aa,    ,88                                                                                                       '
    text += '                                        \"Y8bbdP\"                                                                                                        '
    text += '                                                                                                                                                        '
    text += '8b        d8                        I8,        8        ,8I  ,ad8888ba,   888b      88 88                                                               '
    text += ' Y8,    ,8P                         `8b       d8b       d8\' d8\"\'    `\"8b  8888b     88 88                                                               '
    text += '  Y8,  ,8P                           \"8,     ,8\"8,     ,8\" d8\'        `8b 88 `8b    88 88                                                               '
    text += '   \"8aa8\" ,adPPYba,  88       88      Y8     8P Y8     8P  88          88 88  `8b   88 88                                                               '
    text += '    `88\' a8\"     \"8a 88       88      `8b   d8\' `8b   d8\'  88          88 88   `8b  88 88                                                               '
    text += '     88  8b       d8 88       88       `8a a8\'   `8a a8\'   Y8,        ,8P 88    `8b 88 \\\/                                                               '
    text += '     88  \"8a,   ,a8\" \"8a,   ,a88        `8a8\'     `8a8\'     Y8a.    .a8P  88     `8888 db                                                               '
    text += '     88   `\"YbbdP\"\'   `\"YbbdP\'Y8         `8\'       `8\'       `\"Y8888Y\"\'   88      `888 9P                                                               '
    
    newConsole.WriteConsoleOutputCharacter(Characters=text, WriteCoord=win32console.PyCOORDType(0,0))
    time.sleep(5.2)
    newConsole.Close()
else:
    print('You lost!\nBetter luck next time.\n')

# for i in range(10):
#     file = open('NewLevels\\level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
#     board = make2d(list(file.read()))
#     playercoord = findplayer(i)
#     writeToScreen()
#     myConsole.WriteConsoleOutputCharacter(Characters=screen, WriteCoord=win32console.PyCOORDType(0,0))
#     file.close()
#     time.sleep(1)







