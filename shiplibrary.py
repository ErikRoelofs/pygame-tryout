import classes

class Library:
    def __init__(self, mounts, weaponTypes, event):
        self.ships = []
        self.ships.append(classes.Ship("Narf", 3, (classes.Weapon(3, mounts[0], weaponTypes[0]),),event))
        self.ships.append(classes.Ship("Harf", 3, (classes.Weapon(3, mounts[0], weaponTypes[0]),), event))
        self.ships.append(classes.Ship("Darf", 3, (classes.Weapon(3, mounts[0], weaponTypes[0]),), event))

    def ship(self, index):
        return self.ships[index]

    def shipByName(self, name):
        for ship in self.ships:
            if ship.name() == name:
                return ship
        raise IndexError("No ship registered by the name of: " + name)