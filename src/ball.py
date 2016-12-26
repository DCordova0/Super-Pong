import pygame, numpy, main

class Ball: 
	def __init__(self,x,y,r, vel):
		self.pos = (x, y)
		self.r = r
		self.vel = vel
		self.color = main.WHITE
		self.image = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA, 32)
		pygame.draw.circle(self.image, self.color, (self.r,self.r), self.r)

	def draw(self, screen):
		screen.blit(self.image, numpy.subtract(self.pos, (self.r, self.r)))

	def update(self):
		# Choque con bordes superior e inferior.
		if self.pos[1] + self.r > main.BOT:
			self.vel = (self.vel[0], -self.vel[1])
		if self.pos[1] - self.r < main.TOP:
			self.vel = (self.vel[0], -self.vel[1])

		#Actualizar velocidad
		self.pos = numpy.add(self.pos, self.vel)

	#Si la bola esta fuera de la pantalla
	def out(self):
		if self.pos[0]-self.r > main.SCREEN_WIDTH:
			return 2
		if self.pos[0]+self.r < 0:
			return 1
		return 0

if __name__ == "__main__":
	print "Hola"