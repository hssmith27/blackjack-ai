import random

class BlackjackGame:
    '''
    Blackjack Game Environment
    '''
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, num_decks=6, penetration=0.8):
        '''
        :param num_decks: Number of decks in the shoe
        :param penetration: What portion of cards are dealt before reshuffling
        '''
        # Check valid params
        if not isinstance(num_decks, int):
            raise TypeError("num_decks must be an int")
        if num_decks < 1:
            raise ValueError("num_decks must be at least 1")
        if not isinstance(penetration, float):
            raise TypeError("penetration must be a float")
        if not (0 < penetration < 1):
            raise ValueError("penetration must be between 0 and 1")
        
        self.num_decks = num_decks
        self.penetration = penetration

        self.count = 0

        # Tracks which player hand is active
        self.current_hand = 0

        self.hand_over = False
        self.player_hands = [[]]
        self.dealer_hand = []
        self.hidden_card = ""

        # Tracks payouts for player hands
        self.payouts = [-1]

        self.shoe = []
        self.create_shoe()

    def get_hand_over(self):
        '''
        Returns if the current hand is over
        '''
        return self.hand_over

    def get_current_hand(self):
        '''
        Returns which hand is active
        '''
        return self.current_hand
    
    def get_current_hand_length(self):
        '''
        Returns length of current hand
        '''
        return len(self.player_hands[self.current_hand])
    
    def get_num_hands(self):
        '''
        Returns the number of player hands
        '''
        return len(self.player_hands)
    
    def can_split(self):
        '''
        Returns whether the player can split or not
        '''
        if self.hand_over:
            return False

        active_hand = self.player_hands[self.current_hand]
            
        return len(active_hand) == 2 and self.get_val(active_hand[0]) == self.get_val(active_hand[1])
    
    def can_double(self):
        '''
        Returns whether the player can double down
        '''
        if self.hand_over:
            return False
        
        active_hand = self.player_hands[self.current_hand]

        return len(active_hand) == 2

    def get_val(self, card):
        '''
        Returns the value of a card
        '''
        tens = ['10', 'J', 'Q', 'K']

        if card == 'A':
            return 1
        elif card in tens:
            return 10
        else:
            return int(card)

    def create_shoe(self):
        '''
        Sets and shuffles the shoe of the game, where each rank appears 4 times for each deck
        '''
        res = []
        self.count = 0

        # Create all cards
        for deck in range(self.num_decks):
            for rank in BlackjackGame.ranks:
                for suit in range(4):
                    res.append(rank)
        
        # Shuffle and set shoe
        random.shuffle(res)
        self.shoe = res

    def get_true_count(self):
        '''
        Returns the rounded true count of the deck
        '''
        if len(self.shoe) == 0:
            return 0
        
        decks_remaining = len(self.shoe) / 52
        
        return round(self.count / decks_remaining)

    def deal_player(self):
        '''
        Deals the active player hand one card
        '''
        if len(self.shoe) == 0:
            self.create_shoe()

        card = self.shoe.pop()
        self.update_count(card)
        self.player_hands[self.current_hand].append(card)
    
    def deal_dealer(self, hidden):
        '''
        Deals the dealer one card

        :param hidden: Whether the card is hidden to the player
        '''
        if len(self.shoe) == 0:
            self.create_shoe()

        card = self.shoe.pop()

        if not hidden:
            self.update_count(card)
            self.dealer_hand.append(card)
        else:
            self.hidden_card = card

    def update_count(self, card):
        '''
        Updates the count based on the given @card
        
        :param card: the card to be added to the count
        '''
        low = ['2', '3', '4', '5', '6']
        high = ['10', 'J', 'Q', 'K', 'A']

        if card in low:
            self.count += 1
        elif card in high:
            self.count -= 1

    def update_current_hand(self):
        '''
        Updates the current hand index if a hand ended
        '''
        if self.hand_over:
            self.hand_over = False
            self.current_hand += 1

    def hit(self):
        '''
        Performs hit action
        '''
        self.deal_player()
        self.check_bust()

    def stand(self):
        '''
        Performs stand action
        '''
        # End current hand
        self.hand_over = True
    
    def double_down(self):
        '''
        Performs double down action
        '''
        self.deal_player()
        self.payouts[self.current_hand] *= 2

        # End current hand
        self.hand_over = True

    def split(self):
        '''
        Performs split action
        '''
        # Split hands
        self.payouts.insert(self.current_hand + 1, -1)
        first_val = self.player_hands[self.current_hand][0]
        second_val = self.player_hands[self.current_hand][1]
        self.player_hands[self.current_hand] = [first_val]
        self.player_hands.insert(self.current_hand + 1, [second_val])

        # Deal an extra card to each hand
        self.deal_player()
        self.current_hand += 1
        self.deal_player()
        self.current_hand -= 1

    def get_player_val(self, hand=None):
        '''
        Returns a tuple as:
        (the value of the selected player hand, is soft)
        If the value is 22, the player busted

        :param hand: the hand to get the value of
        '''
        value = 0
        is_soft = False
        ace_count = 0

        # If we aren't given a hand, assume they want the value of the active hand
        if hand is None:
            hand = self.current_hand

        # Count # of aces and sum all other values
        for card in self.player_hands[hand]:
            if card == 'A':
                ace_count += 1
            elif card in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card)

        # Handle aces
        for _ in range(ace_count):
            value += 1
        if ace_count > 0 and value + 10 <= 21:
            value += 10
            is_soft = True

        # Special value for bust
        if value > 21:
            value = 22

        return (value, is_soft)

    def get_dealer_val(self, hidden):
        '''
        Returns the value of the dealer hand
        If the value is 22, the dealer busted
        
        :param hidden: Whether to include the hidden card in the hand value
        '''
        value = 0
        ace_count = 0

        # Count # of aces and sum all other values
        for card in self.dealer_hand:
            if card == 'A':
                ace_count += 1
            elif card in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card)

        # Manage hidden card
        if hidden:
            card = self.hidden_card
            if card == 'A':
                ace_count += 1
            elif card in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card)

        # Handle aces
        for _ in range(ace_count):
            value += 1
        if ace_count > 0 and value + 10 <= 21:
            value += 10
            
        # Special value for bust
        if value > 21:
            value = 22
        return value

    def check_bust(self):
        '''
        Updates the current hand if the player busted
        '''
        if self.get_player_val()[0] > 21:
            self.hand_over = True

    def is_dealer_done(self):
        '''
        Returns whether or not the dealer's turn is over
        '''
        return self.get_dealer_val(False) >= 17
    
    def reveal_card(self):
        '''
        Adds the hidden card to the dealer's hand and updates the count
        '''
        card = self.hidden_card
        self.dealer_hand.append(card)
        self.update_count(card)
        self.hidden_card = ""
    
    def is_player_blackjack(self, hand):
        '''
        Returns whether or not the player hand at index @hand is a blackjack

        :param hand: The hand index being checked
        '''
        return self.get_player_val(hand)[0] == 21 and len(self.player_hands[hand]) == 2

    def is_dealer_blackjack(self):
        '''
        Returns if dealer has blackjack
        '''
        if self.hidden_card:
            return self.get_dealer_val(True) == 21

    def evaluate_hand(self):
        '''
        Returns a factor representing the player's win or loss for each hand
        '''
        player_hand_vals = []

        # Whether dealer has to play
        dealer_action = False

        # Calculate player hand values to determine dealer action
        for i in range(len(self.player_hands)):
            hand_value = self.get_player_val(i)[0]

            if hand_value < 21 or (hand_value == 21 and not self.is_player_blackjack(i)):
                dealer_action = True

            player_hand_vals.append(hand_value)
        
        # Reveal hidden dealer card
        self.reveal_card()

        # If dealer action, play dealer
        if dealer_action:
            while self.get_dealer_val(False) < 17:
                self.deal_dealer(False)

        dealer_val = self.get_dealer_val(False)

        # Update payouts
        for i in range(len(player_hand_vals)):
            player_hand_val = player_hand_vals[i]

            # Handle blackjack cases
            if self.is_dealer_blackjack():
                if self.is_player_blackjack(i):
                    self.payouts[i] *= 0
            elif self.is_player_blackjack(i):
                self.payouts[i] *= -1.5

            # Handle payouts for hands that didn't bust
            elif player_hand_val <= 21:
                if dealer_val > 21 or player_hand_val > dealer_val:
                    self.payouts[i] *= -1
                elif dealer_val == player_hand_val:
                    self.payouts[i] *= 0

        return self.payouts

    def reset(self):
        '''
        Resets the hand and reshuffles the shoe if necessary
        '''
        # Resetting variables to defaults
        self.current_hand = 0
        self.hand_over = False
        self.player_hands = [[]]
        self.dealer_hand = []
        self.hidden_card = ""
        self.payouts = [-1]

        if 1 - (len(self.shoe) / (52 * self.num_decks)) >= self.penetration:
            self.create_shoe()

    def get_state(self):
        '''
        Returns a copy of the state
        '''
        player_val = self.get_player_val()

        return (player_val[0], player_val[1], self.get_dealer_val(False), self.can_split(), self.can_double(), not self.hand_over, self.bin_true_count(self.get_true_count()))

    def get_next_state(self):
        '''
        Returns a copy of the next hand's state
        '''
        self.current_hand += 1

        player_val = self.get_player_val()
        state = (player_val[0], player_val[1], self.get_dealer_val(False), self.can_split(), self.can_double(), not self.hand_over, self.bin_true_count(self.get_true_count()))
        self.current_hand -= 1

        return state

    def bin_true_count(self, true_count):
        '''
        Returns 5 if @true_count >= 5, -5 if @true_count <= -5, @true_count otherwise

        :param true_count: Description
        '''
        if true_count >= 5:
            return 5
        elif true_count <= -5:
            return -5
        return true_count