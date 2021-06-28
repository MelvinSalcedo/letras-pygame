import pygame
import random
pygame.init()

w,h = 800,600
screen = pygame.display.set_mode((w, h))

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Futura', 30)
numeroTotalVidas=0

diff_ticks = 20
ticks = pygame.time.get_ticks() + diff_ticks
word_diff_ticks = 1000
word_ticks = pygame.time.get_ticks() + word_diff_ticks

clock = pygame.time.Clock()
FPS = 60

nuves = pygame.image.load("sky_cloud.png").convert_alpha()

mover_izquierda = False
mover_derecha = False

grupoLetrasEnemigos = pygame.sprite.Group()

EnemigosLetras=[]


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
	screen.blit(nuves,(0,0))#5,0 ....150,0

class Texto(pygame.sprite.Sprite): 
	def __init__(self, my_str):#a,b,s,f,df,hg,sdf,
		pygame.sprite.Sprite.__init__(self)

		self.font = pygame.font.SysFont('Futura', 55)
		self.my_str = my_str# Modifica la lista de letras que quieras
		self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))#Color aleatorio =(0,200,330)
		
		self.word=ord(self.my_str)
		#self.inicializarCadenaTexto()

		self.image = self.font.render(chr(self.word),True,self.color)
		self.rect = self.image.get_rect()# las coordenadas x son aleatorias de 100 a los márgenes izquierdo y derecho
		self.rect.x=random.randint(0,w-100)

	def inicializarCadenaTexto(self):# m 45
		if ord(self.my_str) != 32: # Saltar espacios
			self.word=ord(self.my_str)
		
	def update(self):
		self.rect.y+=1

		self.verificarColision()

		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #(1,1,1)
		self.image = self.font.render(chr(self.word),True,self.color)

		if(self.rect.y>h+10):
			self.kill()

	def verificarColision(self):
		#verificamos si a colisionado con alguien
		if pygame.sprite.spritecollide(player, grupoLetrasEnemigos, False ,pygame.sprite.pygame.sprite.collide_circle_ratio(.8)):
			player.puntaje+=1
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		r=random.randint(0,2) #0 1 2
		self.image = pygame.image.load(f'{r}.png')

		self.rect = self.image.get_rect()# las coordenadas x son aleatorias de 100 a los márgenes izquierdo y derecho
		self.rect.x=random.randint(0,w-100)
	def update(self):
		self.rect.y+=5

		self.verificarColision()
		if(self.rect.y>h+10):
			self.kill()

	def verificarColision(self):
		#verificamos si a colisionado con alguien
		if pygame.sprite.spritecollide(player, grupoLetrasEnemigos , False ,pygame.sprite.pygame.sprite.collide_circle_ratio(.8)):
			player.vida-=1
			self.kill()

	


class Player(pygame.sprite.Sprite): # 

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		img2 = pygame.image.load("pacman.png")
		self.image = pygame.transform.scale(img2, (int(img2.get_width() * 2), int(img2.get_height() * 2)))
		self.rect = self.image.get_rect()# las coordenadas x son aleatorias de 100 a los márgenes izquierdo y derecho
		self.rect.center=(400,550)

		self.velocidad=10
		self.puntaje=0
		self.vida=15

	def mover_player(self, moving_left, moving_right):
		#reseteamos las variables de movimiento
		dx = 0#-10
		dy = 0

		#si 
		if moving_left:
			dx = -self.velocidad
		if moving_right:
			dx = self.velocidad
		self.rect.x += dx

	def draw(self):
		screen.blit(self.image, self.rect)

class CastearEnemigosLetras(pygame.sprite.Sprite):
	def __init__(self,numLetras):
		pygame.sprite.Sprite.__init__(self)

		self.numLetras=numLetras

		self.numeroTotalVidas=self.crearEnemigosLetras()
		
		self.tiempoObtenido = pygame.time.get_ticks()

	def crearEnemigosLetras(self):
		numL=0
		for x in range(self.numLetras):
			r1=random.randint(0,1)
			
			if(r1==0):
				r=random.randint(35,90) #5
				texto=Texto(chr(r))#a
				EnemigosLetras.append(texto)
				numL+=1
			else:
				enemy=Enemy()
				EnemigosLetras.append(enemy)			
			#grupoEnemigos.add(enemy)
		return numL

	def agregarRenderizar(self):
		ANIMATION_COOLDOWN = 400
		if pygame.time.get_ticks() - self.tiempoObtenido > ANIMATION_COOLDOWN:
			self.tiempoObtenido = pygame.time.get_ticks()
			if(len(EnemigosLetras)!=0):
				grupoLetrasEnemigos.add(EnemigosLetras.pop())
						
run = True
castearEnemigosLetras=CastearEnemigosLetras(400)


player=Player()

while run:
	clock.tick(FPS)
	###################EVENTOS###################
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN: #presionanadose sin soltar
			if event.key == pygame.K_a:
				mover_izquierda = True
			if event.key == pygame.K_d:
				mover_derecha = True
			if event.key == pygame.K_ESCAPE:
				run = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				mover_izquierda = False
			if event.key == pygame.K_d:
				mover_derecha = False

	##########################LOGICA delk JUEGO########
	if(player.vida>=1):
		player.mover_player(mover_izquierda,mover_derecha)
	else:
		player.mover_player(False,False)


	grupoLetrasEnemigos.update()
	############RENDER####################
	
	draw_bg() # dibujar el fondo

	grupoLetrasEnemigos.draw(screen)
	

	player.draw()
	draw_text('Puntaje: '+f'{player.puntaje}/{castearEnemigosLetras.numeroTotalVidas}', font, WHITE, 20, 10)
	draw_text('Vida: '+f'{player.vida}', font, WHITE, 20, 40)

	if(player.vida<=0):
		draw_text('Perdiste', font, RED, 400, 300)
	if(player.puntaje==castearEnemigosLetras.numeroTotalVidas):
		draw_text('Ganaste', font, GREEN, 400, 300)

	castearEnemigosLetras.agregarRenderizar()

	

	pygame.display.flip()# actualizar pantalla
pygame.quit()