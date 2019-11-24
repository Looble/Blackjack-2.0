class card:
    def __init__(self, number, suit="cut"):
        """
        When we initially create a card, we pass the 'number' of the card which
        corresponds to it's value e.g. 1 = A, 2 = 2, 11 = J etc.
        We also set the card's value which will be used to return the score.
        """
        self.suit = suit
        if number == "cut": #If the card being added is the cut card set its score to 0 so it doesn't affect gameplay
            self.value = number
            self.score = 0
        else:
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
        """
        A function that returns the amount that should be added to a player's score
        In the case of an Ace this can vary between a 1 and an 11 since if a player's current score + 11
        is above 21 it automatically reverts to a 1.
        """
        if self.score == 1:
            if (total_score + 11) > 21:
                return self.score
            else:
                return 11
        else:
            return self.score

    def get_card_details(self):
        """
        Return the human-readable identity of the card (e.g. AS, KC, 5H etc.)
        """
        return str(str(self.value) + self.suit)

class deck:
    def __init__(self, *args, **kwargs):
        """
        We create a deck by iterating through the list of suits and creating 13 card objects
        for each suit.
        """
        suits = ['H', 'S', 'D', 'C']
        self.cards = []
        for suit in suits:
            for value in range(13):
                self.cards.append(card(value, suit))

    def get_all_card_objects(self):
        """
        Return a list of all the card objects within the deck
        """
        return self.cards

    def get_all_card_values(self):
        """
        Return a human-readable list of all cards in the deck
        """
        card_values = []
        for card in self.cards:
            card_values.append(card.get_card_details())
        return card_values
