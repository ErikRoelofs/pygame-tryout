import pygame

class ActionBar:
    def __init__(self, controller, actions):
        self._controller = controller
        controller.addListener(self, [])
        self._size = (750,200)
        self._surface = pygame.Surface(self._size)

    def draw(self):
        self.unhighlightAll()
        if self._mousePosition:
            theShip = self.findUIAtPosition(self._mousePosition[0], self._mousePosition[1])
            if theShip:
                theShip.highlight(True)

        for index, ui in enumerate(self.shipUIs):
            self._surface.blit(ui.draw(), (index * (SHIP_GAP + ship.SHIP_WIDTH), 0))

        self._mouseClicked = False
        return self._surface

    def update(self, dt):
        return True
