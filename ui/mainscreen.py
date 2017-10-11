import pygame
import element as Element
from colors import *

class MainScreen():

    def __init__(self, size):
        self._surface = pygame.Surface(size)
        self.elements = []
        self._mousePosition = None
        self._size = size

    def setController(self, controller):
        self._controller = controller

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

    def setMousePosition(self, mousex, mousey):
        if mousex >= 0 and mousex <= self._size[0] and mousey >= 0 and mousey <= self._size[1]:
            self._mousePosition = (mousex, mousey)
        else:
            self._mousePosition = None
        for child in self.elements:
            child.entity.setMousePosition(mousex - child.position[0], mousey - child.position[1])

    def clicked(self, mousex, mousey):
        for child in self.elements:
            child.entity.clicked(mousex - child.position[0], mousey - child.position[1])