import random, event, copy


# ship states
STATE_READY = 1
STATE_SPENT = 2

# mounts
MOUNT_LIGHT = "light"
MOUNT_MEDIUM = "medium"
MOUNT_HEAVY = "heavy"

class Ship:
    def __init__(self, name, hull, traits, actions, event):
        self._name = name
        self.hull = hull
        self.damage = 0
        self.traits = traits
        self.actions = []
        for action in actions:
            self.actions.append(
                Weapon(
                    action.rolls,
                    Mount(action.mount.classification(), action.mount.accuracy(), action.mount.damage()),
                    action.weaponType))
        self.state = STATE_READY
        self.event = event

        for trait in self.traits:
            trait.applyToOwner(self)

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

        weapon = copy.deepcopy(weapon)

        # apply my traits that modify my attacks
        for trait in self.traits:
            trait.applyToOutgoingAttack(self, weapon, target)

        # apply target traits that modify incoming attacks
        for trait in target.traits:
            trait.applyToIncomingAttack(target, weapon, self)

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
    def __init__(self, classification, theAccuracy, theDamage):
        self._classification = classification
        self._accuracy = theAccuracy
        self._damage = theDamage

    def classification(self):
        return self._classification

    def accuracy(self):
        return self._accuracy

    def damage(self):
        return self._damage

    # note that lower accuracy is better
    def increaseAccuracy(self, amount):
        self._accuracy -= amount

    def decreaseAccuracy(self, amount):
        self._accuracy += amount

class WeaponType:
    def __init__(self, theName):
        self._name = theName

    def name(self):
        return self._name


class Attack:
    def __init__(self, attacker, weapon, target):
        self._attacker = attacker
        self._weapon = weapon
        self._target = target
        self.results = []
        self.applied = False
        for i in range(0, self._weapon.rolls):
            self.results.append(random.randint(1, 6))

    def attacker(self):
        return self._attacker

    def target(self):
        return self._target

    def weapon(self):
        return self._weapon

    def apply(self):
        assert not self.applied, "This attack has already been applied!"
        self.applied = True
        self._target.resolveAttackOnMe(self._attacker, self._weapon, self.results)

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