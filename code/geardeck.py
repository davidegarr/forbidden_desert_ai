import random

class GearDeck:
    def __init__(self, game):
        self.game = game
        self.gear_deck = self.create()

    def create(self):
        # create deck of gear_cards
        gear_deck = []

        # 3 DuneBlaster
        for i in range(3):
            gear_deck.append(DuneBlaster(f"Dune Blaster {i+1}/3"))

        # 3 JetPack
        for i in range(3):
            gear_deck.append(JetPack(f"Jet Pack {i+1}/3"))

        # 2 Terrascope
        for i in range(2):
            gear_deck.append(Terrascope(f"Terrascope {i+1}/2"))

        # 2 SolarShield
        for i in range(2):
            gear_deck.append(SolarShield(f"Solar Shield {i+1}/2"))

        # 1 TimeThrottle
        for i in range(1):
            gear_deck.append(TimeThrottle(f"Time Throttle {i+1}/1"))

        # 1 SecretWaterReserve
        for i in range(1):
            gear_deck.append(SecretWaterReserve(f"Secret Water Reserve {i+1}/1"))

        return gear_deck

    def shuffle(self):
        random.shuffle(self.gear_deck)

    def draw(self, adventurer):
        if not self.gear_deck:
            return None

        card = self.gear_deck.pop()
        adventurer.get_item(card)


class DuneBlaster:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"
    
    def apply(self, tile):
        tile.sand = 0
        tile.blocked = False
        #print("All sand was cleared!")


class JetPack:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def apply(self, adventurer, move):
        adventurer.move(move)


class Terrascope:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def apply(self, tile):
        return tile.name


class SolarShield:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def apply(self, adventurer):
        adventurer.solar_shield_active = True


class TimeThrottle:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def apply(self):
        pass  # TBD


class SecretWaterReserve:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def apply(self, adventurer):
        #print(f"{adventurer.name} uses {self.name} on {adventurer.tile.name}.")
        for adventurer in adventurer.tile.adventurers:
            adventurer.get_water()
            adventurer.get_water()
            #print(f"{adventurer.name} now has {adventurer.water} units of water.")
