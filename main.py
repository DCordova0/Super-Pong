#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import random
import operator
import numpy
import math
import time

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

VEL_INCREMENT = 1.05
MAX_VEL = 15

NORMAL_SIZE = 70

WHITE = 255,255,255
BLACK = 0,0,0
PURPLE = 102,0,102
TOP = 50
BOT = SCREEN_HEIGHT-10

def collition(rec1, rec2):
	x1,y1,w1,h1 = rec1
	x2,y2,w2,h2 = rec2
	if (x1 < x2+w2 and x1+w1>x2 and
		y1 < y2+h2 and y1+h1>y2):
		return True
	else:
		return False

class Table: 
	def __init__(self,x,y,w,h,side):
		self.side = side # "r": pega por la derecha, "l": pega por la izq.
		self.pos = (x,y)
		self.h = h
		self.w = w
		self.vel = 8
		self.color = WHITE
		self.image = pygame.Surface((w, h))
		self.image.fill(self.color)

	def draw(self, screen):
		screen.blit(self.image, self.pos)

	def move_up(self):
		self.pos = numpy.subtract(self.pos, (0, self.vel))
		if self.pos[1] < TOP:
			self.pos = (self.pos[0], TOP)

	def move_down(self):
		self.pos = numpy.add(self.pos, (0, self.vel))
		if self.pos[1]+self.h > BOT:
			self.pos = (self.pos[0], BOT-self.h)

	#Chequear si bola golpea esta tabla
	def hit(self, ball):
		if collition( (ball.pos[0]-ball.r, ball.pos[1]-ball.r, ball.r*2, ball.r*2),
		(self.pos[0], self.pos[1], self.w, self.h) ):
			if (self.side == "l" and ball.vel[0] > 0):
				dy = ball.pos[1] - (self.pos[1]+self.h/2)
				dx = self.h/2.0
				alpha = math.atan(float(dy)/dx)
				vel = (ball.vel[0]**2+ball.vel[1]**2)**0.5
				vel = vel*VEL_INCREMENT
				if vel > MAX_VEL:
					vel = MAX_VEL
				ball.vel = (-math.cos(alpha)*vel, math.sin(alpha)*vel)
			if (self.side == "r" and ball.vel[0] < 0):
				dy = ball.pos[1] - (self.pos[1]+self.h/2)
				dx = self.h/2.0
				alpha = math.atan(float(dy)/dx)
				vel = (ball.vel[0]**2+ball.vel[1]**2)**0.5
				vel = vel*VEL_INCREMENT
				if vel > MAX_VEL:
					vel = MAX_VEL
				ball.vel = (math.cos(alpha)*vel, math.sin(alpha)*vel)
			return True
		else:
			return False



class Ball: 
	def __init__(self,x,y,r, vel):
		self.pos = (x, y)
		self.r = r
		self.vel = vel
		self.color = WHITE
		self.image = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA, 32)
		pygame.draw.circle(self.image, self.color, (self.r,self.r), self.r)

	def draw(self, screen):
		screen.blit(self.image, numpy.subtract(self.pos, (self.r, self.r)))

	def update(self):
		# Choque con bordes superior e inferior.
		if self.pos[1] + self.r > BOT:
			self.vel = (self.vel[0], -self.vel[1])
		if self.pos[1] - self.r < TOP:
			self.vel = (self.vel[0], -self.vel[1])

		#Actualizar velocidad
		self.pos = numpy.add(self.pos, self.vel)

	#Si la bola esta fuera de la pantalla
	def out(self):
		if self.pos[0]-self.r > SCREEN_WIDTH:
			return 2
		if self.pos[0]+self.r < 0:
			return 1
		return 0



def main():

	#Iniciar Pygame
	pygame.init()

	print "   Welcome to Pong Deluxe!"

	#Fuentes
	myfont = pygame.font.SysFont("monospace", 25)

	#Objetos del juego
	ball = Ball(SCREEN_WIDTH/2, (TOP+BOT)/2.0, 10, (5,0))
	table1 = Table(10 , (TOP+BOT)/2.0-NORMAL_SIZE/2.0, 
		14, NORMAL_SIZE, "r")
	table2 = Table(SCREEN_WIDTH-10-10 , (TOP+BOT)/2.0-NORMAL_SIZE/2.0, 
		14, NORMAL_SIZE, "l")

	#Variables
	started = False
	paused = False
	score_p1 = 0
	score_p2 = 0
	start_p1 = False

	#Etiquetas
	score_p1_label = myfont.render(str(score_p1), 2, WHITE)
	score_p2_label = myfont.render(str(score_p2), 2, WHITE)
	press_enter_label = myfont.render("PRESS ENTER", 2, WHITE)
	paused_label = myfont.render("PAUSED", 2, WHITE)

	#Reloj
	clock 	= pygame.time.Clock()

	#Pantalla
	screen 	= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	#Para dibujar escenario
	background = pygame.Surface(screen.get_size())
	background.fill(BLACK)
	border = pygame.Surface((SCREEN_WIDTH, 10))
	border.fill(WHITE)
	background.blit(border, (0,TOP-10))
	background.blit(border, (0,BOT))



	while True:
		pygame.display.set_caption(" PONG DELUXE | FPS: "+str(round(clock.get_fps(),2)))
		milliseconds = clock.tick(FPS)


		#Manejo de eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print "   See you soon :) ..."
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					if started:
						paused = not paused
				if event.key == 13:
					if not started:
						started = True

		if not paused and started:
			#Manejo de teclas mantenidas
			keys = pygame.key.get_pressed()
			if keys[pygame.K_w]:
				table1.move_up()
			if keys[pygame.K_s]:
				table1.move_down()
			if keys[pygame.K_UP]:
				table2.move_up()
			if keys[pygame.K_DOWN]:
				table2.move_down()
		
			out = ball.out()
			if out == 1 or out == 2:
				started = False
				if out == 1:
					score_p2 += 1
					score_p2_label = myfont.render(str(score_p2), 1, WHITE)
				if out == 2:
					score_p1 += 1
					score_p1_label = myfont.render(str(score_p1), 1, WHITE)
				start_p1 = not start_p1
				if start_p1:
					ball = Ball(SCREEN_WIDTH/2, (TOP+BOT)/2.0, 10, (5,0))
				else:
					ball = Ball(SCREEN_WIDTH/2, (TOP+BOT)/2.0, 10, (-5,0))
				table1 = Table(10 , (TOP+BOT)/2.0-NORMAL_SIZE/2.0, 14, 
					NORMAL_SIZE, "r")
				table2 = Table(SCREEN_WIDTH-10-10 , (TOP+BOT)/2.0-NORMAL_SIZE/2.0, 
					14, NORMAL_SIZE, "l")

			#Actualizando
			ball.update()
			flag1 = table1.hit(ball)
			flag2 = table2.hit(ball)
			if flag1 or flag2:
				table1.vel *= VEL_INCREMENT
				table2.vel *= VEL_INCREMENT

		#Dibujando
		screen.blit(background, (0, 0))
		screen.blit(border, (0,TOP-10))
		screen.blit(border, (0,BOT))
		ball.draw(screen)
		table1.draw(screen)
		table2.draw(screen)
		if not started:
			screen.blit(press_enter_label, (SCREEN_WIDTH/2-80, (TOP+BOT)/3))
		if paused:
			screen.blit(paused_label, (SCREEN_WIDTH/2-80, (TOP+BOT)/3))
		screen.blit(score_p1_label, (SCREEN_WIDTH/4-10, 10))
		screen.blit(score_p2_label, (SCREEN_WIDTH*0.75-10, 10))
		
		#Hacer visibles los cambios
		pygame.display.flip()


if __name__ == "__main__":
	main()

		