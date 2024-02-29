# Import necessary libraries
import random
import json
import os


# Function to calculate the probability of encountering a deadly hazard in the temple
def calculate_deadly_hazard_probability(cards_drawn_so_far, full_deck):
    # Extract all hazard cards drawn so far
    drawn_hazards = [
        card for card in cards_drawn_so_far if card.type == "hazard"]
    # Calculate the potential danger cards based on the number of drawn hazards
    danger_cards = 2 * len(drawn_hazards)
    # Calculate the total remaining cards in the deck
    total_cards = len(full_deck) - len(cards_drawn_so_far)
    # Calculate and return the probability of encountering a deadly hazard
    probability = danger_cards / total_cards
    return probability


# Function to calculate the expected treasure value based on drawn cards
def calculate_expected_treasure_value(cards_drawn_so_far, treasures, full_deck):
    # Extract all treasure cards drawn so far
    drawn_treasures = [
        card for card in cards_drawn_so_far if card.type == "treasure"]
    # Determine the remaining treasures not yet drawn
    left_treasure = [
        treasure for treasure in treasures if treasure not in drawn_treasures]
    # Calculate the total value of remaining treasures
    total_value = sum([card.value for card in left_treasure])
    # Calculate the total remaining cards in the deck
    total_cards = len(full_deck) - len(cards_drawn_so_far)
    # Calculate and return the expected value of treasures
    expected_value = (total_value / total_cards) / 4
    return expected_value

# Class representing a card in the game
class Card:
    def __init__(self, card_name, card_value):
        self.type = card_name
        self.value = card_value


# Class representing a player in the game
class Player:
    def __init__(self, player_name, choice_to_make):
        self.name = player_name
        self.total_treasure = 0
        self.treasure_in_round = 0
        self.explore = True
        self.strategy = choice_to_make


    def choose_card(self, deck, temple, treasures, hazards):
        strategy_mapping = {
            'A': self.choose_card_random,
            'B': lambda: self.smart_choose_card(deck, temple, treasures, hazards),
            'C': self.ask_card,
        }

        strategy_method = strategy_mapping.get(self.strategy)
        if strategy_method:
            strategy_method()


    def ask_card(self):
        card_choice = input(
            f"{self.name}, choose your card ('E' or anything else): ")
        self.explore = card_choice.upper() == 'E'

    def choose_card_random(self):
        card_choice = random.choices(['E', 'R'], weights=[0.8, 0.2])[0]
        self.explore = card_choice.upper() == 'E'
        print(
            f"{self.name}, choose your card ('E' or anything else): {card_choice} : {self.explore}")

    # Method for a player to choose a card based on a smart strategy
    def smart_choose_card(self, deck, temple, treasures, hazards):
        explore_decision = None

        if len(temple) == 0:
            explore_decision = 'E'
        else:
            # Calculate the probability of encountering a deadly hazard
            deadly_hazard_probability = calculate_deadly_hazard_probability(
                temple, deck)
            # Calculate the expected value of treasures
            treasure_probability = calculate_expected_treasure_value(
                temple, treasures, deck)
            # Set a risk factor for decision making
            risk_factor = 1.65
            # Calculate the risk based on hazard probability, treasure value, and risk factor
            risk = risk_factor * deadly_hazard_probability * \
                self.treasure_in_round / treasure_probability
            # Make a decision based on the adjusted risk
            explore_decision = random.choices(
                ['E', 'R'], weights=[1 - risk, risk])[0]

        self.explore = explore_decision.upper() == 'E'
        print(
            f"{self.name}, choose your card ('E' or anything else): {explore_decision} : {self.explore}")


# Class representing the Incan Gold game
class IncanGoldGame:
    def __init__(self, num_players):
        # Initialize game variables
        self.num_players = num_players
        self.current_round = 0
        self.players = [Player(f"Player {i + 1}", chr(ord('A') + (i % 26))) for i in range(num_players)]
        self.temple = []
        self.deck_base = []
        self.special_treasures = []
        self.treasure_values = [1, 2, 3, 4, 5,
                                5, 7, 7, 9, 11, 11, 13, 14, 15, 17]
        self.treasures = [Card("treasure", i) for i in self.treasure_values]
        self.hazards = [Card("hazard", i)
                        for i in [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]]
        self.special_treasures = [
            Card("specialTreasure", 5 * (i + 1)) for i in range(5)]

        self.deck_base.extend(self.treasures)
        self.deck_base.extend(self.hazards)

        self.deck = self.deck_base.copy()

    # Method to play a round of the game
    def play_round(self):
        # Increment the round number
        self.current_round += 1
        print(f"This is round number: {self.current_round}")

        # Add a special treasure to the deck based on the current round
        self.deck_base.append(self.special_treasures[self.current_round - 1])
        self.deck = self.deck_base.copy()

        # Initialize variables for the round
        players_in_round = list(self.players)
        players_going_back_to_camp = []
        treasure_along_the_way = 0
        special_treasure_to_grab = 0

        for player in self.players:
            player.treasure_in_round = 0

        step_inside_round = 0

        while players_in_round:
            print(f"This is step number {step_inside_round}")

            for player in players_in_round:

                player.choose_card(self.deck, self.temple, self.treasures, self.hazards)

            players_going_back_to_camp.extend(
                [player for player in players_in_round if not player.explore])
            players_in_round = [
                player for player in players_in_round if player.explore]

            print("Players going back to camp are:")

            if len(players_going_back_to_camp) == 1:
                players_going_back_to_camp[0].total_treasure += (
                    players_going_back_to_camp[0].treasure_in_round + treasure_along_the_way + special_treasure_to_grab)
                players_going_back_to_camp[0].treasure_in_round = 0
                print(
                    f"Player Name: {players_going_back_to_camp[0].name}, Total Treasure: {players_going_back_to_camp[0].total_treasure}")
                treasure_along_the_way %= len(players_going_back_to_camp)

            elif players_going_back_to_camp:
                treasure_per_player_going_away = treasure_along_the_way // len(
                    players_going_back_to_camp)
                treasure_along_the_way %= len(players_going_back_to_camp)

                for player in players_going_back_to_camp:
                    player.total_treasure += (player.treasure_in_round +
                                              treasure_per_player_going_away)
                    player.treasure_in_round = 0

                    print(
                        f"Player Name: {player.name}, Total Treasure: {player.total_treasure}")

            # Draw a card from the deck or indicate if it's empty
            if len(self.deck) > 0:
                random_index = random.randint(0, len(self.deck) - 1)
                temple_card = self.deck.pop(random_index)
                self.temple.append(temple_card)
            else:
                print("The deck is empty.  This should not have happened")

            # Process the drawn card based on its type
            if temple_card.type == "treasure":
                print(
                    f"The card is a {temple_card.type} - {temple_card.value}")

                if len(players_in_round) > 0:
                    treasure_per_player_in_round = temple_card.value // len(
                        players_in_round)
                    treasure_along_the_way += temple_card.value % len(
                        players_in_round)

                    for player in players_in_round:
                        player.treasure_in_round += treasure_per_player_in_round

            elif temple_card.type == "hazard":
                print(
                    f"The card is a {temple_card.type} - {temple_card.value}")
                # Check if a hazard with the same value exists among previously drawn hazards
                if any(card.type == "hazard" and card.value == temple_card.value for card in self.temple[:-1]):
                    print("Haha you lost everything!!")
                    for player in players_in_round:
                        player.treasure_in_round = 0
                    players_in_round.clear()

            elif temple_card.type == "specialTreasure":
                print(
                    f"The card is a {temple_card.type} - {temple_card.value}")
                special_treasure_to_grab += temple_card.value
            else:
                raise RuntimeError(f"Unexpected card type: {temple_card.type}")

            players_going_back_to_camp.clear()

            print("Players still going in are:")
            for player in players_in_round:
                print(
                    f"Player Name: {player.name}, Total Treasure: {player.treasure_in_round}")

            print(
                f"Total Treasure left along the way: {treasure_along_the_way}")

            # Log game state for each step
            log_game_state(
                self.current_round,
                self.players,
                self.temple,
                players_in_round,
                players_going_back_to_camp
            )

            step_inside_round += 1

        print("The cards drawn in this round were:")
        for i in self.temple:
            print(f"Card: {i.type} - {i.value}")

        print("Player stats are: ")

        for i in self.players:
            print(
                f"Player Name: {i.name} , Total Treasure: {i.total_treasure}")

        if self.current_round < 5:
            print("Best of luck for the next round!")

        self.temple.clear()
        players_in_round.clear()

    # Method to play the entire game
    def play_game(self):
        for _ in range(5):
            self.play_round()

        for player in self.players:
            print(f"{player.name} - {player.total_treasure}")


# Function to log the game state for each step
def log_game_state(round_num, players, deck, in_round, going_back):
    game_data.append({
        'round': round_num,
        'players': {player.name: player.total_treasure for player in players},
        'deck_state': {card.type: card.value for card in deck},
        'in_round': {player.name: player.explore for player in in_round},
        'going_back': {player.name: player.total_treasure for player in going_back}
    })


# Main entry point for the script
if __name__ == "__main__":
    # Check if the JSON file already exists
    if os.path.exists('game_data.json'):
        # Load existing data from the file
        with open('game_data.json', 'r') as file:
            game_data = json.load(file)
    else:
        # If the file doesn't exist, initialize an empty list
        game_data = []

    # Example usage
    game = IncanGoldGame(3)
    
    game.play_game()

    # Save the updated data to the JSON file
    with open('game_data.json', 'w') as file:
        json.dump(game_data, file)


