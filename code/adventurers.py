from collections import deque

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
        self.solar_shield_active = False

    def __str__(self):
        return f"{self.name} ({self.symbol}) at {self.tile.name}. {self.water} water left. Inventory: {self.inventory}"

    def __repr__(self):
        return f"{self.name}"

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

    def use_tunnel (self, tunnel):
        # Update the current tile and the adventurer's position
        self.tile.remove_adventurer(self)
        tunnel.add_adventurer(self)
        self.tile = tunnel

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

    def available_tiles(self):
        available_tiles = []
        for tile in self.game.tiles.values():
            if tile.blocked == False and tile.name != "storm":
                available_tiles.append(tile)
        return available_tiles

    def use_jetpack(self, landing_tile):
        self.tile.remove_adventurer(self)
        landing_tile.add_adventurer(self)
        self.tile = landing_tile

    def activate_solar_shield(self):
        self.solar_shield_active = True
    
    def deactivate_solar_shield(self):
        self.solar_shield_active = False


class Archeologist(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def ability(self, tile_to_clear):
        if tile_to_clear in self.available_sand():
            tile_to_clear.remove_sand()
            tile_to_clear.remove_sand()


class Climber(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)
        self.carrying = None # Track the adventurer being carried
    
    def pick_up_adventurer(self, adventurer_to_pick):
        self.carrying = adventurer_to_pick
    
    def drop_off_adventurer(self):
        self.carrying = None

    def available_moves(self):
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
                ):
                    valid_moves.append((dx, dy))

        return valid_moves
    
    def move(self, move_direction):
        dx, dy = move_direction
        current_x, current_y = self.tile.x_coordinate, self.tile.y_coordinate

        new_x, new_y = current_x + dx, current_y + dy
        new_tile = self.game.coordinate_to_tile[(new_x, new_y)]

        self.tile.remove_adventurer(self)
        new_tile.add_adventurer(self)
        self.tile = new_tile

        # If carrying another adventurer, update their position too
        if self.carrying:
            self.carrying.tile.remove_adventurer(self.carrying)
            new_tile.add_adventurer(self.carrying)
            self.carrying.tile = new_tile
            self.drop_off_adventurer


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

    def bfs_other_adventurer_available_paths(self, adventurer):
        # Navigator can move up to 3 tiles another adventurer
        max_length = 3
        initial_position = adventurer.tile

        # Stores as key the tiles visited, and as value the list of moves needed to get there
        visited_squares = {initial_position: []}
        available_paths = {}
        queue = deque([(initial_position, [])])

        while queue:
            current_tile, path = queue.popleft()
            path_length = len(path)

            if path_length >= max_length:
                continue

            # Generate available moves from the current tile
            for move in self.available_moves_in_remote_tile(adventurer, path):
                new_tile = self.calculate_new_tile(current_tile, move)
                if new_tile not in visited_squares:
                    # Add the new tile to the visited squares with the path taken to get there
                    visited_squares[new_tile] = path + [move]
                    queue.append((new_tile, path + [move]))
                    available_paths[new_tile] = path + [move]
        
        # Visited squares contains the available paths that can move the aventurer up to 3 tiles
        print(available_paths, "\n")
        if available_paths:
            return available_paths
        return None

    def available_moves_in_remote_tile(self, adventurer, path):
        # Save the original position
        original_tile = adventurer.tile

        # Temporarily move the adventurer along the path
        for move in path:
            dx, dy = move
            new_x = adventurer.tile.x_coordinate + dx
            new_y = adventurer.tile.y_coordinate + dy
            adventurer.tile = self.game.coordinate_to_tile[(new_x, new_y)]

        # Now that the adventurer is "at" the end of the path, calculate available moves
        available_moves = adventurer.available_moves()

        # Reset the adventurer's position to the original tile
        adventurer.tile = original_tile

        return available_moves

    def calculate_new_tile(self, current_tile, move):
        dx, dy = move
        current_x, current_y = current_tile.x_coordinate, current_tile.y_coordinate

        new_x, new_y = current_x + dx, current_y + dy
        new_tile = self.game.coordinate_to_tile[(new_x, new_y)]

        return new_tile

    def ability(self, other_adventurer, move):
        x_move, y_move = move

        new_x = other_adventurer.tile.x_coordinate + x_move
        new_y = other_adventurer.tile.y_coordinate + y_move

        other_adventurer.tile.remove_adventurer(other_adventurer)
        other_adventurer.tile = self.game.coordinate_to_tile[(new_x, new_y)]
        other_adventurer.tile.add_adventurer(other_adventurer)


class WaterCarrier(Adventurer):
    def __init__(self, name, symbol, tile, game, water):
        super().__init__(name, symbol, tile, game, water)

    def ability(self):
        self.get_water()
        self.get_water()

