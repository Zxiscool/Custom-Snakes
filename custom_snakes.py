#!/usr/bin/env python
"""
    Copyright (C) 2012  Mattias Ugelvik

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import pygame, sys, random
from pygame.locals import *

width, height 	= 600,400	#Width and height of the window
boxsize 		= 10		#How big the "pixels" will be
speed 			= 40		#Speed of the game, less is more
bonusgrowth 	= 5			#How many boxes the snake will grow when he eats a fruit/bonus/award

helpstr = """
Arguments are used like this: <argument>=<value>  IMPORTANT: no space between the "=" and the argument/value
-ARGUMENTS
	windowsize	:: how big the window should be. valid input value is <width>x<height>.  DEFAULT: """+str(width)+"x"+str(height)+"""
	speed		:: How fast the game should run, smaller is faster. (20 is very fast, 200 is very slow, you do the math) DEFAULT: """+str(speed)+"""
	boxsize		:: Essentially how small the game will be, a small value will give a little snake and vice versa. DEFAULT: """+str(boxsize)+"""
	bonusgrowth	:: How nutritious the fruit will be. In other words, how many boxes the snake will grow after eating the fruit. DEFAULT: """+str(bonusgrowth)+"""
	help		:: What you're reading right now

-EXAMPLE:
	$ python custom_snakes.py windowsize=800x600 speed=20 boxsize=20 bonusgrowth=10
"""



def invalid_arg(arg):
	print "something went wrong with this argument: \""+arg+"\""
	sys.exit()
	
used_arguments = False

for arg in sys.argv[1:]:
	used_arguments = True
	if arg.startswith("windowsize="):
		try:
			size = map(int, arg[11:].split("x"))
			if min(size) > 80:
				width, height = int(size[0]), int(size[1])
			else:
				print "Minimum 80 pixels in both width and height (because I'm lazy and stupid)"
				sys.exit()
		except (IndexError, ValueError):
			invalid_arg(arg)
	elif arg.startswith("speed="):
		try:
			speed = int(arg[6:])
			if isinstance(speed,long):
				raise TypeError	
		except (ValueError, TypeError):
			invalid_arg(arg)
	elif arg.startswith("boxsize="):
		try:
			boxsize = int(arg[8:])
		except ValueError:
			invalid_arg(arg)
	elif arg.startswith("bonusgrowth="):
		try:
			bonusgrowth = int(arg[12:])
		except ValueError:
			invalid_arg(arg)
	elif arg == "help":
		print helpstr
		sys.exit()
	else:
		invalid_arg(arg)

if not used_arguments:
	print "Tips: run with the argument \"help\" to see options\n\tlike this: $ python snakes.py help"

if 0 < max(width % boxsize, height % boxsize):
	print "Warning: width and height should both be a multiples of boxsize"
if min(width,height) < boxsize*3:
	print "The snake doesn't fit on the board!"
	sys.exit()

class Box(pygame.sprite.Sprite):
	def __init__(self, color, boxsize):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([boxsize, boxsize])
		self.image.fill(color)


pygame.init()
screen = pygame.display.set_mode([width, height])


white = pygame.Color(255,255,255)


b = Box([255,0,0],boxsize)
award = Box([200,100,100],boxsize)


white = pygame.Color(255,255,255)

testdir = ["updown","downup","rightleft","leftright"]

def generate_award(occupied):	#Occupied is a list of tuples, which are the x and y of 
	award = occupied[0]			#boxes that are allready occupied by the snake body
	while award in occupied:
		award = [random.choice(range(0,width-boxsize,boxsize)),random.choice(range(0,height-boxsize,boxsize))]
	return award

def notopposite(olddir,newdir):	# Olddir and newdir are strings which can be one of up/down/left/right. 
								# I concatinate them and see if they are opposite of each other.
	if olddir+newdir in testdir: return False
	else: return True

dir_hash = {	#this translates string directions into numbers inside a tuple, which decides how much should
				#be added to x and y of some box.
	"down"	: (0,boxsize),
	"up"	: (0,-boxsize),
	"left"	: (-boxsize,0),
	"right"	: (boxsize,0)
	}

def gameover(score):
	print "you lost the game"
	print "your score: "+ str(score)
	sys.exit()

#	boxes contain all the snake boxes, each list contains x and y, and also a direction. It already contains 3, 
#	which decide where and how the snake will start the game.
boxes = [[[boxsize*3,boxsize],"right"],[[boxsize*2,boxsize],"right"],[[boxsize,boxsize],"right"]]

direction = boxes[0][1]  #A string representation of the direction the *head* of the snake will take

awardbox = generate_award([i[0] for i in boxes[1:]])
score = 0
doappend = 0	#Doappend is a number that represents how many boxes that should be appended to the snake,
				#this is necessary because we only want to append 1 box each game loop.
				#Each time a fruit/award is eated, doappend will become itself + bonusgrowth

screen.fill(white)
pygame.display.update()
while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10)
while 1:
	appendbox = boxes[-1][:]	#appendbox is a copy of the last box of the snake, that will be appended to the snake
								#if doappend > 0 and AFTER the last box has changed (so we don't put two boxes upon each other)
	screen.fill(white)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_DOWN:
				direction = "down"
			elif event.key == K_UP:
				direction = "up"
			elif event.key == K_LEFT:
				direction = "left"
			elif event.key == K_RIGHT:
				direction = "right"
			elif event.key == K_g:
				doappend += bonusgrowth #This is here for testing.
			elif event.key == K_q:
				pygame.quit()
				sys.exit()
			elif event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

	if direction != None:   #Check if the player tries to turn 180 degrees if he/she pressed an arrow key.
		validmove = notopposite(boxes[0][1],direction)
	else: validmove = True
	
	if not validmove:
		direction = boxes[0][1] #If the player tried to turn 180 degrees, then the snake will just continue going the same direction
	prev_dir = direction
	for i in boxes:
		numdir = dir_hash[i[1]]	#Translate up/down/right/left into a tuple with numbers that decide how much
								#the x and y coordinates should be incremented by
								
		i[0] = [i[0][0]+numdir[0],i[0][1]+numdir[1]]  #increment the x and y coordinates

		if i[0][0] >= width: #This part enables the snake to go outside of the game window and appear on the opposite side.
			i[0][0] = 0
		elif i[0][0] < 0:
			i[0][0] = width-boxsize
		elif i[0][1] >= height:
			i[0][1] = 0
		elif i[0][1] < 0:
			i[0][1] = height-boxsize

		i[1], prev_dir = prev_dir, i[1] #change the string representation of the direction so that it will be the value of
										#the box that was before it. For example, the last box of the snake would change its
										#direction to the second last, so that it follows the snake body. At the same time we
										#store the direction it currently have in prev_dir so that the next snake box can
										#follow in its footsteps.

		screen.blit(b.image,i[0])
		
	collisionboxes = [i[0] for i in boxes[1:]] #A list of tuples of all the x and y coordinates of the snake body (except the head)
	if boxes[0][0] in collisionboxes: #check if the head of the snake overlaps any of its tail boxes
		gameover(score)
	elif boxes[0][0] == awardbox:	#check if it (the head) overlaps the award/fruit, in which case, um, well the fruit is then eaten,
									#and a new fruit is made
		doappend += bonusgrowth
		score += 10
		awardbox = generate_award(collisionboxes)
	if doappend > 0:				#Remove a box from the append queue (by decrementing doappend) and append a copy of the
									#(previously) last box to boxes (which is the complete snake)
		doappend -= 1
		boxes.append(appendbox)
	
	screen.blit(award.image,awardbox)

	pygame.display.update()
	pygame.time.delay(speed)
