import pygame

class Entity():
    def __init__(self):
        self._surface = pygame.Surface((10,10))
        pygame.draw.rect(self._surface,(255,255,255),(0,0,10,10),2)

    def draw(self):
        return self._surface

    def update(self, dt):
        return True