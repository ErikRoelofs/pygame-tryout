import pygame, ship, random

class Explode:
    def __init__(self, controller):
        temp = pygame.Surface((ship.SHIP_WIDTH,ship.SHIP_HEIGHT))
        self._surface = pygame.Surface.convert_alpha(temp)
        self.size = 10
        self.duration = 1000
        self.blasts = []
        self._controller = controller

    def update(self, dt):
        for blast in self.blasts:
            blast.update(dt)
            if(blast.shouldClean()):
                self.blasts.remove(blast)
        if random.randint(1,60) < dt:
            self._addExplosion()

        self.duration -= dt
        if self.duration <= 0:
            self._controller.done()

    def draw(self):
        self._surface.fill((0, 0, 0, 0))
        for blast in self.blasts:
            blast.draw(self._surface)
        return self._surface

    def _addExplosion(self):
        self.blasts.append(Explosion(random.randint(30, 170), random.randint(30, 170),  random.randint(1,10), random.randint(8, 40), random.randint(1,20)))

class Explosion:
    def __init__(self, x, y, initialSize, maxSize, growSpeed):
        self.x = x
        self.y = y
        self.size = initialSize
        self.maxSize = maxSize
        self.growSpeed = growSpeed

    def draw(self, surface):
        pygame.draw.circle(surface, self._getColor(), (self.x, self.y), self.size)

    def update(self, dt):
        self.size += dt / 7
        if self.size > self.maxSize:
            self.size = self.maxSize

    def shouldClean(self):
        return self.size >= self.maxSize

    def _getColor(self):
        alpha = ((self.maxSize - self.size) / float(self.maxSize)) * 255
        if alpha < 0:
            alpha = 0
        if alpha > 255:
            alpha = 255
        return (255, 0, 0, alpha)