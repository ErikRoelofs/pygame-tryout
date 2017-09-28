import classes

class Trait:
    def applyToOwner(self, ship):
        return False

    def applyToTarget(self, ship):
        return False

    def applyToOutgoingAttack(self, me, weapon, target):
        return False

    def applyToIncomingAttack(self, attacker, weapon, me):
        return False

class Accurate(Trait):
    def __init__(self, amount):
        self.amount = amount

    def applyToOutgoingAttack(self, me, weapon, target):
        weapon.mount.increaseAccuracy(self.amount)

class Evasive(Trait):
    def __init__(self, amount):
        self.amount = amount

    def applyToIncomingAttack(self, attacker, weapon, me):
        weapon.mount.decreaseAccuracy(self.amount)

class Lumbering(Trait):
    def __init__(self, amount):
        self.amount = amount

    def applyToIncomingAttack(self, attacker, weapon, me):
        weapon.mount.increaseAccuracy(self.amount)

class Armored(Trait):
    def applyToIncomingAttack(self, attacker, weapon, me):
        if weapon.weaponType.name() == classes.WEAPON_KINETIC:
            weapon.mount.decreaseDamage(1)

class HeavilyArmored(Trait):
    def applyToIncomingAttack(self, attacker, weapon, me):
        if weapon.weaponType.name() == classes.WEAPON_KINETIC:
            weapon.mount.decreaseDamage(2)
