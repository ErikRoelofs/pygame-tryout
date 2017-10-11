import animations, classes, dice, event, pygame, shiplibrary, sys, ui.mainscreen, ui.entity, ui.element, ui.shiplane, ui.container
from pygame.locals import *
from ui.actionbar import ActionBar
from ui.colors import *

"""
	- write out attack result
	- destruction
	- return fire
	- good animations
	- separate this part of the game into a module
	
"""

# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900

# margins, offsets, sizes
LEFT_MARGIN = 50
TOP_ROW = 50
BOTTOM_ROW = 400
ACTION_ROW = 650
CONFIRM_LEFT_MARGIN = 800
CONFIRM_TOP_MARGIN = 500

def main():

	global DISPLAYSURF, fontObj
	clock = pygame.time.Clock()

	# game setup
	mounts = (
		classes.Mount(classes.MOUNT_LIGHT, 2, 1),
		classes.Mount(classes.MOUNT_MEDIUM, 4, 2),
		classes.Mount(classes.MOUNT_HEAVY, 5, 3)
	)

	weaponTypes = (
		classes.WeaponType(classes.WEAPON_LASER),
		classes.WeaponType(classes.WEAPON_KINETIC),
		classes.WeaponType(classes.WEAPON_GUIDED)
	)

	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption('Game.')

	# setup vars
	mousex = 0
	mousey = 0	

	# make font
	fontObj = pygame.font.Font('freesansbold.ttf', 16)

	eventControl = event.EventControl()
	library = shiplibrary.Library(mounts, weaponTypes,eventControl)

	playerShips = [library.shipByName("Narf"),library.shipByName("Harf")]
	opponentShips = [library.shipByName("Narf"),library.shipByName("Darf")]
	eventControl.setShipLists(playerShips, opponentShips)

	main = ui.mainscreen.MainScreen((SCREEN_WIDTH, SCREEN_HEIGHT))
	controller = classes.BaseController(main, classes.PlayerTurnStrategy(playerShips, opponentShips), classes.PlayerTurnStrategy(opponentShips, playerShips), eventControl)

	playerLane = ui.shiplane.Shiplane(controller, playerShips, fontObj)
	main.addElement(ui.element.Element(playerLane, (LEFT_MARGIN, BOTTOM_ROW)))

	opponentLane = ui.shiplane.Shiplane(controller, opponentShips, fontObj)
	main.addElement(ui.element.Element(opponentLane, (LEFT_MARGIN, TOP_ROW)))

	main.addElement(ui.element.Element(ui.container.ActionBarContainer(fontObj, controller),(LEFT_MARGIN, ACTION_ROW)))
	main.addElement(ui.element.Element(ui.container.ConfirmActionContainer(fontObj, controller),(CONFIRM_LEFT_MARGIN, CONFIRM_TOP_MARGIN)))

	# main loop
	while True:

		mouseClicked = False

		for someEvent in pygame.event.get():
			if someEvent.type == QUIT:
				pygame.quit()
				sys.exit()
			if someEvent.type == MOUSEMOTION:
				mousex, mousey = someEvent.pos
			if someEvent.type == MOUSEBUTTONUP:
				mousex, mousey = someEvent.pos
				mouseClicked = True

		if turnShouldEnd(playerShips, opponentShips):
			nextTurn(playerShips, opponentShips)

		main.setMousePosition(mousex, mousey)
		if mouseClicked:
			main.clicked(mousex, mousey)

		DISPLAYSURF.blit(main.draw(), (0,0))

		trackCoords(fontObj, mousex, mousey, clock.get_fps())

		pygame.display.update()
		clock.tick(60)

def trackCoords(fontObj, mousex, mousey, fps):
		textSurfaceObj = fontObj.render(str(mousex) + ', ' + str(mousey) + ' @' + str(fps) + 'fps', True, GREEN, BLUE)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.right = SCREEN_WIDTH
		textRectObj.bottom = SCREEN_HEIGHT - 50
		DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def turnShouldEnd(playerShips, opponentShips):
	for ship in playerShips:
		if ship.available():
			return False
	for ship in opponentShips:
		if ship.available():
			return False
	return True	
	
def nextTurn(playerShips, opponentShips):
	for ship in playerShips:
		ship.refresh()
	for ship in opponentShips:
		ship.refresh()

if __name__ == '__main__':
    main()
