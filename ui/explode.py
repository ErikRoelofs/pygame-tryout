import pygame, ship

class Explode:
    def __init__(self):
        temp = pygame.Surface((ship.SHIP_WIDTH,ship.SHIP_HEIGHT))
        self._surface = pygame.Surface.convert_alpha(temp)
        self.size = 10
        self.blasts = []

    def update(self, dt):
        for blast in self.blasts:
            blast.update(dt)
        # clean blasts

    def draw(self):
        self._surface.fill((0, 0, 0, 0))
        for blast in self.blasts:
            blast.draw(self._surface)
        return self._surface

    def _addExplosion(self):
        self.blasts.append()

class Explosion:
    def __init__(self, x, y, initialSize, maxSize, growSpeed):
        self.x = x
        self.y = y
        self.size = initialSize
        self.maxSize = maxSize
        self.growSpeed = growSpeed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.size)

    def update(self, dt):
        self.size += dt * self.growSpeed
        if self.size > self.maxSize:
            self.size = self.maxSize