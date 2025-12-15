import pickle
from blackjack_agent import BlackjackAgent
from game import BlackjackGame

# Load agent
with open("blackjack_agent.pkl", "rb") as f:
    blackjack_agent = pickle.load(f)

total_winnings = 0
total_bet = 0
game = BlackjackGame()

MAX_ITER = 100000
BETTING_UNITS = 10

def get_bet_sizing(true_count):
    '''
    Returns a bet size based on @true_count
    
    :param true_count: true count of deck
    '''
    return max(BETTING_UNITS, BETTING_UNITS * (true_count))

# Test our agent MAX_ITER times
for _ in range(MAX_ITER):
    # Get our bet sizing
    bet = get_bet_sizing(game.bin_true_count(game.get_true_count()))

    # Deal player and dealer
    game.deal_player()
    game.deal_dealer(False)
    game.deal_player()
    game.deal_dealer(True)

    # Check for dealer blackjack
    if not game.is_dealer_blackjack():
        # Iterate over each player hand and let them play actions
        while game.get_current_hand() < game.get_num_hands():
            # Add a card for recently split hands
            if game.get_current_hand_length() == 1:
                game.deal_player()

            state = game.get_state()
            
            # Perform an action
            action = blackjack_agent.get_policy(state)

            if action == 'hit':
                game.hit()
            elif action == 'stand':
                game.stand()
            elif action == 'double':
                game.double_down()
            elif action == 'split':
                game.split()

            # Evaluate if the hand ended
            game.update_current_hand()

    # Evaluate payouts after playing dealer if needed
    payouts = game.evaluate_hand()
    total_payoff = 0

    for payout in payouts:
        total_bet += abs(payout) * bet
        total_payoff += payout

    total_winnings += total_payoff * bet

    # Reset game to prepare for a new hand
    game.reset()

print(f"Player Edge over {MAX_ITER} hands: {((total_winnings / total_bet) * 100):.2f}%")
print(blackjack_agent.get_policy((11, False, 8, False, True, True, 5)))
