import random

class Tile:
    def __init__(self, name, x_coordinate=None, y_coordinate=None):
        self.name = name
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.sand = 0
    
    def set_coordinates(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def move_tile(self, x_move, y_move):
        self.x_coordinate = self.x_coordinate + x_move
        if self.x_coordinate < 0:
            self.x_coordinate = 0
        if self.x_coordinate > 4:
            self.x_coordinate = 4
        
        self.y_coordinate = self.y_coordinate + y_move
        if self.y_coordinate < 0:
            self.y_coordinate = 0
        if self.y_coordinate > 4:
            self.y_coordinate = 4

    def add_sand(self):
        self.sand += 1

    def remove_sand(self):
        self.sand -= 1
        if self.sand < 0:
            self.sand = 0

    def __str__(self):
        return f"{self.name} at {self.x_coordinate, self.y_coordinate}. Sand: {self.sand}."


#Dict of tiles:
tiles = {
    "start": Tile("start"),
    "storm": Tile("storm", 2, 2),

    "tunnel_1": Tile("tunnel_1"),
    "tunnel_2": Tile("tunnel_2"),
    "tunnel_3": Tile("tunnel_3"),

    "boat": Tile("boat"),
    "gem_h": Tile("gem_h"),
    "gem_v": Tile("gem_v"),
    "motor_h": Tile("motor_h"),
    "motor_v": Tile("motor_v"),
    "compass_h": Tile("compass_h"),
    "compass_v": Tile("compass_v"),
    "propeller_h": Tile("propeller_h"),
    "propeller_v": Tile("propeller_v"),

    "water_1": Tile("water_1"),
    "water_2": Tile("water_2"),
    "oasis": Tile("oasis"),

    "dune_1": Tile("dune_1"),
    "dune_2": Tile("dune_2"),
    "dune_3": Tile("dune_3"),
    "dune_4": Tile("dune_4"),
    "dune_5": Tile("dune_5"),
    "dune_6": Tile("dune_6"),
    "dune_7": Tile("dune_7"),
    "dune_8": Tile("dune_8")
}

all_coordinates = [(x, y) for x in range(5) for y in range(5)]
all_coordinates.remove((2,2))

random.shuffle(all_coordinates)

for tile_name, tile in tiles.items():
    if tile.x_coordinate is None and tile.y_coordinate is None:
        x, y = all_coordinates.pop()
        tile.set_coordinates(x, y)

initial_sand = [(0, 2), (1, 1), (1, 3), (2, 0), (2, 4), (3, 1), (3, 3), (4, 2)]
for x_sand_tile, y_sand_tile in initial_sand:
    for tile in tiles:
        if tiles[tile].x_coordinate == x_sand_tile and tiles[tile].y_coordinate == y_sand_tile:
            tiles[tile].add_sand()
