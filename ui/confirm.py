import pygame
import classes
from entity import Entity
from colors import *

CONFIRM_WIDTH = 200
CONFIRM_HEIGHT = 200
CONFIRM_LEFT_MARGIN = 800
CONFIRM_TOP_MARGIN = 500

class Confirm(Entity):
    def __init__(self, controller, fontObj, ship, weapon, target):
        self._controller = controller
        self._size = (CONFIRM_WIDTH,CONFIRM_HEIGHT)
        self._surface = pygame.Surface(self._size)
        self._fontObj = fontObj
        self.ship = ship
        self.weapon = weapon
        self.target = target
        self._highlighted = False
        self._mousePosition = None

    def draw(self):
        highlighted = True if self._mousePosition else False
        return drawConfirmAction(self._fontObj, self.ship, self.weapon, self.target, highlighted)

    def clicked(self, mousex, mousey):
        if 0 <= mousex <= self._size[0] and 0 <= mousey <= self._size[1]:
            self._controller.actionConfirmed()

    def setMousePosition(self, mousex, mousey):
        if 0 <= mousex <= self._size[0] and 0 <= mousey <= self._size[1]:
            self._mousePosition = (mousex,mousey)
        else:
            self._mousePosition = None

    def highlight(self, value):
        self._highlighted = value

def drawConfirmAction(fontObj, ship, weapon, target, highlighted):
	image = pygame.Surface((CONFIRM_WIDTH,CONFIRM_HEIGHT))

	outline_color = OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY if ship.available() and weapon.available() else OUTLINE_SPENT
	pygame.draw.rect(image, outline_color, (0, 0, CONFIRM_WIDTH, CONFIRM_HEIGHT), 10)

	attack = ship.performAttack(weapon, target)
	rolls = drawWeaponRolls(fontObj, attack.weapon().rolls)
	image.blit(rolls, (50, 50))
	weaponType = drawWeaponType(fontObj, attack.weapon().weaponType)
	image.blit(weaponType, (100, 50))
	damage = drawWeaponStats(fontObj, attack.weapon())
	image.blit(damage, (100, 50))

	textSurfaceObj = fontObj.render('FIRE!', True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (CONFIRM_WIDTH / 2, CONFIRM_HEIGHT * 3/4)
	image.blit(textSurfaceObj, textRectObj)

	return image

def drawWeaponType(fontObj, weaponType):
    assert weaponType.isOneOf((classes.WEAPON_KINETIC, classes.WEAPON_LASER,
                               classes.WEAPON_GUIDED)), "Pass a WEAPONTYPE to the drawWeaponType function."

    image = pygame.Surface((40, 40))
    pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)

    text = "K" if weaponType.isType(classes.WEAPON_KINETIC) else "L" if weaponType.isType(classes.WEAPON_LASER) else "G"

    textSurfaceObj = fontObj.render(text, True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (20, 20)
    image.blit(textSurfaceObj, textRectObj)

    return image


def drawWeaponRolls(fontObj, rolls):
    image = pygame.Surface((40, 40))
    pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)

    textSurfaceObj = fontObj.render(str(rolls), True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (20, 20)
    image.blit(textSurfaceObj, textRectObj)

    return image

def drawWeaponStats(fontObj, weapon):
	image = pygame.Surface((80, 40))
	pygame.draw.rect(image, BLUE, (0, 0, 80, 40), 3)

	textSurfaceObj = fontObj.render(str(weapon.mount.accuracy()), True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (20, 20)
	image.blit(textSurfaceObj, textRectObj)

	textSurfaceObj = fontObj.render(str(weapon.mount.damage()), True, WHITE)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (50, 20)
	image.blit(textSurfaceObj, textRectObj)

	return image
