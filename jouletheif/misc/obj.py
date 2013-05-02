import pygame
from log import *
debug("Someone is loading obj.py")

class JouleThiefSprite(pygame.sprite.Sprite):
	def _initilize(self):
		pygame.sprite.Sprite.__init__(self)

class JouledSprite(JouleThiefSprite):
	joules=0
	maxjoules=0
	def hasJoules(self): return joules>0