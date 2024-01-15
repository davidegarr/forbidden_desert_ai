from adventurers import *
from geardeck import *
from stormdeck import *
from tiles import *
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
        self.total_sand = 0
        self.is_game_over = False  # Status flag to control the game loop
        self.player_order = []  # List that holds the order in which players will take turns
        
        self.round = 1 # A round is defined as a turn for each player
        self.turn = 1 # A turn is defined as 4 actions from an adventurer
        self.action = 1 # An action is defined as one of the 4 activities that an adventurer can perform in each turn
        self.action_points = 4 # Each adventurer can spend 4 action points per turn

        self.setup()  # Perform initial game setup

        self.motor_tiles_flipped = 0
        self.propeller_tiles_flipped = 0
        self.gem_tiles_flipped = 0
        self.compass_tiles_flipped = 0
        self.boat_parts_picked = 0

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
        game_state += self.get_adventurers_representation() + "\n"
        game_state += f"Boat parts collected: {self.boat_parts_picked}/4.\n\n"

        self.log_file.write(game_state)

    def start_game(self):
        self.set_player_order()
        while not self.is_game_over:
            for adventurer in self.player_order:
                self.check_solar_shield(adventurer)
                self.execute_turn(adventurer)
                if self.is_game_over:
                    #print("Game Over")
                    break
            self.round += 1
            self.turn = 1

    def check_solar_shield(self, current_adventurer):
        for adventurer in self.adventurers.values():
            if adventurer.solar_shield_active and adventurer == current_adventurer:
                adventurer.deactivate_solar_shield()
                self.log_file.write(f"{adventurer.name}'s Solar Shield has worn off.\n")

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
        self.action_points = 4 # Each adventurer can spend 4 action points per turn
        
        while self.action_points > 0 and self.is_game_over == False:
            possible_actions = self.get_possible_actions(adventurer)
            chosen_action = random.choice(possible_actions) # Select one of the actions at random
            if chosen_action[0] == "pass":
                self.log_file.write(f"{adventurer} skips their turn.\n\n")
                break
            action_cost = chosen_action[2]
            self.perform_action(adventurer, chosen_action)
            if action_cost > 0:
                self.action += 1
            self.action_points -= action_cost
            self.check_game_status()

        if self.adventurers["climber"].carrying:
            self.adventurers["climber"].drop_off_adventurer()

        self.turn += 1
        self.deck.draw()  # Draw cards from the StormDeck at the end of every turn
        if self.deck.mitigated != 0: #Reset the mitigation from Meteorologist to 0
            self.deck.mitigated = 0

    def get_possible_actions(self, adventurer):
        possible_actions = []
    
        # Rules: "adventurers can take *up to* 4 actions"
        possible_actions.append(("pass", "pass", 0))
        
        # Add "move" actions with their corresponding move directions
        for move in adventurer.available_moves():
            possible_actions.append(("move", move, 1))

        # Check if the adventurer can flip the current tile:
        if adventurer.can_flip():
            possible_actions.append(("flip", adventurer, 1))

        # Check if adventurer can clear sand from any accesible tile
        for tile in adventurer.available_sand():
            possible_actions.append(("remove_sand", tile, 1))
        
        # Check if adventurer can use TimeThrottle from their inventory
        if adventurer.inventory:
            for item in adventurer.inventory:
                if isinstance(item, TimeThrottle):
                    possible_actions.append(("use_item", (adventurer, item), -2))
                
        # Check if any adventurer can use an item:
        for adventurer in self.adventurers.values():
            if adventurer.inventory:
                for item in adventurer.inventory:
                    if isinstance(item, JetPack):
                        for tile in adventurer.available_tiles():
                            possible_actions.append(("use_item", (adventurer, item, tile), 0))
                    elif isinstance(item, Terrascope):
                        for tile in self.tiles.values():
                            if not tile.flipped and tile.name != "storm":
                                possible_actions.append(("use_item", (adventurer, item, tile), 0))
                    elif isinstance(item, SecretWaterReserve):
                        possible_actions.append(("use_item", (adventurer, item), 0))
                    elif isinstance(item, DuneBlaster):
                        for tile in adventurer.available_sand():
                            possible_actions.append(("use_item", (adventurer, item, tile), 0))
                    elif isinstance(item, SolarShield):
                        possible_actions.append(("use_item", (adventurer, item), 0))
        
        # Check if adventurer can perform special ability
        if isinstance(adventurer, Archeologist):
            for tile in adventurer.available_sand():
                possible_actions.append(("ability", tile, 1))
        elif isinstance(adventurer, WaterCarrier):
            if (
            adventurer.tile.flipped == True
            and "water" in adventurer.tile.name
            and adventurer.tile.blocked == False
            ):
                possible_actions.append(("ability", adventurer, 1))
        elif isinstance(adventurer, Navigator):
            for other_adventurer in self.adventurers.values():
                if other_adventurer.name != "navigator":
                    if adventurer.bfs_other_adventurer_available_paths(other_adventurer):
                        for path in adventurer.bfs_other_adventurer_available_paths(other_adventurer).values():
                            possible_actions.append(("ability", (adventurer, other_adventurer, path), 1))
        elif isinstance(adventurer, Climber):
            for other_adventurer in adventurer.tile.adventurers:
                if other_adventurer != adventurer:
                    possible_actions.append(("pick_up_adventurer", (adventurer, other_adventurer), 0))

            if adventurer.carrying:
                possible_actions.append(("drop_off_adventurer", (adventurer), 0))
        elif isinstance(adventurer, Meteorologist):
            self.deck.amount_to_draw()
            if self.deck.amount >= self.deck.mitigated:
                possible_actions.append(("ability", adventurer, 1)) 
        
        # Check if adventurer can pickup a boat piece
        if adventurer.tile.boat_parts and adventurer.tile.flipped and not adventurer.tile.blocked:
            for item in adventurer.tile.boat_parts:
                possible_actions.append(("pick_part", (adventurer, item), 1))

        # Sharing items from inventory
        for tile in self.tiles.values():
            if len(tile.adventurers) > 1:  # There's potential for item sharing
                for i, adv in enumerate(tile.adventurers):
                    if adv.inventory:  # Check if adventurer has items to share
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

        # Move between tunnel tiles
        if isinstance(adventurer.tile, TunnelTile):
            current_tunnel = adventurer.tile
            if not current_tunnel.blocked and current_tunnel.flipped:
                all_tunnels = [self.tiles["tunnel_1"], self.tiles["tunnel_2"], self.tiles["tunnel_3"]]
                for tunnel in all_tunnels:
                    if tunnel.flipped and tunnel != current_tunnel and not tunnel.blocked:
                        possible_actions.append(("use_tunnel", (adventurer, tunnel), 1))
        
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
            self.boat_parts_picked += 1
        elif action_type == "use_tunnel":
            adventurer = chosen_action[1][0]
            tunnel = chosen_action[1][1] # This is the tunnel that the adventurer is travelling to.
            adventurer.use_tunnel(tunnel)
        elif action_type == "use_item":
            adventurer = chosen_action[1][0]
            item = chosen_action[1][1]
            if isinstance(item, TimeThrottle):
                adventurer.inventory.remove(item)
            elif isinstance(item, JetPack):
                destiny_tile = chosen_action[1][2]
                adventurer.use_jetpack(destiny_tile)
                adventurer.inventory.remove(item)
            elif isinstance(item, Terrascope):
                tile_to_reveal = chosen_action[1][2]
                self.log_file.write(f"Tile Revealed: {tile_to_reveal.name}\n\n")
                adventurer.inventory.remove(item)
            elif isinstance(item, SecretWaterReserve):
                item.apply(adventurer)
                adventurer.inventory.remove(item)
            elif isinstance(item, DuneBlaster):
                tile_to_clear = chosen_action[1][2]
                item.apply(tile_to_clear)
                adventurer.inventory.remove(item)
            elif isinstance(item, SolarShield):
                item.apply(adventurer)
                adventurer.inventory.remove(item)
        elif action_type == "ability":
            if isinstance(adventurer, Archeologist):
                tile_to_clear = chosen_action[1]
                adventurer.ability(tile_to_clear)
            elif isinstance(adventurer, WaterCarrier):
                adventurer.ability()
            elif isinstance(adventurer, Navigator):
                navigator = chosen_action[1][0]
                other_adventurer = chosen_action[1][1]
                path = chosen_action[1][2]
                for move in path:
                    navigator.ability(other_adventurer, move)
            elif isinstance(adventurer, Meteorologist):
                adventurer.mitigate()
        elif action_type == "pick_up_adventurer":
            climber = chosen_action[1][0]
            other_adventurer = chosen_action[1][1]
            climber.pick_up_adventurer(other_adventurer)
        elif action_type == "drop_off_adventurer":
            climber = chosen_action[1]
            climber.drop_off_adventurer()

        self.print_game(adventurer, chosen_action)

    def check_game_status(self):
        if any(adventurer.water <= 0 for adventurer in self.adventurers.values()):
            self.is_game_over = True
            self.log_file.write("Game over. An adventurer has run out of water.")
        elif self.total_sand > 48:
            self.is_game_over = True
            self.log_file.write("Game Over. Adventurers have been buried in the sand.")
        elif self.sand_storm_level > 15:
            self.is_game_over = True
            self.log_file.write("Game Over. Sand Storm is too strong.")
        elif self.all_parts_collected() and self.all_adventurers_on_boat():
            self.is_game_over = True
            self.log_file.write("Game won!")

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

    def all_parts_collected(self):
        return self.boat_parts_picked == 4

    def all_adventurers_on_boat(self):
        boat_tile = self.tiles.get("boat")  # Get the boat tile object
        if not boat_tile.blocked:  # Check if boat tile exists and is not blocked
            return all(adventurer.tile == boat_tile for adventurer in self.adventurers.values())
        return False


def main():
    with open("game_log.txt", "w") as log_file:
        game = Game(log_file)
        print("Starting game...")
        game.start_game()


if __name__ == "__main__":
    main()
