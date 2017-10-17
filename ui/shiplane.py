import entity, pygame, ship
from colors import *

SHIP_GAP = 25

class Shiplane(entity.Entity):
    def __init__(self, controller, ships, font):
        self._controller = controller
        controller.addListener(self, [])
        self._size = (750,200)
        self._surface = pygame.Surface(self._size)
        self.font = font
        self.ships = ships
        self.shipUIs = []
        for index, theShip in enumerate(self.ships):
            self.shipUIs.append( ship.Ship(controller, theShip, self.font) )

        self._mousePosition = None
        self._mouseClicked = False

    def draw(self):
        self._surface.fill(BG_COLOR)

        for index, ui in enumerate(self.shipUIs):
            self._surface.blit(ui.draw(), (index * (SHIP_GAP + ship.SHIP_WIDTH), 0))

        self._mouseClicked = False
        return self._surface

    def update(self, dt):
        for ui in self.shipUIs:
            ui.update(dt)

    def setMousePosition(self, mousex, mousey):
        self.unhighlightAll()
        if mousex >= 0 and mousex <= self._size[0] and mousey >= 0 and mousey <= self._size[1]:
            self._mousePosition = (mousex, mousey)
            theShip = self.findUIAtPosition(mousex, mousey)
            if theShip:
                self._controller.shipHovered(theShip)
        else:
            self._mousePosition = None


    def clicked(self, x, y):
        ship = self.findUIAtPosition(x,y)
        if ship:
            self._controller.shipClicked(ship)

    def findUIAtPosition(self, x, y):
        for index, theShip in enumerate(self.shipUIs):
            xmin = index * (SHIP_GAP + ship.SHIP_WIDTH)
            xmax = xmin + ship.SHIP_WIDTH
            ymin = 0
            ymax = ymin + ship.SHIP_HEIGHT
            if xmin < x <= xmax and ymin < y < ymax:
                return theShip

    def findShipAtPosition(self, x, y):
        return self.findUIAtPosition(x,y).ship()

    def unhighlightAll(self):
        for ship in self.shipUIs:
            ship.highlight(False)

    def event(self, name, target):
        if name == "all-unselected":
            for ship in self.shipUIs:
                ship.selected(False)

        if name == "player-selected" or name == "opponent-selected":
            if not target in self.shipUIs:
                return
            for ship in self.shipUIs:
                if ship == target:
                    ship.selected(True)
                else:
                    ship.selected(False)
        if name == "hovered":
            for ship in self.shipUIs:
                if ship == target:
                    ship.highlight(True)
                else:
                    ship.highlight(False)

        if name == "destroyed":
            for ui in self.shipUIs:
                if ui.ship() == target:
                    self.shipUIs.remove(ui)

    def findUIForShip(self, ship):
        for ui in self.shipUIs:
            if ui.ship() == ship:
                return ui