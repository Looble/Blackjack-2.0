import unittest
from game import shoe_generation
from deck import card

class TestCard(unittest.TestCase):
    """
    Tests that cover the card class
    """

    # @unittest.skip
    def test_card_creation(self):
        """
        Test that cards can be created successfully and that values are correct for Aces, numbers
        and pictures (king, queen, jack)
        """
        self.assertEquals(card(1, "H").get_card_details(), "AH")
        self.assertEquals(card(4, "H").get_card_details(), "4H")
        self.assertEquals(card(11, "H").get_card_details(), "JH")
        self.assertEquals(card(12, "H").get_card_details(), "QH")
        self.assertEquals(card(13, "H").get_card_details(), "KH")
        

    def test_ace_card_score_calculation(self):
        """
        Test that an ace will return a score of 11 when the new score will be equal to or below 21
        else returning a score of 1
        """
        test_card = card(1, "H")
        self.assertEquals(test_card.get_score(10), 11) # Test that a new score of 21 will return an 11
        self.assertEquals(test_card.get_score(9), 11) # Test that a new score of less than 21 will return an 11
        self.assertEquals(test_card.get_score(13), 1) # Test that a new score above 21 returns a 1

    def test_picture_card_score_calculation(self):
        """
        Test that picture cards (King, Queen, Jack) all return a score of 10
        """
        self.assertEquals(card(11, "H").get_score(1), 10)
        self.assertEquals(card(12, "H").get_score(1), 10)
        self.assertEquals(card(13, "H").get_score(1), 10)

class TestShoe(unittest.TestCase):
    """
    Tests that cover the deck class
    """
    @unittest.skip
    def test_shoe_creation(self):
        """
        Test that the shoe is created with the correct number of cards
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_cut_card(self):
        """
        Test that a cut card is added to the deck
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_deck_creation(self):
        """
        Test that a deck can be created successfully
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_cards_in_deck_are_unique(self):
        """
        Test that the cards generated within a deck are unique
        """
        print("REPLACE WITH TEST")

class TestGame(unittest.TestCase):
    """
    Tests that cover gameplay
    """

    @unittest.skip
    def test_initial_deal(self):
        """
        Test that dealing works correctly
        """
        print("REPLACE WITH TEST")
    
    @unittest.skip
    def test_score_calculation(self):
        """
        Test that score is calculated correctly
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_stands_on_21(self):
        """
        Test that a user automatically stands when they hit 21
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_busts(self):
        """
        Test that a user's turn ends when they bust and that they also lose
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_dealer_stands_on_soft_17(self):
        """
        Test that a dealer always stands when they have a soft 17 (a 17 that could also be a 7 e.g. 6 + A or 3 + 3 + A)
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_wins_when_dealer_plays(self):
        """
        Test that a user wins when their score exceeds the dealer and the dealer doesn't bust
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_wins_when_dealer_busts(self):
        """
        Test that a user wins when the dealer exceeds 21 as long as they have not also bust themselves
        """
        print("REPLACE WITH TEST")
    
    @unittest.skip
    def test_user_loses(self):
        """
        Test that a user loses when the dealer's score exceeds theirs and the dealer doesn't bust
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_pushes(self):
        """
        Test that when a user's score and the dealer's score are the same they push
        """
        print("REPLACE WITH TEST")
    
    @unittest.skip
    def test_user_wins_with_blackjack(self):
        """
        Test that the user wins when they get blackjack and they get the custom message
        """
        print("REPLACE WITH TEST")

    @unittest.skip
    def test_user_pushes_with_blackjack(self):
        """
        Test that the user pushes with blackjack when the dealer also has a blackjack
        """
        print("REPLACE WITH TEST")

if __name__ == '__main__':
    unittest.main()
