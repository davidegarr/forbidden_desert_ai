# Forbidden Desert AI

## Table of Contents
- [About](#about)
- [Requirements](#requirements)
- [Project structure](#project-structure)
- [Running the code](#running-the-code)
- [Contact](#contact)

## About
This project aims to use reinforced learning to play and master the cooperative board game [Forbidden Desert](https://en.wikipedia.org/wiki/Forbidden_Desert). The goal is to create an AI model that can efficiently make decisions in the game to optimize the chances of survival and success for the team of adventurers.

First part of the project is to implement the game in Python. The second part is to create the model.

## Requirements
### OS
Tested on Windows 11. Compatibility with other operating systems is expected but not guaranteed.

### Python version
Python 3.11.4.

_Note: The project so far uses only the Python standard library, so no additional installations are required beyond the correct Python version._

## Project structure
As for January 2024, there are two folders in the repository.
- art: Contains the pixel art for the eventual representation of the game.
- code: Contains the python files that emulate the Forbidden Desert game. 5 files make up the game:
    - game.py: Main file. Contains the central class that connects all the other files and keeps track of the game status.
    - adventurers.py: All the classes related to the characters that play the game, and their special characteristics and abilities.
    - stormdeck.py and geardeck.py: All the classes related to the movement and state of the storm, and the item cards.
    - tiles.py: Contains all the classes related to the tiles that make up the board.

## Running the code
To run the code, first copy the repo:
```
git clone https://github.com/davidegarr/forbidden_desert_ai.git
```
Then, you can run a random game of Forbidden Desert by running
```
python .\code\game.py
```
This will generate *game_log.txt*. This file contains the log of all the actions performed in the simulated game. After each action the board is printed, as well as the state of each of the adventurers. Notation goes as follows:

### Board
- Each square represents a tile. Each tile is represented by a code (letter(s) + (number)). The letter(s) indicate the tile type, the number (optional), onyl serve as a distinguisher between tiles of the same type. 
    - "S" stands for start tile.
    - "X" stands for storm.
    - "T" stands for tunnel. x3.
    - "B" stands for boat.
    - "Gh" and "Gv" stand for the indicators for the gem boat part. Same applies for motor (Mh and Mv), compass (Ch and Cv) and propellers (Ph and Pv).
    - "W" stands for water wells. x2.
    - "M" stands for mirage.
    - "D" stands for dune tiles. x8.
- A number between parenthesis indicate the number of sand marks on that tile.

### Adventurers
- The archeologist log will display all the adventurers at play, the water left in their canteens, and the items in their inventory.

### Turn numbering
- A number of the format A.B.C is displayed everytime there is a board representation.
    - First digit A represents the round (a round is defined as a turn for each player). Second digit B is the turn (a turn is defined as 4 actions from an adventurer). Third digit C is the action (an action is defined as one of the 4 activities that an adventurer can perform in each turn).

## Contact
For any inquiries, you can find me on Twitter/X [@DavidEgea_](https://twitter.com/davidegea_).