from random import shuffle, randint

def shuffle_shoe(shoe):
    """
    Shuffles the shoe using python's inbuilt shuffle function, then adds a cut card at a random
    point to signify where a new shoe should be generated
    """
    shoe.shuffle()
    # Insert a cut card at between 70 and 80% of the way through the deck to show when a new deck should be generated
    shoe.insert(randint(len(shoe)*.7, len(shoe)*.8), card.generate("cut")) #TODO Add card generation with support for cut cards

def shoe_generation(number_of_decks):
    """
    Creates a new shoe generating the required number of decks and shuffling the shoe to ensure that an appropriate number of cards
    are in play and that the deck is fair for all players
    """
    for i in (1, number_of_decks):
        """
        Generates a new shoe (set of cards used for play) based on the number of decks required
        then uses the shuffle_shoe function above
        """
        shoe += deck.generate() #TODO add deck generation
        shoe = shuffle_shoe(shoe)

    