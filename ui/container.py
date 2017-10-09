from empty import Empty
from entity import Entity
from actionbar import ActionBar
from confirm import Confirm

class Container(Entity):

    def __init__(self, fontObj, controller):
        self._content = Empty()
        self._controller = controller
        controller.addListener(self, [])
        self._fontObj = fontObj

    def setContent(self, content):
        self._content = content

    def draw(self):
        return self._content.draw()

    def update(self, dt):
        return self._content.update(dt)

    def setMousePosition(self, mousex, mousey):
        self._content.setMousePosition(mousex, mousey)

    def clicked(self, mousex, mousey):
        self._content.clicked(mousex, mousey)

    def event(self, name, target):
        raise NotImplementedError("Child must override event function.")

class ActionBarContainer(Container):
    def event(self, name, target):
        if name == "player-selected":
            self.setContent(ActionBar(self._controller, target.ship().actions, self._fontObj))

class ConfirmActionContainer(Container):
    def event(self, name, data):
        if name == "all-selected":
            self.setContent(Confirm(self._controller, self._fontObj, data.attacker(), data.weapon(), data.target()))