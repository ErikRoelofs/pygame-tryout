import pygame, sys, random, animations, dice, classes, shiplibrary, event, traits
from pygame.locals import *

"""
	- traits
	- return fire
	- destruction
	- good animations
	- separate this part of the game into a module
	
"""

# colors
BG_COLOR = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

# ship outline colors
OUTLINE_SPENT = (100, 100, 100)
OUTLINE_SLOW = (150, 150, 150)
OUTLINE_READY = (150, 255, 150)
OUTLINE_HIGHLIGHT = (75,255,75)
OUTLINE_SELECTED = (0, 255, 0)


# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900

# margins, offsets, sizes
LEFT_MARGIN = 50
SHIP_WIDTH = 200
SHIP_HEIGHT = 200
SHIP_GAP = 25
TOP_ROW = 50
BOTTOM_ROW = 400
ACTION_ROW = 650
ACTION_WIDTH = 150
ACTION_HEIGHT = 150
ACTION_GAP = 25
CONFIRM_WIDTH = 200
CONFIRM_HEIGHT = 200
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
	selectedShip = None
	selectedAction = None
	selectedOpponent = None
	friendlyHovered = None
	opponentHovered = None
	actionHovered = None
	currentAnimations = []

	# make font
	fontObj = pygame.font.Font('freesansbold.ttf', 16)

	eventControl = event.EventControl()
	library = shiplibrary.Library(mounts, weaponTypes,eventControl)

	playerShips = [library.shipByName("Narf"),library.shipByName("Harf")]
	opponentShips = [library.shipByName("Narf"),library.shipByName("Darf")]
	eventControl.setShipLists(playerShips, opponentShips)

	# main loop
	while True:

		mouseClicked = False
		
		DISPLAYSURF.fill(BG_COLOR)

		trackCoords(fontObj, mousex, mousey, clock.get_fps())
		drawShips(playerShips, opponentShips, (selectedShip, selectedOpponent), (friendlyHovered, opponentHovered))

		for someEvent in pygame.event.get():
			if someEvent.type == QUIT:
				pygame.quit()
				sys.exit()
			if someEvent.type == MOUSEMOTION:
				mousex, mousey = someEvent.pos
			if someEvent.type == MOUSEBUTTONUP:
				mousex, mousey = someEvent.pos
				mouseClicked = True

		if not len(currentAnimations):
			if selectedAction:
				opponentHovered = getOpponentHoveredShip(mousex, mousey, opponentShips)
				if mouseClicked and opponentHovered:
					selectedOpponent = opponentHovered

			if selectedShip:
				actionHovered = hoveredAction(mousex, mousey, selectedShip.actions)
				drawActionBar(fontObj, selectedShip.actions, (selectedAction, ), (actionHovered, ))
				if mouseClicked and actionHovered:
					selectedAction = actionHovered
					selectedOpponent = None

			friendlyHovered = getPlayerHoveredShip(mousex, mousey, playerShips)
			if mouseClicked and friendlyHovered:
				selectedShip = friendlyHovered
				selectedAction = None
				selectedOpponent = None

			if selectedShip and selectedOpponent and selectedAction:
				confirmHovered = confirmButtonIsHovered(mousex,mousey)
				image = drawConfirmAction(fontObj, selectedShip, selectedAction, selectedOpponent, confirmHovered)
				DISPLAYSURF.blit(image, (CONFIRM_LEFT_MARGIN, CONFIRM_TOP_MARGIN))
				if mouseClicked and confirmHovered and selectedShip.available() and selectedAction.available():
					attack = selectedShip.performAttack(selectedAction, selectedOpponent)
					currentAnimations.append(animations.TestAnimation(getShipRectByShip(attack.attacker(), playerShips,True), getShipRectByShip(attack.target(), opponentShips, False), attack.weapon().mount.damage(), attack.weapon().rolls))
					currentAnimations.append(dice.DiceTray(fontObj, attack.results, attack.weapon().mount.accuracy()))
					selectedShip = None
					selectedAction = None
					selectedOpponent = None

		# there are animations; render them
		else:
			if mouseClicked:
				currentAnimations = []

			for animation in currentAnimations:
				DISPLAYSURF.blit(animation.surface(), animation.getPosition())
				animation.advance(clock.get_time())
				currentAnimations = [x for x in currentAnimations if not x.completed()]

			# when all animations finish, apply result of previous attack
			if not len(currentAnimations) and attack:
				attack.apply()
				attack = None

		if turnShouldEnd(playerShips, opponentShips):
			nextTurn(playerShips, opponentShips)

		pygame.display.update()
		clock.tick(60)

def trackCoords(fontObj, mousex, mousey, fps):
		textSurfaceObj = fontObj.render(str(mousex) + ', ' + str(mousey) + ' @' + str(fps) + 'fps', True, GREEN, BLUE)
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.right = SCREEN_WIDTH
		textRectObj.bottom = SCREEN_HEIGHT		
		DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawShips(playerShips, opponentShips, selected, highlighted):
	for index, ship in enumerate(playerShips):
		image = drawShip(ship, ship in selected, ship in highlighted)
		DISPLAYSURF.blit(image, getShipRectByIndex(index, True))

	for index, ship in enumerate(opponentShips):
		image = drawShip(ship, ship in selected, ship in highlighted)
		DISPLAYSURF.blit(image, getShipRectByIndex(index, False))
		
def drawShip(ship, selected, highlighted):
	image = pygame.Surface((SHIP_WIDTH,SHIP_HEIGHT))
	
	outline_color = OUTLINE_SELECTED if selected else OUTLINE_SPENT if not ship.available() else OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY
	
	pygame.draw.rect(image, outline_color, (0, 0, SHIP_WIDTH, SHIP_HEIGHT), 10)
	pygame.draw.circle(image, BLUE, (SHIP_WIDTH // 2, SHIP_HEIGHT // 2), SHIP_WIDTH // 4)

	nameSurfaceObj = fontObj.render(str(ship.name()), True, WHITE)
	nameRectObj = nameSurfaceObj.get_rect()
	nameRectObj.left = 10
	nameRectObj.top = SHIP_HEIGHT - 25
	image.blit(nameSurfaceObj, nameRectObj)

	textSurfaceObj = fontObj.render(str(ship.hull - ship.damage) + ' / ' + str(ship.hull), True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.left = SHIP_WIDTH - 40
	textRectObj.top = SHIP_HEIGHT - 25
	image.blit(textSurfaceObj, textRectObj)

	return image	

def drawActionBar(fontObj, actions, selected, highlighted):
	for index, action in enumerate(actions):
		image = drawWeapon(fontObj, action, action in selected, action in highlighted)
		DISPLAYSURF.blit(image, getActionSlot(index))

def getActionSlot(index):
	return pygame.Rect(LEFT_MARGIN + (ACTION_WIDTH + ACTION_GAP) * index, ACTION_ROW, ACTION_WIDTH, ACTION_HEIGHT)

def drawWeapon(fontObj, weapon, selected, highlighted):
	image = pygame.Surface((ACTION_WIDTH,ACTION_HEIGHT))
	outline_color = OUTLINE_SELECTED if selected else OUTLINE_SPENT if not weapon.available() else OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY
	pygame.draw.rect(image, outline_color, (0, 0, ACTION_WIDTH, ACTION_HEIGHT), 10)

	rollsImg = drawWeaponRolls(weapon.rolls)
	rollsRect = rollsImg.get_rect()
	rollsRect.center = (ACTION_WIDTH / 4, ACTION_HEIGHT / 2 )
	image.blit(rollsImg, rollsRect)

	mountImg = drawMount(weapon.mount)
	mountRect = mountImg.get_rect()
	mountRect.center = (ACTION_WIDTH / 2, ACTION_HEIGHT / 2)
	image.blit(mountImg, mountRect)

	weaponTypeImg = drawWeaponType(weapon.weaponType)
	weaponTypeRect = weaponTypeImg.get_rect()
	weaponTypeRect.center = (ACTION_WIDTH / 4 * 3, ACTION_HEIGHT / 2)
	image.blit(weaponTypeImg, weaponTypeRect)

	return image

def drawMount(mount):
	assert mount.classification() in (classes.MOUNT_LIGHT, classes.MOUNT_MEDIUM, classes.MOUNT_HEAVY), "Pass a MOUNT to the drawMount function."

	image = pygame.Surface((40,40))
	pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)
	
	text = "L" if mount.classification() == classes.MOUNT_LIGHT else "M" if mount.classification() == classes.MOUNT_MEDIUM else "H"

	textSurfaceObj = fontObj.render(text, True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (20, 20)
	image.blit(textSurfaceObj, textRectObj)
	
	return image

def drawWeaponType(weaponType):
	assert weaponType.isOneOf((classes.WEAPON_KINETIC, classes.WEAPON_LASER, classes.WEAPON_GUIDED)), "Pass a WEAPONTYPE to the drawWeaponType function."

	image = pygame.Surface((40,40))
	pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)
	
	text = "K" if weaponType.isType(classes.WEAPON_KINETIC) else "L" if weaponType.isType( classes.WEAPON_LASER ) else "G"

	textSurfaceObj = fontObj.render(text, True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (20, 20)
	image.blit(textSurfaceObj, textRectObj)
	
	return image

def drawWeaponRolls(rolls):

	image = pygame.Surface((40, 40))
	pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)

	textSurfaceObj = fontObj.render(str(rolls), True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (20, 20)
	image.blit(textSurfaceObj, textRectObj)

	return image

def drawConfirmAction(fontObj, ship, weapon, target, highlighted):
	image = pygame.Surface((CONFIRM_WIDTH,CONFIRM_HEIGHT))

	outline_color = OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY if ship.available() and weapon.available() else OUTLINE_SPENT
	pygame.draw.rect(image, outline_color, (0, 0, CONFIRM_WIDTH, CONFIRM_HEIGHT), 10)

	textSurfaceObj = fontObj.render('FIRE!', True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (CONFIRM_WIDTH / 2, CONFIRM_HEIGHT /2)
	image.blit(textSurfaceObj, textRectObj)
	
	return image

def confirmButtonIsHovered(mousex, mousey):
	return pygame.Rect(CONFIRM_LEFT_MARGIN, CONFIRM_TOP_MARGIN, CONFIRM_WIDTH, CONFIRM_HEIGHT).collidepoint(mousex, mousey)

def getShipRectByShip(ship, list, player):
	for index, someShip in enumerate(list):
		if ship == someShip:
			return getShipRectByIndex(index, player)

def getShipRectByIndex(index, player):
	return pygame.Rect(LEFT_MARGIN + (SHIP_WIDTH + SHIP_GAP) * index, BOTTOM_ROW if player else TOP_ROW, SHIP_WIDTH, SHIP_HEIGHT)

def getPlayerHoveredShip(mousex, mousey, ships):
	return getHoveredShip(mousex, mousey, ships, True)

def getOpponentHoveredShip(mousex, mousey, ships):
	return getHoveredShip(mousex, mousey, ships, False)
		
def getHoveredShip(mousex, mousey, ships, player):
	for index, ship in enumerate(ships):
		rect = getShipRectByIndex(index, player)
		if rect.collidepoint(mousex,mousey):
			return ship
	return None

def hoveredAction(mousex, mousey, actions):
	for index, action in enumerate(actions):
		rect = getActionSlot(index)
		if rect.collidepoint(mousex, mousey):
			return action
	return None

def turnShouldEnd(playerShips, opponentShips):
	for ship in playerShips:
		if ship.available():
			return False
#	for ship in opponentShips:
#		if ship.available():
#			return False
	return True	
	
def nextTurn(playerShips, opponentShips):
	for ship in playerShips:
		ship.refresh()
	for ship in opponentShips:
		ship.refresh()

if __name__ == '__main__':
    main()
