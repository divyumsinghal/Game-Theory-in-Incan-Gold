
# Game-Theory-in-Incan-Gold

## Overview

This Python program simulates the Incan Gold game, a press-your-luck adventure where players explore a temple, collecting treasures and avoiding hazards. The simulation includes a game class (`IncanGoldGame`), player class (`Player`), and functions for calculating probabilities and logging game states.

## Files

- **`incan_gold.py`:**
  - The main script containing the Incan Gold game simulation, classes, and functions.

- **`game_data.json`:**
  - A JSON file that stores game state data after each execution of the script.

## Classes

### `IncanGoldGame`

- Represents the Incan Gold game.
- Manages the game state, players, rounds, and card interactions.

### `Player`

- Represents a player in the game.
- Has attributes for the player's name, total treasure, treasure in the current round, and explore decision.
- Provides methods for choosing cards randomly or based on a smart strategy.

### `Card`

- Represents a card in the game.
- Has attributes for the type of card (hazard, treasure, special treasure) and its associated value.

## Functions

### `calculate_deadly_hazard_probability(cards_drawn_so_far, full_deck)`

- Calculates the probability of encountering a deadly hazard in the temple exploration scenario.

### `calculate_expected_treasure_value(cards_drawn_so_far, treasures, full_deck)`

- Calculates the expected treasure value based on the drawn cards during the temple exploration.

### `log_game_state(round_num, players, deck, in_round, going_back)`

- Logs the game state for each step, including player details, deck state, and participants in the current round and those going back to camp.

## Usage

1. **Run the Script:**
   - Execute the `incan_gold.py` script to simulate the Incan Gold game.

2. **View Game Data:**
   - After each execution, the game state data is logged in the `game_data.json` file.

3. **Customization:**
   - Customize the script or classes for different game scenarios or rule variations.


## Requirements

- Python 3.x

## Notes

- The program uses random elements, so results may vary between executions.

Feel free to explore and enjoy the simulated Incan Gold adventure!
