import pickle

from flask import Flask, request, jsonify
from flask_cors import CORS
from blackjack_model.game import BlackjackGame
from blackjack_model.blackjack_agent import BlackjackAgent

app = Flask(__name__)

# Allows frontend to access @app
CORS(app)

# Read in our trained agent's policy
with open("backend/blackjack_ai/blackjack_agent.pkl", "rb") as file:
    model = pickle.load(file)

# Send state information to get policy
@app.route('/get_policy', methods=['POST'])
def get_policy():
    data = request.json
    player_cards = data.get('player_cards', '')
    dealer_card = data.get('dealer_card', '')
    true_count = data.get('true_count', '')

    state = convert_to_state(player_cards, dealer_card, true_count)

    return jsonify({"policy": model.get_policy(state)})

def convert_to_state(player_cards, dealer_card, true_count):
    '''
    Converts given parameters to a state tuple for the blackjack model
    
    :param player_cards: a list of player cards
    :param dealer_card: a string representing the daeler's shown card
    :param true_count: the true count of the deck
    '''
    can_double = len(player_cards) == 2

    return (player_hand_val, is_soft, dealer_hand_val, can_split, can_double, True, true_count)

def calc_card_value(card):
    '''
    Returns the value of a given card
    
    :param card: the inputted card represented as the rank followed by the suit
                 (0 represents 10)
    '''
    rank = card[0]
    if rank == "A":
        return 1
    elif rank in ["0", "J", "Q", "K"]:
        return 10
    else:
        return int(rank)

print(calc_card_value("2S"))
if __name__ == 'main':
    app.run(host='127.0.0.1', port=5000, debug=False)