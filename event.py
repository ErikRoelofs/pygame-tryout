# ship events
EVENT_DESTROYED = 1;

class EventControl:

	def __init__(self):
		self.listeners = []

	def setShipLists(self, playerShips, opponentShips):
		self.playerShips = playerShips
		self.opponentShips = opponentShips

	def __call__(self, sender, event):
		for listener in self.listeners:
			listener.event(event, sender)

	def addListener(self, listener, event):
		self.listeners.append(listener)