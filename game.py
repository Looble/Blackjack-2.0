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
        # Insert a cut card at between 70 and 80% of the way through the deck to show when a new deck should be generated
        # shoe.insert(randint(len(shoe)*.7, len(shoe)*.8), card.generate("cut")) #TODO Add card generation with support for cut cards
        return self.cards
    
    def get_list_of_card_values(self):
        """
        Return a list of all card values
        """
        card_list = []
        for card in self.cards:
            card_list.append(card.get_card_details())
        return card_list
