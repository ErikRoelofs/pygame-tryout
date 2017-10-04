import entity, pygame, ship

SHIP_GAP = 25

class Shiplane(entity.Entity):
    def __init__(self, ships, font):
        self._size = (750,200)
        self._surface = pygame.Surface(self._size)
        self.font = font
        self.ships = ships
        self._mousePosition = None

    def draw(self):
        for index, theShip in enumerate(self.ships):
            shipEntity = ship.Ship(theShip, self.font)
            xmin = index * (SHIP_GAP + ship.SHIP_WIDTH)
            xmax = xmin + ship.SHIP_WIDTH
            ymin = 0
            ymax = ymin + ship.SHIP_HEIGHT
            shipEntity.highlight(self._mousePosition and xmin < self._mousePosition[0] <= xmax and ymin < self._mousePosition[1] < ymax)

            self._surface.blit(shipEntity.draw(), (index * (SHIP_GAP + ship.SHIP_WIDTH), 0))
        return self._surface

    def update(self, dt):
        return True

    def setMousePosition(self, mousex, mousey):
        if mousex >= 0 and mousex <= self._size[0] and mousey >= 0 and mousey <= self._size[1]:
            self._mousePosition = (mousex, mousey)
        else:
            self._mousePosition = None