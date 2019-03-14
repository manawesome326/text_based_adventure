#!/bin/python3

import random
import time
import re
import math
import string
import getpass
import sys
from datetime import datetime, timedelta
#Am I importing enough crap?

#range but better
def range2(inputlist):
	return range(inputlist[0], inputlist[1]+1)

deafened = False
hearing_loss = 0
DEBUG_fast_mode = False # DEBUG ONLYE
digest = {"grudge":False}

def print2(text, wait_time = 0.8, crystal_clear = False, mute_level = False):
	global deafened
	global hearing_loss
	if deafened and not crystal_clear:
		for i in range(math.floor(len(text)/(8-(mute_level or hearing_loss)))): #math crap
			randomselection = random.randint(0, len(text))
			text = text[:randomselection] + random.choice(list(string.ascii_lowercase)+[" "]*26) + text[randomselection+1:]
		print(text) 
	else:
		print(text)
	if not DEBUG_fast_mode:
		time.sleep(wait_time)

def darkness_envelops( white = False):
	sleep_time = 0.0001
	time_to_add = 0.000001
	for i in range(1920):
		if white:
			print(" ", end='')
		else:
			print("\u2588", end='')
		sys.stdout.flush()
		time.sleep(sleep_time)
		sleep_time += time_to_add
		time_to_add += 0.00000001

turns = 0

#exec(open('monsterbattleopening.py').read()) # is this a good idea? Well, you can't stop me.
#exec(open('walmar.py').read())
exec(open('speaking_bit.py').read())
exec(open('monsterbattleclosing.py').read())
