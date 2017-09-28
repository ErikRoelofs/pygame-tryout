import classes

class Library:
    def __init__(self, mounts, weaponTypes, event):
        self.ships = []
        self.ships.append(classes.Ship(3, (classes.Weapon(3, mounts[0], weaponTypes[0]),),event))

    def ship(self, index):
        return self.ships[index]

