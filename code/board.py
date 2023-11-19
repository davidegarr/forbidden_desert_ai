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
        coordinate_to_tile,
        x_coordinate=None,
        y_coordinate=None,
        flipped=False,
        blocked=False
    ):
        self.name = name
        self.symbol = symbol
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.sand = 0
        self.flipped = flipped
        self.blocked = blocked
        self.coordinate_to_tile = coordinate_to_tile
        self.adventurers = []  # List of adventurers on this tile


    def __str__(self):
        return (
            f"{self.name} at {self.x_coordinate, self.y_coordinate}. Sand: {self.sand}."
        )

    def add_adventurer(self, adventurer):
        self.adventurers.append(adventurer)

    def remove_adventurer(self, adventurer):
        self.adventurers.remove(adventurer)

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
        coordinate_to_tile[
            (other_tile.x_coordinate, other_tile.y_coordinate)
        ] = other_tile

    def add_sand(self):
        self.sand += 1
        if self.sand > 1:
            self.blocked = True

    def remove_sand(self):
        self.sand -= 1
        if self.sand < 0:
            self.sand = 0

        if self.sand < 2:
            self.blocked = False


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

    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        self.name = name
        self.symbol = symbol
        self.tile = tile
        self.coordinate_to_tile = coordinate_to_tile
        self.water = water
        self.max_water = water

    def available_tiles(self):
        accessible_tiles = [self.tile]
        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy

            # Check if the new coordinates are within the board boundaries
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.coordinate_to_tile.get((new_x, new_y))

                # Check if the adjacent tile is not the storm tile
                if adjacent_tile and adjacent_tile.name != "storm":
                    accessible_tiles.append(adjacent_tile)

        return accessible_tiles
        
    
    def __str__(self):
        return f"{self.name} ({self.symbol}) at {self.tile.name}. {self.water} water left."

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

        if self.coordinate_to_tile[(new_x, new_y)].blocked == True:
            new_x = current_x
            new_y = current_y
            raise ValueError("Movement not valid. Destination tile is blocked.")
        
        self.tile.remove_adventurer(self)

        self.tile = self.coordinate_to_tile[(new_x, new_y)]

        self.tile.add_adventurer(self)

    def get_water(self):
        self.water += 1
        if self.water > 5:
            self.water = 5

    def lose_water(self):
        self.water -= 1
        if self.water < 0:
            self.water = 0

    def give_water(self, other_adventurer):
        if self.water == 0:
            raise ValueError("Not enough water to give.")
        if other_adventurer.water == other_adventurer.max_water:
            raise ValueError ("Cannot give water. Full deposit.")
        
        self.water -= 1
        other_adventurer.water += 1
    
    def clear_sand(self, tile_to_clear):
        if tile_to_clear in self.available_tiles:
            tile_to_clear.remove_sand()




class Archeologist(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)

    def ability(self, tile_to_clear):
        if tile_to_clear in self.available_tiles:
            tile_to_clear.remove_sand()
            tile_to_clear.remove_sand()

class Climber(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)

class Explorer(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)

class Meteorologist(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)

class Navigator(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)

class WaterCarrier(Adventurer):
    def __init__(self, name, symbol, tile, water, coordinate_to_tile):
        super().__init__(name, symbol, tile, water, coordinate_to_tile)
    
    def ability(self):
        if self.tile.flipped == True and "water" in self.tile.name and self.tile.blocked == False:
            self.get_water()
            self.get_water()

class Deck:
    def __init__(self):
        self.deck = self.initialize_deck()

    def initialize_deck(self):
        # create deck of cards
        deck = []

        # add storm cards
        storm_patterns = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # 1 move cards
        for pattern in storm_patterns:
            for i in range(3):
                deck.append(StormCard(f"Storm Moves {i}", [pattern]))

        # 2 move cards
        for pattern in storm_patterns:
            for i in range(2):
                deck.append(StormCard(f"Storm Moves {i}", [pattern, pattern]))

        # 3 move cards
        for pattern in storm_patterns:
            for i in range(1):
                deck.append(StormCard(f"Storm Moves {i}", [pattern, pattern, pattern]))

        # add sun betas down cards
        for i in range(4):
            deck.append(SBDCard(f"Sun Beats Down {i}"))

        # add storm picks up cards
        for i in range(3):
            deck.append(SPUCard(f"Storm Picks Up {i}"))

        return deck


class StormCard:
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves

    def apply(self, storm, coordinate_to_tile):
        for move in self.moves:
            x_move, y_move = move
            new_x = storm.x_coordinate + x_move
            new_y = storm.y_coordinate + y_move

            # Check if the move is within board boundaries
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = coordinate_to_tile[(new_x, new_y)]
                adjacent_tile.add_sand()
                for adventurer in adjacent_tile.adventurers:
                    adventurer.lose_water()
                
                storm.swap(adjacent_tile, coordinate_to_tile)


class SBDCard:
    def __init__(self, name):
        self.name = name
    
    def apply(self, tiles):
        for tile in tiles.values():
            if not tile.flipped and "tunnel" not in tile.name:
                for adventurer in tile.adventurers:
                    adventurer.lose_water()


class SPUCard:
    def __init__(self, name):
        self.name = name


def initialize_tiles(coordinate_to_tile):
    """
    The tiles dictionary is the equivalent of the stack of tiles that comes with the boardgame.
    The same quantity and type of tiles as within the "real" boardgame is depicted here.
    Each key-value pair consists of a unique tile name and a corresponding Tile object that holds
    the tile's properties such as its symbol, coordinates, and state (flipped or not, and the amount of sand).
    """
    tiles = {
        "start": Tile("start", "S", coordinate_to_tile),
        "storm": Tile("storm", "X", coordinate_to_tile),
        "tunnel_1": Tile("tunnel_1", "T1", coordinate_to_tile),
        "tunnel_2": Tile("tunnel_2", "T2", coordinate_to_tile),
        "tunnel_3": Tile("tunnel_3", "T3", coordinate_to_tile),
        "boat": Tile("boat", "B", coordinate_to_tile),
        "gem_h": Tile("gem_h", "Gh", coordinate_to_tile),
        "gem_v": Tile("gem_v", "Gv", coordinate_to_tile),
        "motor_h": Tile("motor_h", "Mh", coordinate_to_tile),
        "motor_v": Tile("motor_v", "Mv", coordinate_to_tile),
        "compass_h": Tile("compass_h", "Ch", coordinate_to_tile),
        "compass_v": Tile("compass_v", "Cv", coordinate_to_tile),
        "propeller_h": Tile("propeller_h", "Ph", coordinate_to_tile),
        "propeller_v": Tile("propeller_v", "Pv", coordinate_to_tile),
        "water_1": Tile("water_1", "W1", coordinate_to_tile),
        "water_2": Tile("water_2", "W2", coordinate_to_tile),
        "oasis": Tile("oasis", "O", coordinate_to_tile),
        "dune_1": Tile("dune_1", "D1", coordinate_to_tile),
        "dune_2": Tile("dune_2", "D2", coordinate_to_tile),
        "dune_3": Tile("dune_3", "D3", coordinate_to_tile),
        "dune_4": Tile("dune_4", "D4", coordinate_to_tile),
        "dune_5": Tile("dune_5", "D5", coordinate_to_tile),
        "dune_6": Tile("dune_6", "D6", coordinate_to_tile),
        "dune_7": Tile("dune_7", "D7", coordinate_to_tile),
        "dune_8": Tile("dune_8", "D8", coordinate_to_tile),
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
        "archeologist": Archeologist(
            "archeologist", "A", tiles["start"], 3, coordinate_to_tile
        ),
        "climber": Climber("climber", "C", tiles["start"], 3, coordinate_to_tile),
        "explorer": Explorer("explorer", "E", tiles["start"], 4, coordinate_to_tile),
        "meteorologist": Meteorologist(
            "meteorologist", "M", tiles["start"], 4, coordinate_to_tile
        ),
        "navigator": Navigator("navigator", "N", tiles["start"], 4, coordinate_to_tile),
        "water_carrier": WaterCarrier(
            "water_carrier", "WC", tiles["start"], 5, coordinate_to_tile
        ),
    }

    # add the adventurers to the start tile
    for adventurer in adventurers:
        tiles["start"].add_adventurer(adventurers[adventurer])

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
    coordinate_to_tile = {}
    tiles = initialize_tiles(coordinate_to_tile)
    coordinate_to_tile = set_tile_coordinates(tiles)
    adventurers = initialize_adventurers(tiles, coordinate_to_tile)

    # Example usage
    storm_tile = tiles["storm"]  # Assuming tiles is already initialized
    storm_card = StormCard("Storm Moves", [(1, 0), (1, 0)])  # Example for "two right"

    # To apply the storm card
    storm_card.apply(storm_tile, coordinate_to_tile)

    print_board(tiles)
    print_adventurers(adventurers)

    adventurers["archeologist"].move((0,1))
    SBD_card = SBDCard("Sun Beats down")
    SBD_card.apply(tiles)

    print_board(tiles)
    print_adventurers(adventurers)


if __name__ == "__main__":
    main()