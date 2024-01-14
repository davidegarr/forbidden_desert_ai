class Tile:
    """
    The Tile class represents a single tile on the Forbidden Desert game board.
    Attributes:
        name (str): The name of the tile, which is unique and descriptive (e.g., 'oasis', 'water_1').
        symbol (str): A single-character or short string symbol representing the tile on the board.
        x_coordinate (int, optional): The x-coordinate of the tile on the board. Defaults to None.
        y_coordinate (int, optional): The y-coordinate of the tile on the board. Defaults to None.
        sand (int): The number of sand markers on the tile. Initialized to 0.
        flipped (bool): A boolean indicating whether the tile has been flipped over. Defaults to False.

    Methods:
        flip(): Marks the tile as flipped over.
        set_coordinates(x_coordinate, y_coordinate): Sets the tile's position on the board.
        swap(other_tile): Swaps the position of this tile with another tile on the board.
        add_sand(): Adds a sand marker to the tile.
        remove_sand(): Removes a sand marker from the tile, ensuring the count does not go below zero.
    """

    def __init__(
        self,
        name,
        symbol,
        game,
        x_coordinate=None,
        y_coordinate=None,
        flipped=False,
        blocked=False,
    ):
        self.name = name
        self.symbol = symbol
        self.game = game
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.sand = 0
        self.flipped = flipped
        self.blocked = blocked
        self.adventurers = []  # List of adventurers on this tile
        self.boat_parts = [] # List of boat parts on this tile

    def __str__(self):
        return (
            f"{self.name} at {self.x_coordinate, self.y_coordinate}. Sand: {self.sand}"
        )

    def __repr__(self):
        return f"{self.name}"

    def add_adventurer(self, adventurer):
        self.adventurers.append(adventurer)

    def remove_adventurer(self, adventurer):
        self.adventurers.remove(adventurer)

    def flip(self, adventurer):
        #print(f"{adventurer.name} has flipped tile {self.name}")
        self.flipped = True
        self.apply_flip_effect(adventurer)

    def apply_flip_effect(self, adventurer):
        # Described in each tile sublass - vide infra.
        pass

    def set_coordinates(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def swap(self, other_tile):
        # if the storm tile (only one to trigger swap) has a boat part, give it immediately to the next tile after swap
        if self.boat_parts:
            for part in self.boat_parts[:]:  # iterating over a copy of the list
                self.game.log_file.write(f"{part} is now on {other_tile}.\n")
                self.boat_parts.remove(part)
                other_tile.boat_parts.append(part)


        # swap coordinates
        temp_x, temp_y = self.x_coordinate, self.y_coordinate
        self.x_coordinate, self.y_coordinate = (
            other_tile.x_coordinate,
            other_tile.y_coordinate,
        )
        other_tile.x_coordinate, other_tile.y_coordinate = temp_x, temp_y

        # Update the shared mapping with new coordinates
        self.game.coordinate_to_tile[(self.x_coordinate, self.y_coordinate)] = self
        self.game.coordinate_to_tile[
            (other_tile.x_coordinate, other_tile.y_coordinate)
        ] = other_tile

    def add_sand(self):
        self.sand += 1
        self.game.total_sand += 1
        if self.sand > 1:
            self.blocked = True

    def remove_sand(self):
        self.sand -= 1
        self.game.total_sand -= 1
        if self.sand < 0:
            self.sand = 0

        if self.sand < 2:
            self.blocked = False


class WaterTile(Tile):
    def __init__(
        self, name, symbol, game, x_coordinate=None, y_coordinate=None
    ):
        super().__init__(name, symbol, game, x_coordinate, y_coordinate)

    def apply_flip_effect(self, adventurer):
        # adventurer is actually not needed TBD
        for adventurer in self.adventurers:
            adventurer.get_water()
            adventurer.get_water()


class MirageTile(Tile):
    def __init__(
        self, name, symbol, game, x_coordinate=None, y_coordinate=None
    ):
        super().__init__(name, symbol, game, x_coordinate, y_coordinate)

    def apply_flip_effect(self, adventurer):
        # adventurer is actually not needed TBD
        #print("The well is dry...")
        pass


class GearTile(Tile):
    def __init__(
        self, name, symbol, game, x_coordinate=None, y_coordinate=None
    ):
        super().__init__(name, symbol, game, x_coordinate, y_coordinate)

    def apply_flip_effect(self, adventurer):
        self.game.gear_deck.draw(adventurer)


class TunnelTile(Tile):
    def __init__(
        self, name, symbol, game, x_coordinate=None, y_coordinate=None
    ):
        super().__init__(name, symbol, game, x_coordinate, y_coordinate)
    
    def apply_flip_effect(self, adventurer):
        self.game.gear_deck.draw(adventurer)


class PartTile(Tile):
    def __init__(
        self, name, symbol, game, x_coordinate=None, y_coordinate=None
    ):
        super().__init__(name, symbol, game, x_coordinate, y_coordinate)
    
    def apply_flip_effect(self, adventurer):
        if "gem" in self.name:
            self.game.gem_tiles_flipped += 1
        elif "motor" in self.name:
            self.game.motor_tiles_flipped += 1
        elif "compass" in self.name:
            self.game.compass_tiles_flipped += 1
        elif "propeller" in self.name: self.game.propeller_tiles_flipped += 1
