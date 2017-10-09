from entity import Entity
from actionbar import ActionBar

class Container(Entity):

    def __init__(self, fontObj, controller):
        self._content = Entity()
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
        True

    def clicked(self, mousex, mousey):
        True

    def event(self, name, target):
        if name == "player-selected":
            self.setContent(ActionBar(self._controller, target.ship().actions, self._fontObj))