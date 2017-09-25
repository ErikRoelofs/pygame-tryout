import pygame, sys
from pygame.locals import *

# colors
BG_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

# ship outline colors
OUTLINE_SPENT = (100, 100, 100)
OUTLINE_SLOW = (150, 150, 150)
OUTLINE_READY = (150, 255, 150)
OUTLINE_HIGHLIGHT = (0,255,0)

# ship states
STATE_READY = 1
STATE_SPENT = 2

# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900

# margins
LEFT_MARGIN = 50
SHIP_WIDTH = 200
SHIP_HEIGHT = 200
SHIP_GAP = 25

TOP_ROW = 50
BOTTOM_ROW = 400

def main():

	global DISPLAYSURF

	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption('Game.')

	# setup vars
	mousex = 0
	mousey = 0	
	
	# font test
	fontObj = pygame.font.Font('freesansbold.ttf', 32)
	
	playerShips = [makeShip(3), makeShip(3)]
	opponentShips = [makeShip(3)]

	selectedShip = None
	
	# main loop
	while True:

		mouseClicked = False
		
		DISPLAYSURF.fill(BG_COLOR)
			
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			if event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		hovered = getPlayerHoveredShip(mousex, mousey, playerShips)
		if mouseClicked and hovered:
			hovered.spend()
				
		trackCoords(fontObj, mousex, mousey)				
		drawShips(playerShips, opponentShips, hovered)
		
		pygame.display.update()

def trackCoords(fontObj, mousex, mousey):
		textSurfaceObj = fontObj.render(str(mousex) + ', ' + str(mousey), True, GREEN, BLUE)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.right = SCREEN_WIDTH
		textRectObj.bottom = SCREEN_HEIGHT		
		DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		
def makeShip(hull):
        return Ship(hull);

def drawShips(playerShips, opponentShips, highlighted):
	for index, ship in enumerate(playerShips):
		image = drawShip(ship, True if highlighted == ship else False)
		DISPLAYSURF.blit(image, getShipRectByIndex(index, True))

	for index, ship in enumerate(opponentShips):
		image = drawShip(ship, False)
		DISPLAYSURF.blit(image, getShipRectByIndex(index, False))
		
def drawShip(ship, highlighted):
	image = pygame.Surface((SHIP_WIDTH,SHIP_HEIGHT));
	
	outline_color = OUTLINE_SPENT if ship.state == STATE_SPENT else OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY
	
	pygame.draw.rect(image, outline_color, (0, 0, SHIP_WIDTH, SHIP_HEIGHT), 10)
	pygame.draw.circle(image, BLUE, (SHIP_WIDTH / 2, SHIP_HEIGHT / 2), SHIP_WIDTH / 4)
	return image	

def getShipRectByIndex(index, player):
	return pygame.Rect(LEFT_MARGIN + (SHIP_WIDTH + SHIP_GAP) * index, BOTTOM_ROW if player else TOP_ROW, SHIP_WIDTH, SHIP_HEIGHT)

def getPlayerHoveredShip(mousex, mousey, ships):
	for index, ship in enumerate(ships):
		rect = getShipRectByIndex(index, True)
		if rect.collidepoint(mousex,mousey):
			return ship
	return None
			
class Ship:
	def __init__(self, hull):
		self.hull = hull                
		self.damage = 0
		self.actions = []
		self.state = STATE_READY
		
	def spend(self):
		self.state = STATE_SPENT
		
	def refresh(self):
		self.state = STATE_READY

if __name__ == '__main__':
    main()
