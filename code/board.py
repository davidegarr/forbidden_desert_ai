import random


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
        x_coordinate=None,
        y_coordinate=None,
        flipped=False,
    ):
        self.name = name
        self.symbol = symbol
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.sand = 0
        self.flipped = flipped
        self.coordinate_to_tile = None

    def __str__(self):
        return (
            f"{self.name} at {self.x_coordinate, self.y_coordinate}. Sand: {self.sand}."
        )

    def set_coordinate_mapping(self, coordinate_to_tile):
        self.coordinate_to_tile = coordinate_to_tile

    def flip(self):
        self.flipped = True

    def set_coordinates(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def swap(self, other_tile, coordinate_to_tile):
        # swap coordinates
        temp_x, temp_y = self.x_coordinate, self.y_coordinate
        self.x_coordinate, self.y_coordinate = (
            other_tile.x_coordinate,
            other_tile.y_coordinate,
        )
        other_tile.x_coordinate, other_tile.y_coordinate = temp_x, temp_y

        # Update the shared mapping with new coordinates
        coordinate_to_tile[(self.x_coordinate, self.y_coordinate)] = self
        coordinate_to_tile[(other_tile.x_coordinate, other_tile.y_coordinate)] = other_tile

    def add_sand(self):
        self.sand += 1

    def remove_sand(self):
        self.sand -= 1
        if self.sand < 0:
            self.sand = 0


class Adventurer:
    """
    The Adventurer class represents a player in the Forbidden Desert game.
    Attributes:
        name (str): The name of the adventurer, indicating the role (e.g., 'archeologist', 'navigator').
        symbol (str): A unique symbol representing the adventurer on the board.
        tile (Tile): The tile object on which the adventurer is currently located.
        water (int): The current water level of the adventurer, starts at 5.

    Methods:
        __str__(): Returns a string representation of the adventurer's current state.
        move(move): Moves the adventurer to a new tile on the board, based on the provided (x, y) offsets.
        get_water(): Increases the adventurer's water level by 1, not exceeding the maximum.
        lose_water(): Decreases the adventurer's water level by 1, not falling below zero.
        give_water(other_adventurer): Transfers 1 water unit to another adventurer if possible.
    """

    def __init__(self, name, symbol, tile, coordinate_to_tile):
        self.name = name
        self.symbol = symbol
        self.tile = tile
        self.coordinate_to_tile = coordinate_to_tile
        self.water = 5

    def __str__(self):
        return f"{self.name} at {self.tile.name}. Symbol: {self.symbol}."

    def move(self, move):
        x_move, y_move = move
        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        new_x, new_y = current_x + x_move, current_y + y_move
        if not (0 <= new_x <= 4) or not (0 <= new_y <= 4):
            new_x = current_x
            new_y = current_y
            raise ValueError("Movement not valid. Move outside borders.")

        if self.coordinate_to_tile[(new_x, new_y)].name == "storm":
            new_x = current_x
            new_y = current_y
            raise ValueError("Movement not valid. You can not run into the storm.")

        self.tile = self.coordinate_to_tile[(new_x, new_y)]

    def get_water(self):
        self.water += 1
        if self.water > 5:
            self.water = 5

    def lose_water(self):
        self.water -= 1
        if self.water < 0:
            self.water = 0

    def give_water(self, other_adventurer):
        if self.water == 1:
            raise ValueError("Not enough water to give.")
        self.water -= 1
        other_adventurer.water += 1
        if other_adventurer.water > 5:
            other_adventurer.water = 5


def initialize_tiles():
    """
    The tiles dictionary is the equivalent of the stack of tiles that comes with the boardgame.
    The same quantity and type of tiles as within the "real" boardgame is depicted here.
    Each key-value pair consists of a unique tile name and a corresponding Tile object that holds
    the tile's properties such as its symbol, coordinates, and state (flipped or not, and the amount of sand).
    """
    tiles = {
        "start": Tile("start", "S"),
        "storm": Tile("storm", "X"),
        "tunnel_1": Tile("tunnel_1", "T1"),
        "tunnel_2": Tile("tunnel_2", "T2"),
        "tunnel_3": Tile("tunnel_3", "T3"),
        "boat": Tile("boat", "B"),
        "gem_h": Tile("gem_h", "Gh"),
        "gem_v": Tile("gem_v", "Gv"),
        "motor_h": Tile("motor_h", "Mh"),
        "motor_v": Tile("motor_v", "Mv"),
        "compass_h": Tile("compass_h", "Ch"),
        "compass_v": Tile("compass_v", "Cv"),
        "propeller_h": Tile("propeller_h", "Ph"),
        "propeller_v": Tile("propeller_v", "Pv"),
        "water_1": Tile("water_1", "W1"),
        "water_2": Tile("water_2", "W2"),
        "oasis": Tile("oasis", "O"),
        "dune_1": Tile("dune_1", "D1"),
        "dune_2": Tile("dune_2", "D2"),
        "dune_3": Tile("dune_3", "D3"),
        "dune_4": Tile("dune_4", "D4"),
        "dune_5": Tile("dune_5", "D5"),
        "dune_6": Tile("dune_6", "D6"),
        "dune_7": Tile("dune_7", "D7"),
        "dune_8": Tile("dune_8", "D8"),
    }
    return tiles


def set_tile_coordinates(tiles):
    """
    Assigns coordinates to the tiles and returns the coordinate_to_tile mapping.
    Only the "storm" tile is placed at a particular place (middle of the board: 2,2), the rest are placed at random.
    Adds initial sand to board.
    """
    # Assign fixed coordinates to the storm tile
    tiles["storm"].set_coordinates(2, 2)

    # Create a list of all possible coordinates except for the storm's
    all_coordinates = [(x, y) for x in range(5) for y in range(5)]
    all_coordinates.remove((2, 2))  # Remove the storm's fixed coordinates
    random.shuffle(all_coordinates)

    # Initialize coordinate_to_tile with the storm tile
    coordinate_to_tile = {(2, 2): tiles["storm"]}

    # Assign coordinates to the rest of the tiles
    for tile_name, tile in tiles.items():
        if tile.x_coordinate is None and tile.y_coordinate is None:
            x, y = all_coordinates.pop()
            tile.set_coordinates(x, y)
            coordinate_to_tile[(x, y)] = tile

    for tile in tiles.values():
        tile.set_coordinate_mapping(coordinate_to_tile)

    """
    Add initial sand using the .add_sand() method.
    """
    initial_sand = [(0, 2), (1, 1), (1, 3), (2, 0), (2, 4), (3, 1), (3, 3), (4, 2)]
    for x_sand_tile, y_sand_tile in initial_sand:
        coordinate_to_tile[(x_sand_tile, y_sand_tile)].add_sand()

    return coordinate_to_tile


def initialize_adventurers(tiles, coordinate_to_tile):
    """
    Here the adventurers dictionary is initialized, after the board is set.
    By default, all adventureres go to the "start" Tile (see method above).
    """
    adventurers = {
        "archeologist": Adventurer(
            "archeologist", "A", tiles["start"], coordinate_to_tile
        ),
        "climber": Adventurer("climber", "C", tiles["start"], coordinate_to_tile),
        "explorer": Adventurer("explorer", "E", tiles["start"], coordinate_to_tile),
        "meteorologist": Adventurer(
            "meteorologist", "M", tiles["start"], coordinate_to_tile
        ),
        "navigator": Adventurer("navigator", "N", tiles["start"], coordinate_to_tile),
        "water_carrier": Adventurer(
            "water_carrier", "WC", tiles["start"], coordinate_to_tile
        ),
    }

    return adventurers


def print_board(tiles):
    """
    Self-explanatory. This function prints the board to the terminal. It formats the board so its easier to read (same size for each tile, etc).
    It includes the symbol for the tile, and the amount of sand that it holds, if any.
    """
    board_representation = [["" for _ in range(5)] for _ in range(5)]

    # Place tiles on the board
    for tile_name, tile in tiles.items():
        x, y = tile.x_coordinate, tile.y_coordinate
        symbol = tile.symbol
        sand = f"({tile.sand})" if tile.sand > 0 else " "

        # Format each cell to have a fixed width for alignment
        board_representation[y][x] = f"{symbol:<2}{sand:<3}"

    # Print the board
    for row in board_representation:
        print(" | ".join(cell for cell in row))
        print("-" * (6 * 5 + 4 * 4))  # Adjust the separator length to the cell width


def print_adventurers(adventurers):
    """
    Self explanatory. Prints each adventurer using the __str__ method in the class to the terminal.
    """
    for adventurer in adventurers:
        print(adventurers[adventurer])


def main():
    tiles = initialize_tiles()
    coordinate_to_tile = set_tile_coordinates(tiles)
    for tile in tiles.values():
        tile.coordinate_to_tile = coordinate_to_tile
    adventurers = initialize_adventurers(tiles, coordinate_to_tile)


if __name__ == "__main__":
    main()