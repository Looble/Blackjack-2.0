class card:
    def __init__(self, number, suit):
        """
        When we initially create a card, we pass the 'number' of the card which
        corresponds to it's value e.g. 1 = A, 2 = 2, 11 = J etc.
        We also set the card's value which will be used to return the score.
        """
        self.suit = suit
        if 1 < number < 11:
            self.value = number
            self.score = number
        elif number == 1:
            self.value = "A"
            self.score = number
        else:
            self.score = 10
            if number == 11:
                self.value = "J"
            elif number == 12:
                self.value = "Q"
            else:
                self.value = "K"
    
    def get_score(self, total_score):
        if self.score == 1:
            if (total_score + 11) > 21:
                return self.score
            else:
                return 11
        else:
            return self.score

    def get_card_details(self):
        return str(str(self.value) + self.suit)
