import pygame, random;

class TestAnimation:
    def __init__(self, origin, target, size, amount ):
        assert isinstance(origin, pygame.Rect), "origin should be a Rect"
        assert isinstance(target, pygame.Rect), "target should be a Rect"
        self.origin = origin
        self.target = target
        self.size = size
        self.amount = amount
        self.timer = 0
        self.lastDrawn = 0

        width, height = self._getSurfaceSize()
        image = pygame.Surface((width, height))
        image = image.convert_alpha()

        self.__surface = image

    def _getSurfaceSize(self):
        position = self.getPosition()
        right = max(self.origin.right, self.target.right)
        bottom = max(self.origin.bottom, self.target.bottom)
        return (right - position[0], bottom - position[1])

    # the redraw method updates the surface with the new state of the animation
    def redraw(self):
        width, height = self._getSurfaceSize()
        self.__surface.fill((0, 0, 0, 0))

        for i in range(self.amount):
            self.drawBeam()

        outline_color = (255,0,0,255)
        pygame.draw.rect(self.__surface, outline_color, (0, 0, width, height), 10)
        return self.__surface

    # the surface method returns an image that should be drawn to the screen, positioned using the getPosition function
    def surface(self):
        return self.__surface

    # this returns the top-left coordinate of origin/target, which should give us the position on the screen where the image should go.
    def getPosition(self):
        return (min(self.origin.left, self.target.left), min(self.origin.top, self.target.top))

    def advance(self, dt):
        self.timer += dt
        if self.timer > self.lastDrawn:
            self.redraw()
            self.lastDrawn += 250

    def randomSurfacePointInTarget(self):
        position = self.getPosition()
        return (
            random.randint(self.target.left, self.target.right) - position[0],
            random.randint(self.target.top, self.target.bottom) - position[1])

    def randomSurfacePointInOrigin(self):
        position = self.getPosition()
        return (
            random.randint(self.origin.left, self.origin.right) - position[0],
            random.randint(self.origin.top, self.origin.bottom) - position[1])

    def drawBeam(self):
        impact = self.randomSurfacePointInTarget()
        pygame.draw.line(self.__surface, (255,0,0,255), self.randomSurfacePointInOrigin(), impact, self.size)
        pygame.draw.circle(self.__surface, (255, 0, 0, 255), impact, self.size*3)
