import animations, pygame, random;

BACKGROUND = ( 0,0,0,0 )
WHITE = ( 255, 255, 255 )
HIT = ( 0, 255, 0)
MISS = ( 255, 0, 0)

DICE_MARGIN = 100
DICE_ROW = 650
DICE_WIDTH = 50
DICE_HEIGHT = 50
DICE_GAP = 15
DICE_THICKNESS = 5

class DiceTray(animations.Animation):

    def __init__(self, fontObj, results, required):
        self.fontObj = fontObj
        self.results = results
        self.required = required
        self.dice = []
        for i, result in enumerate(results):
            self.dice.append(Die(fontObj, result, required, i))

        self.__surface = pygame.Surface(( (DICE_WIDTH + DICE_GAP) * len(self.results), DICE_HEIGHT ))
        self.redraw()

    def surface(self):
        return self.__surface

    def advance(self, dt):
        result = False
        for die in self.dice:
            result = result or die.advance(dt)
        if result:
            self.redraw()

    def redraw(self):
        for i, die in enumerate(self.dice):
            image = die.surface()
            self.__surface.blit(image, ( (DICE_WIDTH + DICE_GAP ) * i, 0))

    def getPosition(self):
        return (DICE_MARGIN, DICE_ROW)

class Die(animations.Animation):

    def __init__(self, fontObj, result, required, slotnum):
        self.result = result
        self.required = required
        self.slotnum = slotnum
        self.fontObj = fontObj
        self.__surface = pygame.Surface((DICE_WIDTH,DICE_HEIGHT))
        self.timer = 0
        self.lastDrawn = 0
        self.maxDuration = 2000
        self.delay = 25
        self.delayDx = 10
        self._redraw(False)

    def surface(self):
        return self.__surface

    def advance(self, dt):
        self.timer += dt
        if self.timer > self.maxDuration:
            self._redraw(True)
            return True
        elif self.timer > self.lastDrawn:
            self._redraw(False)
            self.lastDrawn += self.delay
            self.delay = self.delay + self.delayDx
            return True
        return False

    def _redraw(self, final):
        self.__surface.fill(BACKGROUND)

        if final:
            roll = self.result
        else:
            roll = random.randint(1,6)

        color = HIT if roll >= self.required else MISS

        pygame.draw.rect(self.__surface, color, pygame.Rect(0,0,DICE_WIDTH,DICE_HEIGHT), DICE_THICKNESS)

        textSurfaceObj = self.fontObj.render(str(roll), True, color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (DICE_WIDTH / 2, DICE_HEIGHT / 2)
        self.__surface.blit(textSurfaceObj, textRectObj)

        return self.__surface

    def getPosition(self):
        return (DICE_MARGIN + (DICE_WIDTH + DICE_GAP) * self.slotnum, DICE_ROW)