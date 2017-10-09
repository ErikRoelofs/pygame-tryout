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
        for theAction in actions:
            self.actionUIs.append(Action(controller, theAction, fontObj))

    def draw(self):
        for index, theAction in enumerate(self.actionUIs):
            self._surface.blit(theAction.draw(), (index * (ACTION_GAP + action.ACTION_WIDTH), 0))

        return self._surface

    def update(self, dt):
        return True

    def event(self, name, data):
        True