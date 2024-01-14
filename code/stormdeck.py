import random

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

            #print(card)
            # Apply the effect of the drawn card
            if isinstance(card, StormCard):
                card.apply()
            elif isinstance(card, SBDCard):
                card.apply()
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

    def apply(self):
        self.game.log_file.write(f"{self.name}\n\n")
        for tile in self.game.tiles.values():
            # Check if the tile is safe due to being flipped or a tunnel
            safe_tunnel = tile.flipped and "tunnel" in tile.name
            
            # Check if any adventurer on the tile has an active solar shield
            any_shield_active = any(adventurer.solar_shield_active for adventurer in tile.adventurers)
            
            if not safe_tunnel and not any_shield_active:
                # If the tile isn't safe and no solar shields are active, adventurers lose water
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
