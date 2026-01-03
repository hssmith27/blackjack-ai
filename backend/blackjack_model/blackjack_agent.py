import random
from collections import defaultdict
from blackjack_model.game import BlackjackGame

class BlackjackAgent:
    '''
    Blackjack AI Agent trained by Q-learning where state is a tuple of the form:
    (player_hand_val, is_soft, dealer_hand_val, can_split, can_double, can_act, true_count)
    '''
    def __init__(self, alpha=0.01, epsilon=1.0, gamma=0.999):
        '''
        :param alpha: Learning rate
        :param epsilon: Random choice probability
        :param gamma: Discount factor
        '''
        self.q_vals = defaultdict(float)
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.game = BlackjackGame()
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99999999
        self.alpha_min = 0.0001
        self.alpha_decay = 0.99999999

    def get_q_val(self, state, action):
        '''
        Returns Q(state, action)
        
        :param state: current state we're in
        :param action: action we're taking from that state
        '''
        if (state, action) in self.q_vals:
            return self.q_vals[(state, action)]
        return 0.0
    
    def compute_max_q_val(self, state):
        '''
        Returns Q(state, action) based on the action that maximizes
        the output

        :param state: the state we're finding the optimal Q of
        '''
        best_action = self.compute_best_action(state)

        return self.get_q_val(state, best_action)
    
    def get_legal_actions(self, state):
        '''
        Returns legal actions from a given state

        :param state: state we want legal actions from
        '''
        legal_actions = []

        # If we can act, add hit and stand
        can_act = state[5]
        if can_act:
            legal_actions.append('hit')
            legal_actions.append('stand')
        
        # If we can split, add split
        can_split = state[3]
        if can_split:
            legal_actions.append('split')

        # If we can double, add double
        can_double = state[4]
        if can_double:
            legal_actions.append('double')

        return legal_actions

    def compute_best_action(self, state):
        '''
        Returns the best action to take in a state.

        :param state: the state we're finding the best action from
        '''
        best_actions = [None]
        best_val = 0.0
        
        # Iterate over actions and choose the best
        for action in self.get_legal_actions(state):
            q_val = self.get_q_val(state, action)
            
            # If we don't have a best action yet or q val is better, update the best action
            if best_actions[0] is None or q_val > best_val:
                best_val = q_val
                best_actions = [action]
            # If we have a tie, add it to the list of best actions
            elif q_val == best_val:
                best_actions.append(action)

        return random.choice(best_actions)
    
    def get_action(self, state):
        '''
        Compute action to take in current state with an epsilon-greedy algorithm

        :param state: state we're computing an action from
        '''
        legal_actions = self.get_legal_actions(state)
        action = None

        if not legal_actions:
            return None

        # With probability epsilon choose a random action
        if random.random() <= self.epsilon:
            action = random.choice(legal_actions)

        # Otherwise choose the best action
        else:
            action = self.compute_best_action(state)

        return action
    
    def update(self, state, action, next_state, reward):
        '''
        Updates q value table

        :param state: state we start in
        :param action: action we take from state
        :param next_state: state we end up in
        :param reward: reward we get for entering @next_state
        '''
        learning_rate = self.alpha
        original_q = self.get_q_val(state, action)

        # Compute sampled Q-state utility
        sampled_util = reward + (self.gamma * self.compute_max_q_val(next_state))

        # Update Q val
        self.q_vals[(state, action)] = ((1 - learning_rate) * original_q) + (learning_rate * sampled_util)

    def get_policy(self, state):
        '''
        Returns optimal policy at a given state

        :param state: state we want the best action from
        '''
        return self.compute_best_action(state)
    
    def run_episode(self):
        '''
        Runs an episode of blackjack for Q-learning, where an episode is a hand
        '''
        game = self.game

        # Stores tuples of the form (state, action, terminal_state) to compute Q-vals with payoffs
        terminal_values = []

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
                is_split = False

                # Perform an action
                action = self.get_action(state)
                if action == 'hit':
                    game.hit()
                elif action == 'stand':
                    game.stand()
                elif action == 'double':
                    game.double_down()
                elif action == 'split':
                    is_split = True
                    game.split()
                
                hand_over = game.get_hand_over()
                next_state = game.get_state()

                # Update our q-values
                if not hand_over:
                    self.update(state, action, next_state, 0)
                    
                    # If split use next hand as well for the calculation
                    if is_split:
                        self.update(state, action, game.get_next_state(), 0)
                else:
                    terminal_values.append((state, action, next_state))

                # Evaluate if the hand ended
                game.update_current_hand()
        
        # Evaluate payouts after playing dealer if needed
        payouts = game.evaluate_hand()

        for i in range(len(terminal_values)):
            state, action, next_state = terminal_values[i]

            # Update state based on dealer action
            reward = payouts[i]
            self.update(state, action, next_state, reward)

        # Reset game to prepare for a new hand
        game.reset()

        # Update epsilon and alpha
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.alpha = max(self.alpha_min, self.alpha * self.alpha_decay)