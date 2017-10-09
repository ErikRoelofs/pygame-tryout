import pygame, classes

ACTION_WIDTH = 150
ACTION_HEIGHT = 150
ACTION_GAP = 25

OUTLINE_SPENT = (100, 100, 100)
OUTLINE_SLOW = (150, 150, 150)
OUTLINE_READY = (150, 255, 150)
OUTLINE_HIGHLIGHT = (75,255,75)
OUTLINE_SELECTED = (0, 255, 0)

BG_COLOR = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

class ActionBar:
    def __init__(self, controller, actions, fontObj):
        self._fontObj = fontObj
        self._controller = controller
        controller.addListener(self, [])
        self._size = (750,200)
        self._surface = pygame.Surface(self._size)
        self.actions = actions

    def draw(self):
        for index, action in enumerate(self.actions):
            image = drawWeapon(self._fontObj, action, False, False)
            self._surface.blit(image, (index * (ACTION_GAP + ACTION_WIDTH), 0))

        return self._surface

    def update(self, dt):
        return True

    def event(self, name, data):
        True


def drawWeapon(fontObj, weapon, selected, highlighted):
    image = pygame.Surface((ACTION_WIDTH, ACTION_HEIGHT))
    outline_color = OUTLINE_SELECTED if selected else OUTLINE_SPENT if not weapon.available() else OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY
    pygame.draw.rect(image, outline_color, (0, 0, ACTION_WIDTH, ACTION_HEIGHT), 10)

    rollsImg = drawWeaponRolls(fontObj, weapon.rolls)
    rollsRect = rollsImg.get_rect()
    rollsRect.center = (ACTION_WIDTH / 4, ACTION_HEIGHT / 2)
    image.blit(rollsImg, rollsRect)

    mountImg = drawMount(fontObj, weapon.mount)
    mountRect = mountImg.get_rect()
    mountRect.center = (ACTION_WIDTH / 2, ACTION_HEIGHT / 2)
    image.blit(mountImg, mountRect)

    weaponTypeImg = drawWeaponType(fontObj, weapon.weaponType)
    weaponTypeRect = weaponTypeImg.get_rect()
    weaponTypeRect.center = (ACTION_WIDTH / 4 * 3, ACTION_HEIGHT / 2)
    image.blit(weaponTypeImg, weaponTypeRect)

    return image


def drawMount(fontObj, mount):
    assert mount.classification() in (
    classes.MOUNT_LIGHT, classes.MOUNT_MEDIUM, classes.MOUNT_HEAVY), "Pass a MOUNT to the drawMount function."

    image = pygame.Surface((40, 40))
    pygame.draw.rect(image, BLUE, (0, 0, 40, 40), 3)

    text = "L" if mount.classification() == classes.MOUNT_LIGHT else "M" if mount.classification() == classes.MOUNT_MEDIUM else "H"

    textSurfaceObj = fontObj.render(text, True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (20, 20)
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
