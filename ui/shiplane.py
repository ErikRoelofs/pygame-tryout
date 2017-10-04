import entity, pygame, ship

SHIP_GAP = 25

class Shiplane(entity.Entity):
    def __init__(self, font):
        self._surface = pygame.Surface((750, 200))
        self.ships = []
        self.font = font

    def draw(self):
        for index, theShip in enumerate(self.ships):
            self._surface.blit(theShip.draw(), (index * (SHIP_GAP + ship.SHIP_WIDTH), 0))
        return self._surface

    def update(self, dt):
        return True

    def addShip(self, theShip):
        self.ships.append(ship.Ship(theShip, self.font))

    def addShips(self, ships):
        for theShip in ships:
            self.ships.append(ship.Ship(theShip, self.font))