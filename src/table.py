import pygame, math, numpy, main

class Table:
	def __init__(self,x,y,w,h,side):
		self.side = side # "r": pega por la derecha, "l": pega por la izq.
		self.pos = (x,y)
		self.h = h
		self.w = w
		self.vel = 8
		self.color = main.WHITE
		self.image = pygame.Surface((w, h))
		self.image.fill(self.color)

	def draw(self, screen):
		screen.blit(self.image, self.pos)

	def move_up(self):
		self.pos = numpy.subtract(self.pos, (0, self.vel))
		if self.pos[1] < main.TOP:
			self.pos = (self.pos[0], main.TOP)

	def move_down(self):
		self.pos = numpy.add(self.pos, (0, self.vel))
		if self.pos[1]+self.h > main.BOT:
			self.pos = (self.pos[0], main.BOT-self.h)

	#Chequear si bola golpea esta tabla
	def hit(self, ball):
		if main.collition( (ball.pos[0]-ball.r, ball.pos[1]-ball.r, ball.r*2, ball.r*2),
		(self.pos[0], self.pos[1], self.w, self.h) ):
			if (self.side == "l" and ball.vel[0] > 0):
				dy = ball.pos[1] - (self.pos[1]+self.h/2)
				dx = self.h/2.0
				alpha = math.atan(float(dy)/dx)
				vel = (ball.vel[0]**2+ball.vel[1]**2)**0.5
				vel = vel*main.VEL_INCREMENT
				if vel > main.MAX_VEL:
					vel = main.MAX_VEL
				ball.vel = (-math.cos(alpha)*vel, math.sin(alpha)*vel)
			if (self.side == "r" and ball.vel[0] < 0):
				dy = ball.pos[1] - (self.pos[1]+self.h/2)
				dx = self.h/2.0
				alpha = math.atan(float(dy)/dx)
				vel = (ball.vel[0]**2+ball.vel[1]**2)**0.5
				vel = vel*main.VEL_INCREMENT
				if vel > main.MAX_VEL:
					vel = main.MAX_VEL
				ball.vel = (math.cos(alpha)*vel, math.sin(alpha)*vel)
			return True
		else:
			return False