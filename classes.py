import random, event


# ship states
STATE_READY = 1
STATE_SPENT = 2

class Ship:
    def __init__(self, name, hull, actions, event):
        self._name = name
        self.hull = hull
        self.damage = 0
        self.actions = actions
        self.state = STATE_READY
        self.event = event

    def name(self):
        return self._name

    def spend(self):
        self.state = STATE_SPENT

    def refresh(self):
        self.state = STATE_READY
        for action in self.actions:
            action.refresh()

    def available(self):
        return self.state == STATE_READY

    def performAttack(self, weapon, target):
        assert weapon in self.actions, "Cannot fire a weapon that is not on the ship!"
        self.spend()
        weapon.spend()
        return Attack(self, weapon, target)

    def resolveAttackOnMe(self, attacker, weapon, results):
        for result in results:
            if (result >= weapon.mount.accuracy()):
                self.takeDamage(weapon.mount.damage())

        if self.damage >= self.hull:
            self.destroy()

    def takeDamage(self, amount):
        self.damage += amount

    def destroy(self):
        self.event(self, event.EVENT_DESTROYED)


class Weapon:
    def __init__(self, rolls, mount, weaponType):
        self.rolls = rolls
        self.mount = mount
        self.weaponType = weaponType
        self.spent = False

    def spend(self):
        self.spent = True

    def refresh(self):
        self.spent = False

    def available(self):
        return not self.spent


class Mount:
    def __init__(self, theAccuracy, theDamage):
        self._accuracy = theAccuracy
        self._damage = theDamage

    def accuracy(self):
        return self._accuracy

    def damage(self):
        return self._damage


class WeaponType:
    def __init__(self, theName):
        self._name = theName

    def name(self):
        return self._name


class Attack:
    def __init__(self, attacker, weapon, target):
        self.attacker = attacker
        self.weapon = weapon
        self.target = target
        self.results = []
        self.applied = False
        for i in range(0, self.weapon.rolls):
            self.results.append(random.randint(1, 6))

    def apply(self):
        assert not self.applied, "This attack has already been applied!"
        self.applied = True
        self.target.resolveAttackOnMe(self.attacker, self.weapon, self.results)
