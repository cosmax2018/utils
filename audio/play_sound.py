
# play_sound.py : play single notes

import pygame.midi
import time
from random import randint,random

VOLUME = 127	# ..maximum volume

major=[0,4,7,12]

def go(note):
    player.note_on(note, 127,1)
    time.sleep(1)
    player.note_off(note,127,1)

def arp(base,ints):
    for n in ints:
        go(base+n)

def chord(base, ints):
    player.note_on(base,127,1)
    player.note_on(base+ints[1],127,1)
    player.note_on(base+ints[2],127,1)
    player.note_on(base+ints[3],127,1)
    time.sleep(1)
    player.note_off(base,127,1)
    player.note_off(base+ints[1],127,1)
    player.note_off(base+ints[2],127,1)
    player.note_off(base+ints[3],127,1)
	
def play(n):
	player.note_on(n, VOLUME,14)
	time.sleep(.1)#random())
	player.note_off(n,VOLUME,14)


pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)
# player.set_instrument(48,1)

i = 0
for note in range(1,100):#256):
	# note = randint(1,100)#256)
	play(note)
	i += 1
	print(i)

del player
pygame.midi.quit()
	