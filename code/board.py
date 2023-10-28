import random


class Tile:
    def __init__(
        self, name, symbol, x_coordinate=None, y_coordinate=None, flipped=False
    ):
        self.name = name
        self.symbol = symbol
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.sand = 0
        self.flipped = flipped

    def __str__(self):
        return (
            f"{self.name} at {self.x_coordinate, self.y_coordinate}. Sand: {self.sand}."
        )

    def flip(self):
        self.flipped = True

    def set_coordinates(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def swap(self, other_tile):
        temp_x, temp_y = self.x_coordinate, self.y_coordinate
        self.x_coordinate, self.y_coordinate = (
            other_tile.x_coordinate,
            other_tile.y_coordinate,
        )
        other_tile.x_coordinate, other_tile.y_coordinate = temp_x, temp_y

    def add_sand(self):
        self.sand += 1

    def remove_sand(self):
        self.sand -= 1
        if self.sand < 0:
            self.sand = 0


class Adventurer:
    def __init__(self, name, symbol, tile=None):
        self.name = name
        self.symbol = symbol
        if tile is None:
            self.tile = tiles["start"]
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
        
        if new_x == tiles["storm"].x_coordinate and new_y == tiles["storm"].y_coordinate:
            new_x = current_x
            new_y = current_y
            raise ValueError("Movement not valid. You can not run into the storm.")

        for tile in tiles:
            if new_x == tiles[tile].x_coordinate and new_y == tiles[tile].y_coordinate:
                self.tile = tiles[tile]

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


# Dict of tiles:
tiles = {
    "start": Tile("start", "S"),
    "storm": Tile("storm", "X", 2, 2),
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

all_coordinates = [(x, y) for x in range(5) for y in range(5)]
all_coordinates.remove((2, 2))

random.shuffle(all_coordinates)

for tile_name, tile in tiles.items():
    if tile.x_coordinate is None and tile.y_coordinate is None:
        x, y = all_coordinates.pop()
        tile.set_coordinates(x, y)

initial_sand = [(0, 2), (1, 1), (1, 3), (2, 0), (2, 4), (3, 1), (3, 3), (4, 2)]
for x_sand_tile, y_sand_tile in initial_sand:
    for tile in tiles:
        if (
            tiles[tile].x_coordinate == x_sand_tile
            and tiles[tile].y_coordinate == y_sand_tile
        ):
            tiles[tile].add_sand()

# dict of adventurers:
adventurers = {
    "archeologist": Adventurer("archeologist", "A"),
    "climber": Adventurer("climber", "C"),
    "explorer": Adventurer("explorer", "E"),
    "meteorologist": Adventurer("meteorologist", "M"),
    "navigator": Adventurer("navigator", "N"),
    "water_carrier": Adventurer("water_carrier", "WC"),
}


def print_board():
    board_representation = [["  " for _ in range(5)] for _ in range(5)]

    for tile_name, tile in tiles.items():
        x, y = tile.x_coordinate, tile.y_coordinate
        symbol = tile.symbol  # Directly access the symbol from the Tile object

        if tile.sand > 0:
            board_representation[y][x] = symbol + "(" + str(tile.sand) + ")"
        else:
            board_representation[y][x] = symbol

    for row in board_representation:
        print(" | ".join(row))
        print("-" * 40)  # Print a separator line


print_board()
for adventurer in adventurers:
    print(adventurers[adventurer])