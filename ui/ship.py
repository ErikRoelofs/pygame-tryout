import entity, pygame, classes
# classes needs to go

SHIP_WIDTH = 200
SHIP_HEIGHT = 200

# ship outline colors - do not belong here
OUTLINE_SPENT = (100, 100, 100)
OUTLINE_SLOW = (150, 150, 150)
OUTLINE_READY = (150, 255, 150)
OUTLINE_HIGHLIGHT = (75,255,75)
OUTLINE_SELECTED = (0, 255, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)


class Ship(entity.Entity):
    def __init__(self, ship, font):
        self._surface = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))
        self.ship = ship
        self.font = font

    def draw(self):
        return drawShip(self.font, self.ship, False, False)
        #self._surface.blit(image, (0,0))
        #return self._surface

    def update(self, dt):
        return True


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