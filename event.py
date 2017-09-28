# ship events
EVENT_DESTROYED = 1;

class EventControl:
	def setShipLists(self, playerShips, opponentShips):
		self.playerShips = playerShips
		self.opponentShips = opponentShips

	def __call__(self, sender, event):
		if event == EVENT_DESTROYED:
			if sender in self.playerShips:
				self.playerShips.remove(sender)
			if sender in self.opponentShips:
				self.opponentShips.remove(sender)
