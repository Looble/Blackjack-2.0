from random import shuffle, randint


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
    
    def get_score(self):
        """
        A function that returns the amount that should be added to a player's score
        """
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
            for value in range(1, 14):
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

class shoe:
    def __init__(self, number_of_decks, *args, **kwargs):
        """
        Creates a new shoe generating the required number of decks and shuffling the shoe to ensure that an appropriate number of cards
        are in play and that the deck is fair for all players
        """
        self.cards = []
        for _ in range(0, number_of_decks):
            """
            Generates a new shoe (set of cards used for play) based on the number of decks required
            then uses the shuffle_shoe function above
            """
            self.cards += deck().get_all_card_objects()

    def shuffle_shoe(self):
        """
        Shuffles the shoe using python's inbuilt shuffle function, then adds a cut card at a random
        point to signify where a new shoe should be generated
        """
        shuffle(self.cards)
        card_count = len(self.cards)
        # Insert a cut card at between 70 and 80% of the way through the deck to show when a new deck should be generated
        self.cards.insert(randint(round(card_count*.7, 0),
                                  round(card_count*.8, 0)), card("cut"))
        return self.cards

    def get_list_of_card_values(self):
        """
        Return a list of all card values
        """
        card_list = []
        for card in self.cards:
            card_list.append(card.get_card_details())
        return card_list

    def get_first_card(self):
        """
        Return the first card in the shoe and remove it from the shoe
        """
        next_card = self.cards[0]
        self.cards.pop(0)
        return next_card
