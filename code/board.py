import random


class Game:
    def __init__(self, log_file) -> None:
        self.log_file = log_file
        # Initialize game state
        self.coordinate_to_tile = {}  # Holds the mapping from coordinates to tiles
        self.tiles = {}  # Dictionary to store tiles by name
        self.adventurers = {}  # Holds the adventurers by name
        self.deck = Deck(self)  # Creates the deck of cards
        self.gear_deck = GearDeck(self) # Creates the deck of gear cards
        self.sand_storm_level = 1
        self.is_game_over = False  # Status flag to control the game loop
        self.player_order = []  # List that holds the order in which players will take turns
        
        self.round = 1 # A round is defined as a turn for each player
        self.turn = 1 # A turn is defined as 4 actions from an adventurer
        self.action = 1 # An action is defined as one of the 4 activities that an adventurer can perform in each turn

        self.setup()  # Perform initial game setup

        self.motor_tiles_flipped = 0
        self.propeller_tiles_flipped = 0
        self.gem_tiles_flipped = 0
        self.compass_tiles_flipped = 0

    def setup(self):
        # Call methods to initialize the game components
        self.initialize_tiles()
        self.initialize_adventurers()
        self.deck.shuffle()
        self.gear_deck.shuffle()

        game_state = f"Initial State:\n"
        game_state += f"Storm Level: {self.sand_storm_level}\n"
        game_state += "Game Board: \n"
        game_state += self.get_board_representation()
        game_state += "\n\nAdventurers:\n"
        game_state += self.get_adventurers_representation() + "\n\n"

        self.log_file.write(game_state)

    def initialize_tiles(self):
        """
        The tiles dictionary is the equivalent of the stack of tiles that comes with the boardgame.
        The same quantity and type of tiles as within the "real" boardgame is depicted here.
        Each key-value pair consists of a unique tile name and a corresponding Tile object that holds
        the tile's properties such as its symbol, coordinates, and state (flipped or not, and the amount of sand).
        """
        tiles = {
            "start": GearTile("start", "S", self),
            "storm": Tile("storm", "X", self),
            "tunnel_1": TunnelTile("tunnel_1", "T1", self),
            "tunnel_2": TunnelTile("tunnel_2", "T2", self),
            "tunnel_3": TunnelTile("tunnel_3", "T3", self),
            "boat": Tile("boat", "B", self),
            "gem_h": PartTile("gem_h", "Gh", self),
            "gem_v": PartTile("gem_v", "Gv", self),
            "motor_h": PartTile("motor_h", "Mh", self),
            "motor_v": PartTile("motor_v", "Mv", self),
            "compass_h": PartTile("compass_h", "Ch", self),
            "compass_v": PartTile("compass_v", "Cv", self),
            "propeller_h": PartTile("propeller_h", "Ph", self),
            "propeller_v": PartTile("propeller_v", "Pv", self),
            "water_1": WaterTile("water_1", "W1", self),
            "water_2": WaterTile("water_2", "W2", self),
            "oasis": MirageTile("mirage", "M", self),
            "dune_1": GearTile("dune_1", "D1", self),
            "dune_2": GearTile("dune_2", "D2", self),
            "dune_3": GearTile("dune_3", "D3", self),
            "dune_4": GearTile("dune_4", "D4", self),
            "dune_5": GearTile("dune_5", "D5", self),
            "dune_6": GearTile("dune_6", "D6", self),
            "dune_7": GearTile("dune_7", "D7", self),
            "dune_8": GearTile("dune_8", "D8", self),
        }

        self.tiles = tiles

        """
        Below, coordinates to the tiles are assigned and returns the coordinate_to_tile mapping.
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
        self.coordinate_to_tile = {(2, 2): tiles["storm"]}

        # Assign coordinates to the rest of the tiles
        for tile_name, tile in tiles.items():
            if tile.x_coordinate is None and tile.y_coordinate is None:
                x, y = all_coordinates.pop()
                tile.set_coordinates(x, y)
                self.coordinate_to_tile[(x, y)] = tile

        """
        Add initial sand using the .add_sand() method.
        """
        initial_sand = [(0, 2), (1, 1), (1, 3), (2, 0), (2, 4), (3, 1), (3, 3), (4, 2)]
        for x_sand_tile, y_sand_tile in initial_sand:
            self.coordinate_to_tile[(x_sand_tile, y_sand_tile)].add_sand()

    def initialize_adventurers(self):
        """
        Here the adventurers dictionary is initialized, after the board is set.
        By default, all adventureres go to the "start" Tile.
        """

        self.adventurers = {
            "archeologist": Archeologist(
                "archeologist", "A", self.tiles["start"], self, 3
            ),
            "climber": Climber("climber", "C", self.tiles["start"], self, 3),
            "explorer": Explorer("explorer", "E", self.tiles["start"], self, 4),
            "meteorologist": Meteorologist(
                "meteorologist", "M", self.tiles["start"], self, 4
            ),
            "navigator": Navigator("navigator", "N", self.tiles["start"], self, 4),
            "water_carrier": WaterCarrier(
                "water_carrier", "WC", self.tiles["start"], self, 5
            ),
        }

        # Add the adventurers to the start tile
        for adventurer in self.adventurers.values():
            self.tiles["start"].add_adventurer(adventurer)

    def increase_storm_level(self):
        self.sand_storm_level += 1

    def get_board_representation(self):
        board_representation = [["" for _ in range(5)] for _ in range(5)]
        for _, tile in self.coordinate_to_tile.items():
            x, y = tile.x_coordinate, tile.y_coordinate
            symbol = tile.symbol
            sand = f"({tile.sand})" if tile.sand > 0 else " "
            board_representation[y][x] = f"{symbol:<2}{sand:<3}"

        board_str = "-" * (6 * 5 + 4 * 3) + "\n"  # Start with a line of dashes
        board_str += "\n".join("| " + " | ".join(cell for cell in row) + " |" + "\n" + "-" * (6 * 5 + 4 * 3) for row in board_representation)
        return board_str

    def get_adventurers_representation(self):
        adventurers_str = "\n".join(str(adventurer) for adventurer in self.adventurers.values())
        return adventurers_str
    
    def print_game(self, adventurer, chosen_action):
        #print("Game Board:")
        #self.print_board()
        #print("\nAdventurers:")
        #self.print_adventurers()
        #print("\nStorm Level:", self.sand_storm_level, "\n")

        game_state = f"{self.round}." + f"{self.turn}." + f"{self.action}: \n"
        game_state += f"Storm Level: {self.sand_storm_level}\n"
        game_state += f"{adventurer.name}: {chosen_action[0]}, {chosen_action[1]}. Cost: {chosen_action[2]}.\n"
        game_state += "Game Board: \n"
        game_state += self.get_board_representation()
        game_state += "\n\nAdventurers:\n"
        game_state += self.get_adventurers_representation() + "\n\n"

        self.log_file.write(game_state)

    def start_game(self):
        self.set_player_order()
        while not self.is_game_over:
            for adventurer in self.player_order:
                self.execute_turn(adventurer)
                if self.is_game_over:
                    print("Game Over")
                    break
            self.round += 1
            self.turn = 1

    def set_player_order(self):
        # Find the minimum water level amongst all adventurers
        min_water_level = min(
            adventurer.water for adventurer in self.adventurers.values()
        )

        # Add to the list all the adventurers with the minimum amount of water
        least_water_adventurers = []
        for adventurer in self.adventurers.values():
            if adventurer.water == min_water_level:
                least_water_adventurers.append(adventurer)

        # Between all the adventurers with the least amount of water, choose one at random
        first_player = random.choice(least_water_adventurers)

        # Create a list of the other players
        other_players = [
            adventurer
            for adventurer in self.adventurers.values()
            if adventurer != first_player
        ]
        random.shuffle(other_players)

        # Set the player order starting with the first player followed by the others
        self.player_order = [first_player] + other_players

    def execute_turn(self, adventurer):
        self.action = 1

        action_points = 4 # Each adventurer can spend 4 action points per turn
        while action_points > 0:
            possible_actions = self.get_possible_actions(adventurer)
            chosen_action = random.choice(possible_actions) # Select one of the actions at random
            action_cost = chosen_action[2]
            print(adventurer.name, "chosen action:", chosen_action[0], chosen_action[1], "cost:", action_cost)
            self.perform_action(adventurer, chosen_action)
            self.action += action_cost
            action_points -= action_cost


        self.turn += 1
        self.deck.draw()  # Draw cards from the StormDeck at the end of every turn
        self.check_game_status()

    def get_possible_actions(self, adventurer):
        possible_actions = []

        # Add "move" actions with their corresponding move directions
        for move in adventurer.available_moves():
            possible_actions.append(("move", move, 1))

        # Check if the adventurer can flip the current tile:
        if adventurer.can_flip():
            possible_actions.append(("flip", adventurer, 1))

        # Check if adventurer can clear sand from any accesible tile
        for tile in adventurer.available_sand():
            possible_actions.append(("remove_sand", tile, 1))

        # Check if adventurer can perform special ability

        # Check if adventurer can pickup a boat piece
        if adventurer.tile.boat_parts:
            for item in adventurer.tile.boat_parts:
                possible_actions.append(("pick_part", (adventurer, item), 1))

        # Sharing items from inventory
        for tile in self.tiles.values():
            if len(tile.adventurers) > 1:  # There's potential for item sharing
                for i, adventurer in enumerate(tile.adventurers):
                    if adventurer.inventory:  # Check if adventurer has items to share
                        for other_adventurer in tile.adventurers[i+1:]:
                            for item in adventurer.inventory:
                                # Add an action for each item the adventurer can share
                                possible_actions.append(("give_item", (adventurer, other_adventurer, item), 0))


        # Sharing water between adventurers in the same tile
        for tile in self.tiles.values():
            if len(tile.adventurers) > 1:  # There's potential for water sharing
                for i, adventurer in enumerate(tile.adventurers):
                    for other_adventurer in tile.adventurers[i+1:]:
                        if other_adventurer.water < other_adventurer.max_water:
                            possible_actions.append(("give_water", (adventurer, other_adventurer), 0))

        return possible_actions

    def perform_action(self, adventurer, chosen_action):
        self.log_file.write(f"{chosen_action[0]}, {chosen_action[1]}\n")
        action_type = chosen_action[0]
        if action_type == "move":
            adventurer.move(chosen_action[1])
        elif action_type == "flip":
            adventurer.flip()
            if isinstance(adventurer.tile, PartTile):
                self.check_placement()
        elif action_type == "remove_sand":
            tile_to_clear = chosen_action[1]
            adventurer.clear_sand(tile_to_clear)
        elif action_type == "give_water":
            water_giver = chosen_action[1][0]
            water_reciever = chosen_action[1][1]
            water_giver.give_water(water_reciever)
        elif action_type == "give_item":
            item_giver = chosen_action[1][0]
            item_reciever = chosen_action[1][1]
            item = chosen_action[1][2]
            item_giver.give_item(item_reciever, item)
        elif action_type == "pick_part":
            adventurer = chosen_action[1][0]
            part = chosen_action[1][1]
            adventurer.pick_part(part)

        self.print_game(adventurer, chosen_action)

    def check_game_status(self):
        if any(adventurer.water == 0 for adventurer in self.adventurers.values()):
            self.is_game_over = True
            self.log_file.write("Game over. An adventurer has run out of water.")

    def check_placement(self):
        if self.propeller_tiles_flipped == 2:
            propeller_x_tile = self.tiles["propeller_v"].x_coordinate
            propeller_y_tile = self.tiles["propeller_h"].y_coordinate
            propeller_tile = self.coordinate_to_tile[(propeller_x_tile, propeller_y_tile)]
            self.log_file.write(f"Propeller has appeared at {propeller_tile.name} \n")
            propeller_tile.boat_parts.append("Propeller")
            self.propeller_tiles_flipped += 1

        elif self.motor_tiles_flipped == 2:
            motor_x_tile = self.tiles["motor_v"].x_coordinate
            motor_y_tile = self.tiles["motor_h"].y_coordinate
            motor_tile = self.coordinate_to_tile[(motor_x_tile, motor_y_tile)]
            self.log_file.write(f"Motor has appeared at {motor_tile.name}\n")
            motor_tile.boat_parts.append("Motor")
            self.motor_tiles_flipped += 1
        
        elif self.gem_tiles_flipped == 2:
            gem_x_tile = self.tiles["gem_v"].x_coordinate
            gem_y_tile = self.tiles["gem_h"].y_coordinate
            gem_tile = self.coordinate_to_tile[(gem_x_tile, gem_y_tile)]
            self.log_file.write(f"Gem has appeared at {gem_tile.name}\n")
            gem_tile.boat_parts.append("Gem")
            self.gem_tiles_flipped += 1
        
        elif self.compass_tiles_flipped == 2:
            compass_x_tile = self.tiles["compass_v"].x_coordinate
            compass_y_tile = self.tiles["compass_h"].y_coordinate
            compass_tile = self.coordinate_to_tile[(compass_x_tile, compass_y_tile)]
            self.log_file.write(f"Compass has appeared at {compass_tile.name}\n")
            compass_tile.boat_parts.append("Compass")
            self.compass_tiles_flipped += 1


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

    def add_adventurer(self, adventurer):
        self.adventurers.append(adventurer)

    def remove_adventurer(self, adventurer):
        self.adventurers.remove(adventurer)

    def flip(self, adventurer):
        print(f"{adventurer.name} has flipped tile {self.name}")
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
        if self.sand > 1:
            self.blocked = True

    def remove_sand(self):
        self.sand -= 1
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
        print("The well is dry...")


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

    def __init__(self, name, symbol, tile, game, water):
        self.name = name
        self.symbol = symbol
        self.tile = tile  # Current tile where the adventurer is standing
        self.game = game
        self.water = water
        self.max_water = water  # Maximum water they can carry
        self.inventory = []
        self.boat_parts = []

    def __str__(self):
        return f"{self.name} ({self.symbol}) at {self.tile.name}. {self.water} water left. Inventory: {self.inventory}"

    def can_flip(self):
        return not self.tile.flipped and self.tile.sand == 0

    def flip(self):
        self.tile.flip(self)

    def available_sand(self):
        if self.tile.blocked:
            return [self.tile]

        accessible_tiles = []

        if self.tile.sand > 0:
            accessible_tiles = [self.tile]

        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy

            # Check if the new coordinates are within the board boundaries
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.game.coordinate_to_tile.get((new_x, new_y))

                # Check if the adjacent tile is not the storm tile
                if (
                    adjacent_tile
                    and adjacent_tile.name != "storm"
                    and adjacent_tile.sand > 0
                ):
                    accessible_tiles.append(adjacent_tile)

        return accessible_tiles

    def available_moves(self):
        if self.tile.blocked:
            return []

        valid_moves = []
        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy

            # Check if the new coordinates are within board boundaries and not a storm tile
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.game.coordinate_to_tile.get((new_x, new_y))

                if (
                    adjacent_tile
                    and adjacent_tile.name != "storm"
                    and not adjacent_tile.blocked
                ):
                    valid_moves.append((dx, dy))

        return valid_moves

    def move(self, move_direction):
        if move_direction in self.available_moves():
            dx, dy = move_direction
            current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

            new_x, new_y = current_x + dx, current_y + dy
            new_tile = self.game.coordinate_to_tile[(new_x, new_y)]

            # Update the current tile and the adventurer's position
            self.tile.remove_adventurer(self)
            new_tile.add_adventurer(self)
            self.tile = new_tile
        else:
            raise ValueError("Invalid move.")

    def get_water(self):
        self.water += 1
        if self.water > 5:
            self.water = 5

    def lose_water(self):
        self.water -= 1
        if self.water < 0:
            self.water = 0

    def give_water(self, other_adventurer):
        self.water -= 1
        other_adventurer.water += 1

    def give_item(self, other_adventurer, item):
        self.inventory.remove(item)
        other_adventurer.inventory.append(item)

    def clear_sand(self, tile_to_clear):
        if tile_to_clear in self.available_sand():
            tile_to_clear.remove_sand()

    def get_item(self, gear_card):
        self.inventory.append(gear_card)

    def available_items(self):
        return self.inventory

    def use_item(self, item):
        pass

    def pick_part(self, part):
        self.tile.boat_parts.remove(part)
        self.boat_parts.append(part)


class Archeologist(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def ability(self, tile_to_clear):
        if tile_to_clear in self.available_sand:
            tile_to_clear.remove_sand()
            tile_to_clear.remove_sand()


class Climber(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)


class Explorer(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def available_moves(self):
        if self.tile.blocked:
            return []

        valid_moves = []
        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        # Explorer can move diagonally
        directions = [
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy

            # Check if the new coordinates are within board boundaries and not a storm tile
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.game.coordinate_to_tile.get((new_x, new_y))

                if (
                    adjacent_tile
                    and adjacent_tile.name != "storm"
                    and not adjacent_tile.blocked
                ):
                    valid_moves.append((dx, dy))

        return valid_moves

    def available_sand(self):
        if self.tile.blocked:
            return [self.tile]

        accessible_tiles = []

        if self.tile.sand > 0:
            accessible_tiles = [self.tile]

        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        # Climber can remove sand diagonally (including duneblaser.)
        directions = [
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy

            # Check if the new coordinates are within the board boundaries
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.game.coordinate_to_tile.get((new_x, new_y))

                # Check if the adjacent tile is not the storm tile
                if (
                    adjacent_tile
                    and adjacent_tile.name != "storm"
                    and adjacent_tile.sand > 0
                ):
                    accessible_tiles.append(adjacent_tile)

        return accessible_tiles


class Meteorologist(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)


class Navigator(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def ability(self, other_adventurer, move):
        x_move, y_move = move

        new_x = other_adventurer.tile.x_coordinate + x_move
        new_y = other_adventurer.tile.y_coordinate + y_move

        if (0 <= new_x <= 4 and 0 <= new_y <= 4) and not self.game.coordinate_to_tile[
            (new_x, new_y)
        ].blocked:
            other_adventurer.tile.remove_adventurer(other_adventurer)
            other_adventurer.tile = self.game.coordinate_to_tile[(new_x, new_y)]
            other_adventurer.tile.add_adventurer(other_adventurer)
        else:
            raise ValueError("Invalid move for Navigator's ability.")


class WaterCarrier(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def ability(self):
        if (
            self.tile.flipped == True
            and "water" in self.tile.name
            and self.tile.blocked == False
        ):
            self.get_water()
            self.get_water()


class Deck:
    def __init__(self, game):
        self.game = game
        self.deck = self.create()
        self.discard_pile = []
        self.amount = 0  # Amount to cards to draw

    def create(self):
        # create deck of cards
        deck = []

        # add storm cards
        storm_patterns = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # 1 move cards
        for pattern in storm_patterns:
            for i in range(3):
                deck.append(StormCard(f"Storm Moves x1 {i+1}/3", [pattern], self.game))

        # 2 move cards
        for pattern in storm_patterns:
            for i in range(2):
                deck.append(
                    StormCard(f"Storm Moves x2 {i+1}/2", [pattern, pattern], self.game)
                )

        # 3 move cards
        for pattern in storm_patterns:
            for i in range(1):
                deck.append(
                    StormCard(
                        f"Storm Moves x3 {i+1}/1",
                        [pattern, pattern, pattern],
                        self.game,
                    )
                )

        # add sun beats down cards
        for i in range(4):
            deck.append(SBDCard(f"Sun Beats Down {i+1}/4", self.game))

        # add storm picks up cards
        for i in range(3):
            deck.append(SPUCard(f"Storm Picks Up {i+1}/3", self.game))

        return deck

    def amount_to_draw(self):
        """
        Determine the amount of cards to draw according to the storm level.
        Implemented for 5 players.
        """
        if self.game.sand_storm_level <= 1:
            self.amount = 2
        elif 2 <= self.game.sand_storm_level <= 6:
            self.amount = 3
        elif 7 <= self.game.sand_storm_level <= 10:
            self.amount = 4
        elif 11 <= self.game.sand_storm_level <= 13:
            self.amount = 5
        elif 14 <= self.game.sand_storm_level <= 15:
            self.amount = 6
        elif self.game.sand_storm_level > 15:
            self.game.is_game_over = True

    def shuffle(self):
        random.shuffle(self.deck)

    def reshuffle(self):
        self.deck = self.discard_pile
        self.discard_pile = []

        self.shuffle()

    def draw(self):
        drawn_cards = []
        self.amount_to_draw()
        amount = self.amount
        for _ in range(amount):
            if not self.deck:  # Check if the deck is empty. If it is, reshuffle.
                self.reshuffle()

            card = self.deck.pop()
            self.discard_pile.append(card)
            drawn_cards.append(card)

            print(card)
            # Apply the effect of the drawn card
            if isinstance(card, StormCard):
                card.apply()
            elif isinstance(card, SBDCard):
                card.apply(self.game)
            elif isinstance(card, SPUCard):
                self.game.increase_storm_level()
                self.game.log_file.write(f"{card.name}. Storm Level: {self.game.sand_storm_level}. Next turn draw {self.amount} cards.\n\n")

        return drawn_cards  # Return a list of drawn cards

    def __str__(self):
        return "\n".join(str(card) for card in self.deck)


class StormCard:
    def __init__(self, name, moves, game):
        self.name = name
        self.moves = moves
        self.game = game

    def apply(self):
        storm = self.game.tiles["storm"]
        self.game.log_file.write(f"{self.name}, {self.moves}\n\n")
        for move in self.moves:
            x_move, y_move = move
            new_x = storm.x_coordinate + x_move
            new_y = storm.y_coordinate + y_move

            # Check if the move is within board boundaries
            if 0 <= new_x <= 4 and 0 <= new_y <= 4:
                adjacent_tile = self.game.coordinate_to_tile[(new_x, new_y)]
                adjacent_tile.add_sand()
                for adventurer in adjacent_tile.adventurers:
                    adventurer.lose_water()

                storm.swap(adjacent_tile)

    def __str__(self):
        return f"{self.name}, {self.moves}"


class SBDCard:
    def __init__(self, name, game):
        self.name = name
        self.game = game

    def apply(self, tiles): # I dont think we need to pass tiles here? TBD
        self.game.log_file.write(f"{self.name}\n\n")
        for tile in self.game.tiles.values():
            if not tile.flipped and "tunnel" not in tile.name:
                for adventurer in tile.adventurers:
                    adventurer.lose_water()

    def __str__(self):
        return self.name


class SPUCard:
    def __init__(self, name, game):
        self.name = name
        self.game = game

    def __str__(self):
        return self.name


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

    def apply(self, tile):
        tile.sand = 0
        tile.blocked = False
        print("All sand was cleared!")


class JetPack:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def apply(self, adventurer, move):
        adventurer.move(move)


class Terrascope:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def apply(self, tile):
        return tile.name


class SolarShield:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def apply(self):
        pass  # TBD


class TimeThrottle:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def apply(self):
        pass  # TBD


class SecretWaterReserve:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def apply(self, adventurer):
        print(f"{adventurer.name} uses {self.name} on {adventurer.tile.name}.")
        for adventurer in adventurer.tile.adventurers:
            adventurer.get_water()
            adventurer.get_water()
            print(f"{adventurer.name} now has {adventurer.water} units of water.")


def main():
    with open("game_log.txt", "w") as log_file:
        game = Game(log_file)
        print("Starting game...")
        game.start_game()


if __name__ == "__main__":
    main()
