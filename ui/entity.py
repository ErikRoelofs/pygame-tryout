import pygame
from colors import *

class Entity():
    def __init__(self):
        self._surface = pygame.Surface((10,10))
        pygame.draw.rect(self._surface,WHITE,(0,0,10,10),2)

    def draw(self):
        return self._surface

    def update(self, dt):
        return True

    def setMousePosition(self, mousex, mousey):
        raise NotImplementedError("Should implement setMousePosition (it takes int, int)")

    def clicked(self, mousex, mousey):
        raise NotImplementedError("Should implement clicked (it takes int, int)")