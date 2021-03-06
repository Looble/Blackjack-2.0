from cards import card, deck, shoe

class player:
    def __init__(self, name, *args, **kwargs):
        self.score = 0
        self.hand = []
        self.name = str(name)

    def get_name(self):
        """
        Return the player's name
        """
        return self.name

    def get_score(self):
        """
        Calculate a player's score based on their hand, if the player's hand
        has not yet been dealt score is set to 0
        """
        score = 0
        if len(self.hand) == 0:
            return 0
        else:
            soft_possible = False
            for card in self.hand:
                addition = card.get_score()
                if addition == 1:
                    if score + 11 <= 21:
                        new_score = score + 11
                        soft_possible = True
                    else:
                        new_score = score + 1
                else:
                    new_score = score + addition
                score = new_score
            if soft_possible and score > 21:
                score = score - 10
        return score

    def soft_score_check(self):
        """
        Check if the player has a soft score based on their total score and if they
        have an Ace in their hand
        """
        if any("A" in card.get_card_details() for card in self.hand):
            ace_detected = False
            score = 0
            for card in self.get_hand():
                if card.get_score() == 1:
                    if not ace_detected:
                        if score + 11 < 21:
                            score += 11
                            ace_detected = True
                        else:
                            score += 1
                    else:
                        score += 1
                else:
                    score += card.get_score()
            if ace_detected and score < 21:
                return True
        return False

    def check_bust(self):
        """
        Check if the player has bust
        """
        if self.get_score() > 21:
            return True
        return False

    def get_viewable_hand(self):
        """
        Return the player's hand in a human readable format
        """
        hand = ""
        for card in self.hand:
            hand = hand + " " + card.get_card_details()
        return hand

    def get_hand(self):
        """
        Return the player's hand with the card objects
        """
        return self.hand

    def hit_hand(self, shoe):
        """
        Take the first card from the deck and add it to the
        player's hand
        """
        card = shoe.get_first_card()
        if card.get_card_details() == "cutcut":
            card = shoe.get_first_card()
        self.hand.append(card)
        return self.hand

    def new_game_reset(self):
        """
        Reset the player's hand and score at the start
        of a new game
        """
        self.score = 0
        self.hand = []

    def __str__(self):
        return self.name
class dealer(player):
    def __init__(self, *args, **kwargs):
        super(dealer, self).__init__(*args, **kwargs)
        self.hidden_card = []

    def check_hide_card(self, shoe):
        """
        Give the dealer a hidden card if necessary, else hit
        """
        if len(self.hand) != 1:
            self.hit_hand(shoe)
        else:
            self.hidden_card.append(shoe.get_first_card())

    def reveal_hidden_card(self):
        """
        Add the dealer's hidden card to their hand
        """
        self.hand.append(self.hidden_card[0])
        return self.hand

    def get_hidden_card_only(self):
        """
        Get the dealer's hidden card
        """
        return self.hidden_card[0]

    def check_hit(self, shoe):
        """
        Check if the dealer should hit
        """
        if self.get_score() < 17:
            return True
        else:
            return False
    
    def reset_dealer(self):
        """
        Extension of the new_game_reset function inhereted from player
        that also resets the dealer's hidden card
        """
        super().new_game_reset()
        self.hidden_card = []

def decide_soft_score_print(current_player):
    """
    Based on the current player/dealer's score decide what needs to be printed
    if it is soft or a blackjack
    """
    string = ""
    score = current_player.get_score()
    if isinstance(current_player, dealer):
        string += "Dealer has "
    else:
        string += "You have "
    if current_player.soft_score_check():
        string += ("soft " + str(score))
    else:
        if check_blackjack(score, current_player.get_hand()):
            string += "blackjack\n"
        else:
            string += str(score) + "\n"
    print(string)

def check_stand(current_player):
    """
    When a player/dealer stands, check what needs to be printed
    """
    string = ""
    score = current_player.get_score()
    if isinstance(current_player, dealer):
        string += "\nDealer "
    else:
        string += "\nPlayer " + str(current_player.get_name()) + " "
    if current_player.check_bust():
        string += "busts\n"
        print(string)
        return True
    else:
        string += "stands with "
        if check_blackjack(score, current_player.get_hand()):
            string += "blackjack\n"
        else:
            string += str(score) + "\n"
        print(string)
        return False

def check_blackjack(score, hand):
    """
    Check if the player/dealer has blackjack
    """
    return score == 21 and len(hand) == 2
