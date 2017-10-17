import entity, pygame, classes
from colors import *
# classes needs to go

SHIP_WIDTH = 200
SHIP_HEIGHT = 200


class Ship(entity.Entity):
    def __init__(self, controller, ship, font):
        self._surface = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))
        self._ship = ship
        self.font = font
        self._highlighted = False
        self._selected = False
        self._modified = True
        self._animation = None

    def draw(self):
        if self._modified:
            self.redraw()
        return self._surface

    def redraw(self):
        image = drawShip(self.font, self._ship, self._selected, self._highlighted)
        self._surface.blit(image, (0,0))
        self._modified = False

    def update(self, dt):
        return True

    def highlight(self, value):
        if self._highlighted != value:
            self._highlighted = value
            self._modified = True

    def selected(self, value):
        if self._selected != value:
            self._selected = value
            self._modified = True

    def ship(self):
        return self._ship

def drawShip(font, ship, selected, highlighted):
    image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))

    outline_color = OUTLINE_SELECTED if selected else OUTLINE_SPENT if not ship.available() else OUTLINE_HIGHLIGHT if highlighted else OUTLINE_READY

    pygame.draw.rect(image, outline_color, (0, 0, SHIP_WIDTH, SHIP_HEIGHT), 10)
    pygame.draw.circle(image, BLUE, (SHIP_WIDTH // 2, SHIP_HEIGHT // 2), SHIP_WIDTH // 4)

    nameSurfaceObj = font.render(str(ship.name()), True, WHITE)
    nameRectObj = nameSurfaceObj.get_rect()
    nameRectObj.left = 10
    nameRectObj.top = SHIP_HEIGHT - 25
    image.blit(nameSurfaceObj, nameRectObj)

    textSurfaceObj = font.render(str(ship.hull - ship.damage) + ' / ' + str(ship.hull), True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = SHIP_WIDTH - 40
    textRectObj.top = SHIP_HEIGHT - 25
    image.blit(textSurfaceObj, textRectObj)

    for key, trait in enumerate(ship.traits):
        textSurfaceObj = drawTrait(font, trait)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.left = 10
        textRectObj.top = SHIP_HEIGHT - 45 - (20 * key)
        image.blit(textSurfaceObj, textRectObj)

    return image


def drawTrait(font, trait):
    textSurfaceObj = font.render(trait.writeTrait(), True, WHITE)
    return textSurfaceObj