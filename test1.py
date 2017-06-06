import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Nin10do test')
clock = pygame.time.Clock()

meatboyfront = pygame.image.load('meatboyfront.png')

def meatboy(x,y):
	gameDisplay.blit(meatboyfront,(x,y))
	
x = (display_width * 0.2)
y = (display_height * 0.6)
x_move = 0
y_move = 0

crashed = False

while not crashed:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x_move = -5
			elif event.key == pygame.K_RIGHT:
				x_move = 5
			elif event.key == pygame.K_UP:
				y_move = -5
			elif event.key == pygame.K_DOWN:
				y_move = 5
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				x_move = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				y_move = 0
	
	x += x_move
	y += y_move
	
	gameDisplay.fill(black)
	meatboy(x,y)
	
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()