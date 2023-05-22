import win32console, win32con, time
#═║
block = {'*' : '©', '.' : ' ', '-' : '░', '=' : '▒', 'x' : '▓', '#' : '█'}
texture = {}
texture[9] = {'*' : '╔─┬─╦─┬─╗│ │ │ │ │├─█─┼─█─┤│ │ │ │ │╠─┼─╬─┼─╣│ │ │ │ │├─█─┼─█─┤│ │ │ │ │╚─┴─╩─┴─╝',
              '.' : ' ·· ·· ···· ·· ·· · ·· ·· · ·· ·· ···· ·· ·· · ·· ·· · ·· ·· ···· ·· ·· · ·· ·· ·',
              '-' : '·::·::·::::·::·::·:·::·::·:·::·::·::::·::·::·:·::·::·:·::·::·::::·::·::·:·::·::·:',
              '=' : ':##:##:####:##:##:#:##:##:#:##:##:####:##:##:#:##:##:#:##:##:####:##:##:#:##:##:#',
              'x' : '▓▒▒░░░▒▒▓▒░░   ░░▒░░     ░░░       ░░       ░░       ░░░     ░░▒░░   ░░▒▓▒▒░░░▒▒▓',
              '#' : '▓██▓██▓████▓██▓██▓█▓██▓██▓█▓██▓██▓████▓██▓██▓█▓██▓██▓█▓██▓██▓████▓██▓██▓█▓██▓██▓█'}
texture[8] = {'*' : '╔╦─┬┬─╦╗╠┼─┼┼─┼╣││ ││ ││├┼─┼┼─┼┤├┼─┼┼─┼┤││ ││ ││╠┼─┼┼─┼╣╚╩─┴┴─╩╝',
              '.' : ' · · · ·· · · ·  · · · ·· · · ·  · · · ·· · · ·  · · · ·· · · · ',
              '-' : '·:·:·:·::·:·:·:··:·:·:·::·:·:·:··:·:·:·::·:·:·:··:·:·:·::·:·:·:·',
              '=' : ':#:#:#:##:#:#:#::#:#:#:##:#:#:#::#:#:#:##:#:#:#::#:#:#:##:#:#:#:',
              'x' : '▓▒░░░░▒▓▒░    ░▒░      ░░      ░░      ░░      ░▒░    ░▒▓▒░░░░▒▓',
              '#' : '▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓▓█▓█▓█▓██▓█▓█▓█▓'}
texture[7] = {'*' : '╔─┬─┬─╗│ │ │ │├─┼─┼─┤│ │ │ │├─┼─┼─┤│ │ │ │╚─┴─┴─╝',
              '.' : ' · · · · · · · · · · · · · · · · · · · · · · · · ',
              '-' : '·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·:·',
              '=' : ':#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:',
              'x' : '▓▒░░░▒▓▒░   ░▒░     ░░     ░░     ░▒░   ░▒▓▒░░░▒▓',
              '#' : '▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓'}
texture[6] = {'*' : '╔─┬┬─╗│ ││ │├─┼┼─┤├─┼┼─┤│ ││ │╚─┴┴─╝',
              '.' : ' · · ·· · ·  · · ·· · ·  · · ·· · · ',
              '-' : '·:·:·::·:·:··:·:·::·:·:··:·:·::·:·:·',
              '=' : ':#:#:##:#:#::#:#:##:#:#::#:#:##:#:#:',
              'x' : '▓▒░░▒▓▒░  ░▒░    ░░    ░▒░  ░▒▓▒░░▒▓',
              '#' : '▓█▓█▓██▓█▓█▓▓█▓█▓██▓█▓█▓▓█▓█▓██▓█▓█▓'}
texture[5] = {'*' : '╔─┬─╗│ │ │├─┼─┤│ │ │╚─┴─╝',
              '.' : ' · · · · · · · · · · · · ',
              '-' : '·:·:·:·:·:·:·:·:·:·:·:·:·',
              '=' : ':#:#:#:#:#:#:#:#:#:#:#:#:',
              'x' : '▓▒░▒▓▒░ ░▒░   ░▒░ ░▒▓▒░▒▓',
              '#' : '▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓█▓'}
texture[4] = {'*' : '╔┬┬╗├┼┼┤├┼┼┤╚┴┴╝',
              '.' : ' · ·· ·  · ·· · ',
              '-' : '·:·::·:··:·::·:·',
              '=' : ':#:##:#::#:##:#:',
              'x' : '▓▒▒▓▒░░▒▒░░▒▓▒▒▓',
              '#' : '▓█▓██▓█▓▓█▓██▓█▓'}
texture[3] = {'*' : '╔┬╗├┼┤╚┴╝',
              '.' : ' · · · · ',
              '-' : '·:·:·:·:·',
              '=' : ':#:#:#:#:',
              'x' : '▒░▒░ ░▒░▒',
              '#' : '▓█▓█▓█▓█▓'}

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
        for a in range(600):
            screen += ' '

def findplayer():
    global board
    for y in range(height):
        for x in range(width):
            if board[coord(x, y, width)] == '*':
                #board[coord(x, y, width)] = '.'
                return [x, y]
                break
    # if height == 15:
    #     board[coord(width-2, int(height/2))] = '*'

def make2d(board1):
    boardx = []
    for y in range(height):
        for x in range(width):
            character = board1[coord(x, y, width)]
            boardx.append(character)
    return boardx

myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
myConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active

for i in range(14):
    # if i >= 7:
    #     height = 15
    file = open('..\\Resources\\level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
    board = make2d(list(file.read()))
    player_coord = findplayer()
    writeToScreen()
    myConsole.WriteConsoleOutputCharacter(Characters=screen, WriteCoord=win32console.PyCOORDType(0,0))
    file.close()
    time.sleep(1)














