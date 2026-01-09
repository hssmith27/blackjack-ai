import pickle
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS
from blackjack_model.game import BlackjackGame
from blackjack_model.blackjack_agent import BlackjackAgent

app = Flask(__name__)

# Allows frontend to access @app
CORS(app)

# Read in our trained agent's policy
POLICY_PATH = "backend/blackjack_model/blackjack_agent.pkl"

try: 
    with open(POLICY_PATH, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print(f"Policy model could not be found at {POLICY_PATH}")
    sys.exit(1)
except Exception as e:
    print(f"Failed to load policy model: {e}")
    sys.exit(1)

# Send state information to get policy
@app.route('/get_policy', methods=['POST'])
def get_policy():
    data = request.json
    player_cards = data.get('player_cards', '')
    dealer_card = data.get('dealer_card', '')
    true_count = data.get('true_count', '')

    state = convert_to_state(player_cards, dealer_card, true_count)

    return jsonify({"policy": model.get_policy(state)})

def validate_card(card):
    '''
    Raises an error if a card is invalid
    
    :param card: the card we're checking
    '''
    if not isinstance(card, str):
        raise ValueError("Card must be represented as a string")
    if len(card) != 2:
        raise ValueError("Card must be of length 2")
    if card[0] not in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"]:
        raise ValueError("Invalid rank")
    if card[1] not in ["H", "D", "C", "S"]:
        raise ValueError("Invalid suit")

def validate_input(player_cards, dealer_card, true_count):
    '''
    Raises an error if given input is invalid
    
    :param player_cards: a list if player cards
    :param dealer_card: a string representing the dealer's shown card
    :param true_count: the true count of the deck
    '''
    # Validate player cards
    if not isinstance(player_cards, list):
        raise ValueError("Player cards must be a list")
    for card in player_cards:
        validate_card(card)

    # Validate dealer card
    validate_card(dealer_card)

    # Validate true count
    if not isinstance(true_count, int):
        raise ValueError("True count must be an int")
    if not -5 <= true_count <= 5:
        raise ValueError(f"True count of {true_count} is invalid, must be in the range [-5, 5]")

def convert_to_state(player_cards, dealer_card, true_count):
    '''
    Converts given parameters to a state tuple for the blackjack model
    
    :param player_cards: a list of player cards
    :param dealer_card: a string representing the dealer's shown card
    :param true_count: the true count of the deck
    '''
    validate_input(player_cards, dealer_card, true_count)

    can_double = len(player_cards) == 2
    dealer_hand_val = calc_card_value(dealer_card)
    can_split = len(player_cards) == 2 and calc_card_value(player_cards[0]) == calc_card_value(player_cards[1])
    player_hand_val = 0
    soft_aces = 0

    # Calculate total player hand value and the number of soft aces
    for card in player_cards:
        val = calc_card_value(card)
        player_hand_val += val

        # Calculate number of soft aces
        if val == 11:
            soft_aces += 1
    
    # Reduce aces to prevent busting
    while soft_aces > 0 and player_hand_val > 21:
        if player_hand_val + 10 < 22:
            player_hand_val -= 10
            soft_aces -= 1
        else:
            break

    is_soft = bool(soft_aces)

    return (player_hand_val, is_soft, dealer_hand_val, can_split, can_double, True, true_count)

def calc_card_value(card):
    '''
    Returns the value of a given card
    
    :param card: the inputted card represented as the rank followed by the suit
                 (0 represents 10)
    '''
    rank = card[0]
    if rank == "A":
        return 11
    elif rank in ["0", "J", "Q", "K"]:
        return 10
    else:
        return int(rank)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)