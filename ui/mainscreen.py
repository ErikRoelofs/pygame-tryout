import pygame
import element as Element

BG_COLOR = (0, 0, 0)

class MainScreen():

    def __init__(self, size):
        self._surface = pygame.Surface(size)
        self.elements = [];

    def draw(self):
        self._surface.fill(BG_COLOR)
        for e in self.elements:
            self._surface.blit(e.entity.draw(), e.position)
        return self._surface

    def update(self, dt):
        for e in self.elements:
            e.entity.update(dt)

    def addElement(self, element):
        assert(isinstance(element, Element.Element ))
        self.elements.append(element)
