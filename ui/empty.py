from entity import Entity

import pygame

class Empty(Entity):
    def __init__(self):
        self._surface = pygame.Surface((1,1))

    def draw(self):
        return self._surface

    def update(self, dt):
        return True

    def setMousePosition(self, mousex, mousey):
        return True

    def clicked(self, mousex, mousey):
        return True