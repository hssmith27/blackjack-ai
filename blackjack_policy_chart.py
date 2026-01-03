import pickle
from blackjack_agent import BlackjackAgent
from game import BlackjackGame
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

TRUE_COUNT = 0
IS_SOFT = False
IS_SPLIT = False

# Load agent
with open("blackjack_agent.pkl", "rb") as f:
    blackjack_agent = pickle.load(f)

ACTION_TO_NUM = {
    "stand": 0,
    "hit": 1,
    "double": 2,
    "split": 3
}

NUM_TO_ACTION = {
    0: "S",
    1: "H",
    2: "D",
    3: "SP"
}

SPLIT_ACTION_TO_NUM = {
    "stand": 0,
    "hit": 0,
    "double": 0,
    "split": 1
}

NUM_TO_SPLIT = {
    0: "N",
    1: "Y",
}

def get_player_dealer_totals(is_soft=False, is_split=False):
    '''
    Returns a tuple where the first index is a list representing the spread of player hand 
    values based on @is_soft and @is_split, and the second index is a list representing 
    the spread of dealer hand values.
    
    :param is_soft: whether the player hand value is soft or not
    :param is_split: whether the player hand value is splittable or not
    '''
    player_vals = range(7, 18)
    dealer_vals = range(2, 12)

    # If considering soft_hands, we only care about possible soft values
    if is_soft:
        player_vals = range(13, 21)
    elif is_split:
        player_vals = range(4, 24, 2)
    
    return (list(player_vals), list(dealer_vals))

def generate_policy(is_soft=False, is_split=False, true_count=0):
    '''
    Returns a tuple, where each entry is a numpy array. The first entry is used to map player
    and dealer hand values to actions represented as ints. The second entry is a labeled version of the
    previous array.
    
    :param is_soft: whether or not this is for soft hand values
    :param is_split: whether or not this is for splittable hand
    :param true_count: the true count we're checking the policy for
    '''
    totals = get_player_dealer_totals(is_soft, is_split)
    player_totals = totals[0]
    dealer_totals = totals[1]

    policy = np.zeros((len(player_totals), len(dealer_totals)))
    labeled_policy = np.empty(policy.shape, dtype=object)

    # Generate our numpy arrays
    for i, player_val in enumerate(player_totals):
        for j, dealer_val in enumerate(dealer_totals):
            if not is_split:
                policy[i, j] = ACTION_TO_NUM[blackjack_agent.get_policy((player_val, is_soft, dealer_val, False, True, True, true_count))]
                labeled_policy[i, j] = NUM_TO_ACTION[int(policy[i, j])]
            else:
                # Handle splitting aces
                if i == 22:
                    policy[i, j] = SPLIT_ACTION_TO_NUM[blackjack_agent.get_policy((12, True, dealer_val, True, True, True, true_count))]
                else:
                    policy[i, j] = SPLIT_ACTION_TO_NUM[blackjack_agent.get_policy((player_val, False, dealer_val, True, True, True, true_count))]
                labeled_policy[i, j] = NUM_TO_SPLIT[int(policy[i, j])]
    
    return (policy, labeled_policy)

def generate_heat_map(is_soft, is_split, true_count, policy, labeled_policy):
    '''
    Generates a heat map for optimal player actions based on the player and dealer hand values.
    Assumes a fixed @true_count value.
    
    :param is_soft: whether this chart is for soft values
    :param is_split: whether this chart is for split values
    :param true_count: the true count being considered
    :param policy: AI's estimated policy
    :param labeled_policy: labeled version of the estimated policy
    '''
    totals = get_player_dealer_totals(is_soft, is_split)
    player_totals = totals[0]
    dealer_totals = totals[1]

    # Convert to dataframes
    policy_df = pd.DataFrame(policy, index=player_totals, columns=dealer_totals)
    labeled_df = pd.DataFrame(labeled_policy, index=player_totals, columns=dealer_totals)

    # Plot
    sns.heatmap(data=policy_df, fmt="", annot=labeled_df, linewidths=2, linecolor="black", cbar=False)
    plt.title("Blackjack Strategy Chart, Stand Soft 17, True Count: " + str(true_count))
    plt.xlabel("Dealer Hand Value")
    plt.ylabel("Player Hand Value")
    plt.show()

policy_vals, labeled_policy_vals = generate_policy(IS_SOFT, IS_SPLIT, TRUE_COUNT)
generate_heat_map(IS_SOFT, IS_SPLIT, TRUE_COUNT, policy_vals, labeled_policy_vals)

