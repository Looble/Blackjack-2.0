from random import randint, shuffle

from deck import card, deck

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
        self.cards.insert(randint(round(card_count*.7, 0), round(card_count*.8, 0)), card("cut"))
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
