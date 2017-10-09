from action import Action
import action
import pygame, classes

ACTION_GAP = 25

class ActionBar:
    def __init__(self, controller, actions, fontObj):
        self._fontObj = fontObj
        self._controller = controller
        controller.addListener(self, [])
        self._size = (750,action.ACTION_HEIGHT)
        self._surface = pygame.Surface(self._size)
        self.actions = actions
        self.actionUIs = []
        self._mousePosition = None
        for theAction in actions:
            self.actionUIs.append(Action(controller, theAction, fontObj))

    def draw(self):
        self.unhighlightAll()

        if self._mousePosition:
            theAction = self.findUIAtPosition(self._mousePosition[0], self._mousePosition[1])
            if theAction:
                theAction.highlight(True)

        for index, theAction in enumerate(self.actionUIs):
            self._surface.blit(theAction.draw(), (index * (ACTION_GAP + action.ACTION_WIDTH), 0))

        return self._surface

    def update(self, dt):
        return True

    def event(self, name, data):
        if name == "action-selected":
            data.selected(True)

    def unhighlightAll(self):
        for action in self.actionUIs:
            action.highlight(False)

    def setMousePosition(self, mousex, mousey):
        if mousex >= 0 and mousex <= self._size[0] and mousey >= 0 and mousey <= self._size[1]:
            self._mousePosition = (mousex, mousey)

        else:
            self._mousePosition = None

    def findUIAtPosition(self, x, y):
        for index, theAction in enumerate(self.actionUIs):
            xmin = index * (ACTION_GAP + action.ACTION_WIDTH)
            xmax = xmin + action.ACTION_WIDTH
            ymin = 0
            ymax = ymin + action.ACTION_HEIGHT
            if xmin < x <= xmax and ymin < y < ymax:
                return theAction

    def findActionAtPosition(self, x, y):
        return self.findUIAtPosition(x,y).action()

    def clicked(self, x, y):
        action = self.findUIAtPosition(x,y)
        if action:
            self._controller.actionClicked(action)
