# from ctypes import windll, byref
# from ctypes.wintypes import SMALL_RECT

# STDOUT = -11

# hdl = windll.kernel32.GetStdHandle(STDOUT)
# rect = SMALL_RECT(0, 0, 100, 100) # (left, top, right, bottom)
# windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))

# for y in range(100):
#     littlestring = ''
#     for x in range(100):
#         littlestring += str((x//10+y//10)%10)
#     print(littlestring)

# from win32api import GetAsyncKeyState as keypress
# from os import system

# while 1:
#     system('cls')
#     if keypress(ord('R')):
#         print('A')

# input()

codefile = open('..\\3D_CLI_ASCII\\Source.cpp', encoding="utf-8")
readcodefile = codefile.read()
number = int(readcodefile[197:200])
size = int(readcodefile[210:213])
print(number, size)
input()