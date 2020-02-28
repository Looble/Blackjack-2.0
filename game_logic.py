from cards import card, deck, shoe

class player:
    def __init__(self, *args, **kwargs):
        self.score = 0
        self.hand = []

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
        if self.get_score() > 21:
            return True
        return False

    def get_viewable_hand(self):
        hand = ""
        for card in self.hand:
            hand = hand + " " + card.get_card_details()
        return hand

    def get_hand(self):
        return self.hand

    def hit_hand(self, shoe):
        self.hand.append(shoe.get_first_card())
        return self.hand

class dealer(player):
    def __init__(self, *args, **kwargs):
        super(dealer, self).__init__(*args, **kwargs)
        self.hidden_card = []

    def check_hide_card(self, shoe):
        if len(self.hand) != 1:
            self.hit_hand(shoe)
        else:
            self.hidden_card.append(shoe.get_first_card())

    def reveal_hidden_card(self):
        self.hand.append(self.hidden_card[0])
        return self.hand

    def get_hidden_card_only(self):
        return self.hidden_card[0]

    def check_hit(self, shoe):
        if self.get_score() < 17:
            return True
        else:
            return False

def decide_soft_score_print(current_player):
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
    string = ""
    score = current_player.get_score()
    if isinstance(current_player, dealer):
        string += "\nDealer "
    else:
        string += "\nPlayer "
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
    return score == 21 and len(hand) == 2