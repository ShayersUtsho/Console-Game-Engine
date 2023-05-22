import win32console, win32con, time
#═║
block = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}
dirsign = list('o^>└v│┌├<┘─┴┐┤┬┼')
texture = {}
texture[9] = {'p' : '╔─┬─╦─┬─╗│ │ │ │ │├─█─┼─█─┤│ │ │ │ │╠─┼─╬─┼─╣│ │ │ │ │├─█─┼─█─┤│ │ │ │ │╚─┴─╩─┴─╝',
              's' : ' ·· ·· ···· ·· ·· · ·· ·· · ·· ·· ···· ·· ·· · ·· ·· · ·· ·· ···· ·· ·· · ·· ·· ·',
              'l' : '·::·::·::::·::·::·:·::·::·:·::·::·::::·::·::·:·::·::·:·::·::·::::·::·::·:·::·::·:',
              'm' : ':##:##:####:##:##:#:##:##:#:##:##:####:##:##:#:##:##:#:##:##:####:##:##:#:##:##:#',
              'd' : '▓▒▒░░░▒▒▓▒░░   ░░▒░░     ░░░       ░░       ░░       ░░░     ░░▒░░   ░░▒▓▒▒░░░▒▒▓',
              'b' : '▓██▓██▓████▓██▓██▓█▓██▓██▓█▓██▓██▓████▓██▓██▓█▓██▓██▓█▓██▓██▓████▓██▓██▓█▓██▓██▓█'}
texture[8] = {'p' : '╔╦─┬┬─╦╗╠┼─┼┼─┼╣││ ││ ││├┼─┼┼─┼┤├┼─┼┼─┼┤││ ││ ││╠┼─┼┼─┼╣╚╩─┴┴─╩╝',
              's' : ' · · · ·· · · ·  · · · ·· · · ·  · · · ·· · · ·  · · · ·· · · · ',
              'l' : '·:·:·:·::·:·:·:··:·:·:·::·:·:·:··:·:·:·::·:·:·:··:·:·:·::·:·:·:·',
              'm' : ':#:#:#:##:#:#:#::#:#:#:##:#:#:#::#:#:#:##:#:#:#::#:#:#:##:#:#:#:',
              'd' : '▓▒░░░░▒▓▒░    ░▒░      ░░      ░░      ░░      ░▒░    ░▒▓▒░░░░▒▓',
              'b' : '▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓'}
texture[7] = {'p' : '╔─┬─┬─╗│ │ │ │├─┼─┼─┤│ │ │ │├─┼─┼─┤│ │ │ │╚─┴─┴─╝',
              's' : ' · · · · · · · · · · · · · · · · · · · · · · · · ',
              'l' : '·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·',
              'm' : ':#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:',
              'd' : '▓▒░░░▒▓▒░   ░▒░     ░░     ░░     ░▒░   ░▒▓▒░░░▒▓',
              'b' : '▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓'}
texture[6] = {'p' : '╔─┬┬─╗│ ││ │├─┼┼─┤├─┼┼─┤│ ││ │╚─┴┴─╝',
              's' : ' · · ·· · ·  · · ·· · ·  · · ·· · · ',
              'l' : '·:·:·::·:·:··:·:·::·:·:··:·:·::·:·:·',
              'm' : ':#:#:##:#:#::#:#:##:#:#::#:#:##:#:#:',
              'd' : '▓▒░░▒▓▒░  ░▒░    ░░    ░▒░  ░▒▓▒░░▒▓',
              'b' : '▓█▓█▓██▓█▓█▓▓█▓█▓██▓█▓█▓▓█▓█▓██▓█▓█▓'}
texture[5] = {'p' : '╔─┬─╗│ │ │├─┼─┤│ │ │╚─┴─╝',
              's' : ' · · · · · · · · · · · · ',
              'l' : '·:·:·:·:·:·:·:·:·:·:·:·:·',
              'm' : ':#:#:#:#:#:#:#:#:#:#:#:#:',
              'd' : '▓▒░▒▓▒░ ░▒░   ░▒░ ░▒▓▒░▒▓',
              'b' : '▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓'}
texture[4] = {'p' : '╔┬┬╗├┼┼┤├┼┼┤╚┴┴╝',
              's' : ' · ·· ·  · ·· · ',
              'l' : '·:·::·:··:·::·:·',
              'm' : ':#:##:#::#:##:#:',
              'd' : '▓▒▒▓▒░░▒▒░░▒▓▒▒▓',
              'b' : '▓█▓██▓█▓▓█▓██▓█▓'}
texture[3] = {'p' : '╔┬╗├┼┤╚┴╝',
              's' : ' · · · · ',
              'l' : '·:·:·:·:·',
              'm' : ':#:#:#:#:',
              'd' : '▒░▒░ ░▒░▒',
              'b' : '▓█▓█▓█▓█▓'}

height = 31
width = 31

screen = ''
textureWidth = 5

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
    for i in range(700*180):
        screen += ' '

def writeToScreen():
    global board, screen
    screen = ''
    for y in range(height):
        for j in range(textureWidth):
            for x in range(width):
                for i in range(textureWidth):
                        screen += list(texture[textureWidth][board[coord(x, y, width)]])[coord(i, j, textureWidth)]
            for a in range(700 - textureWidth*width):
                screen += ' '
    for b in range(180 - textureWidth*height):
        for a in range(700):
            screen += ' '

def findplayer():
    global board
    for y in range(height):
        for x in range(width):
            if board[coord(x, y, width)] == 'p':
                board[coord(x, y, width)] = 's'
                return [x, y]
                break

def findexit():
    global board
    for y in range(height):
        for x in range(width):
            if board[coord(x, y, width)] == 'd':
                return [x, y]
                break

def make2d(board1):
    boardx = []
    for y in range(height):
        for x in range(width):
            character = board1[coord(x, y, width)]
            boardx.append(character)
    return boardx


class Vertex:
    r = False
    d = False
    l = False
    u = False
    direc = ' '
    def __init__(self, u, r, d, l):
        self.u = u
        self.r = r
        self.d = d
        self.l = l
        self.direc = dirsign[u + r*2 + d*4 + l*8]
    def __repr__(self):
        return self.direc
    def __str__(self):
        return self.direc
#o^>└v│┌├<┘─┴┐┤┬┼

def makeGraph():
    global board
    vertices = []
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            vertices.append(Vertex( board[coord(x, y-1)]=='s', board[coord(x+1, y)]=='s', board[coord(x, y+1)]=='s', board[coord(x-1, y)]=='s'))
    return vertices

def makeStr():
    pass

myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
myConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active

i = 1
if i >= 7:
    height = 15
file = open('DesignedLevels\\level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
board = list(file.read())
player_coord = findplayer()
exit_coord = findexit()
writeToScreen()
myConsole.WriteConsoleOutputCharacter(Characters=screen, WriteCoord=win32console.PyCOORDType(0,0))
file.close()
time.sleep(3)
myConsole.Close()
print((makeGraph()))
input()














