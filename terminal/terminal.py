# terminal.py : terminal routines

import sys
import re
import os
from subprocess import Popen, PIPE


off 		= '\033[0m\033[27m'
bold 		= '\033[1m'
dim 		= '\033[2m'
underscore 	= '\033[4m'
blink 		= '\033[5m'
reverse 	= '\033[7m'
hide 		= '\033[8m'

black 		= '\033[30m'
red 		= '\033[31m'
green 		= '\033[32m'
yellow 		= '\033[33m'
blue 		= '\033[34m'
magenta 	= '\033[35m'
cyan 		= '\033[36m'
white 		= '\033[37m'

bgblack 	= '\033[40m'
bgred 		= '\033[41m'
bggreen 	= '\033[42m'
bgyellow 	= '\033[43m'
bgblue 		= '\033[44m'
bgmagenta	= '\033[45m'
bgcyan 		= '\033[46m'
bgwhite 	= '\033[47m'
	
def send(cmd):
    sys.stdout.write(cmd)
    sys.stdout.flush()
	
def pos(line, column):
	# posiziona il cursore
    send('\033[%s;%sf' % (line, column))
	
def homePos():
    send('\033[H')

def up(value=1):
    send('\033[%sA' % value)

def down(value=1):
    send('\033[%sB' % value)

def right(value=1):
    send('\033[%sC' % value)

def left(value=1):
    send('\033[%sD' % value)

def saveCursor():
    send('\0337')
    # send('\033[s')

def restoreCursor():
    send('\0338')
    # send('\033[u')

def clear():
    send('\033[2J')

def clearLineFromPos():
    send('\033[K')

def clearLineToPos():
    send('\033[1K')

def clearLine():
    send('\033[2K')

def write(text='', *style):
    send(format(text, *style))

def writeLine(text='', *style):
    write(str(text) + '\n', *style)

def setTitle(name):
    send('\033]2;%s\007' % name)

def clearTitle():
    setTitle('')

def setTab(name):
    send('\033]1;%s\007' % name)

def clearTab():
    setTab('')

def strip(text):
    return re.sub('\x1b\[[0-9]{1,2}m', '', text)

def center(text):
    return ' ' * (int(getSize()[1] / 2) - int(len(strip(text)) / 2)) + text

def right(text):
    return ' ' * (getSize()[1] - len(strip(text))) + text
	
def message(message,pause):
	# print a message to console and wait if necessary
	print(message)
	if pause: sleep
	
def locate(message,x=0,y=0):
	# Plot the message at the starting at position HORIZ, VERT...
	x,y = int(x),int(y)
	if x >= 255: x = 255
	if y >= 255: y = 255
	if x <= 0: x = 0
	if y <= 0: y = 0
	HORIZ,VERT = str(x),str(y)
	print("\033["+VERT+";"+HORIZ+"f"+message)
	if pause: sleep

def getCursorPos():
	# ritorna la posizione del cursore
	sys.stdout.write("\x1b[6n"); a = sys.stdin.read(10)
	return a[2:]
	
def getch():
	# ritorna il codice ascii del tasto premuto
   import msvcrt
   while True:
       if msvcrt.kbhit():
           return msvcrt.getch()
