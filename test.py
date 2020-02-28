import unittest

from cards import card, deck, shoe
from game_logic import dealer, player
from gameplay import initial_deal, dealer_play, user_play, setup_game, check_blackjack, check_stand, decide_soft_score_print,\
    check_results
from unittest import mock


class TestCard(unittest.TestCase):
    """
    Tests that cover the card class
    """
    def test_card_creation(self):
        """
        Test that cards can be created successfully and that values are correct for Aces, numbers
        and pictures (king, queen, jack)
        """
        self.assertEqual(card(1, "H").get_card_details(), "AH")
        self.assertEqual(card(4, "H").get_card_details(), "4H")
        self.assertEqual(card(11, "H").get_card_details(), "JH")
        self.assertEqual(card(12, "H").get_card_details(), "QH")
        self.assertEqual(card(13, "H").get_card_details(), "KH")

    def test_picture_card_score_calculation(self):
        """
        Test that picture cards (King, Queen, Jack) all return a score of 10
        """
        self.assertEqual(card(11, "H").get_score(), 10)
        self.assertEqual(card(12, "H").get_score(), 10)
        self.assertEqual(card(13, "H").get_score(), 10)


class TestShoe(unittest.TestCase):
    """
    Tests that cover the deck class
    """

    def test_shoe_creation(self):
        """
        Test that the shoe is created with the correct number of cards
        """
        number_of_decks = 2
        self.assertEqual(
            len(shoe(number_of_decks).shuffle_shoe().get_list_of_card_values()), (number_of_decks*52) + 1)

    def test_cut_card(self):
        """
        Test that a cut card is added to the deck
        """
        self.assertEqual(card("cut").get_card_details(), "cutcut")

    def test_draw_card(self):
        """
        Test that a card is drawn correctly and that it is removed from the shoe
        """
        test_shoe = shoe(1)
        self.assertEqual((test_shoe.get_first_card()).get_card_details(), "AH")
        self.assertEqual(len(test_shoe.get_list_of_card_values()), 51)


class TestDeck(unittest.TestCase):
    def test_deck_creation(self):
        """
        Test that a deck of the correct length can be created successfully
        """
        self.assertEqual(len(deck().get_all_card_objects()), 52)

    def test_cards_in_deck_are_unique(self):
        """
        Test that the cards generated within a deck are unique
        """
        self.assertEqual(len(set(deck().get_all_card_objects())), 52)


class TestGame(unittest.TestCase):
    """
    Tests that cover gameplay
    """
    def setUp(self):
        self.test_shoe = shoe(1)
        self.dealer = dealer()
        self.test_player_list = [player()]

    def test_game_setup(self):
        """
        Test that the initial game setup works correctly
        """
        game_data = setup_game()
        players = game_data[0]
        play_shoe = game_data[2]
        self.assertEqual(len(players), 1)
        self.assertEqual(len(play_shoe.get_list_of_card_values()), 53)

    def test_initial_deal(self):
        """
        Test that dealing works correctly
        """
        player_list = self.test_player_list
        dealer = self.dealer
        shoe = self.test_shoe
        initial_deal(shoe, player_list, dealer)
        self.assertEqual(len(player_list[0].get_hand()), 2)
        self.assertTrue(dealer.get_hidden_card_only())
        self.assertEqual(len(dealer.get_hand()), 1)


    def test_score_calculation(self):
        """
        Test that score is calculated correctly both for the initial deal and
        in cases of soft scores
        """
        test_shoe = self.test_shoe
        dealer = self.dealer
        player_list = self.test_player_list
        player = player_list[0]

        initial_deal(test_shoe, player_list, dealer)
        self.assertEqual(player.get_score(), 14)
        self.assertEqual(dealer.get_hidden_card_only().get_score() + dealer.get_score(), 6)
        player.hit_hand(test_shoe)
        self.assertEqual(player.get_score(), 19)
        self.assertTrue(player.soft_score_check())
        player.hit_hand(test_shoe)
        self.assertEqual(player.get_score(), 15)
        self.assertFalse(player.soft_score_check())
        dealer.reveal_hidden_card()
        self.assertFalse(dealer.soft_score_check())

   
    def test_user_stands_with_blackjack(self):
        """
        Test that a user automatically stands when they have blackjack
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(10, "H"))
        test_shoe.cards.insert(2, card(1, "H"))
        initial_deal(test_shoe, player_list, dealer)
        self.assertEqual(player.get_score(), 21)
        self.assertTrue(check_blackjack(player.get_score(), player.get_hand()))

    def test_user_stands_on_21(self):
        """
        Test that a user automatically stands when they hit 21
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(10, "H"))
        test_shoe.cards.insert(2, card(3, "H"))
        test_shoe.cards.insert(4, card(8, "D"))
        initial_deal(test_shoe, player_list, dealer)
        with mock.patch('builtins.input', return_value="hit"):
            user_play(test_shoe, player, dealer)
        self.assertEqual(player.get_score(), 21)
        self.assertFalse(check_blackjack(player.get_score(), player.get_hand()))

    def test_user_busts(self):
        """
        Test that a user's turn ends when they bust and that they also lose
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(10, "H"))
        test_shoe.cards.insert(2, card(3, "H"))
        test_shoe.cards.insert(4, card(10, "D"))
        initial_deal(test_shoe, player_list, dealer)
        with mock.patch('builtins.input', return_value="hit"):
            user_play(test_shoe, player, dealer)
        self.assertTrue(player.check_bust)

    def test_dealer_stands_on_soft_17(self):
        """
        Test that a dealer always stands when they have a soft 17 (a 17 that could also be a 7 e.g. 6 + A or 3 + 3 + A)
        """
        dealer = self.dealer
        test_shoe = self.test_shoe
        test_shoe.cards.insert(0, card(1, "S"))
        test_shoe.cards.insert(3, card(3, "S"))
        player_list = self.test_player_list
        initial_deal(test_shoe, player_list, dealer)
        self.assertTrue(dealer.soft_score_check())
        self.assertFalse(dealer_play(test_shoe, dealer))
        self.assertEqual(dealer.get_score(), 17)

    def test_user_wins_when_dealer_plays(self):
        """
        Test that a user wins when their score exceeds the dealer and the dealer doesn't bust
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(8, "H"))
        test_shoe.cards.insert(1, card(10, "C"))
        test_shoe.cards.insert(2, card(10, "C"))
        test_shoe.cards.insert(3, card(6, "D"))
        initial_deal(test_shoe, player_list, dealer)
        dealer_play(test_shoe, dealer)
        self.assertFalse(dealer.check_bust())
        self.assertFalse(check_blackjack(player.get_score(), player.get_hand()))
        results = check_results(player_list, dealer)
        winners = results[0]
        self.assertIn(player, winners)


    def test_user_wins_when_dealer_busts(self):
        """
        Test that a user wins when the dealer exceeds 21 as long as they have not also bust themselves
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(8, "H"))
        test_shoe.cards.insert(1, card(10, "C"))
        test_shoe.cards.insert(2, card(8, "C"))
        test_shoe.cards.insert(3, card(6, "D"))
        test_shoe.cards.insert(4, card(10, "D"))
        initial_deal(test_shoe, player_list, dealer)
        dealer_play(test_shoe, dealer)
        self.assertTrue(dealer.check_bust())
        self.assertFalse(check_blackjack(player.get_score(), player.get_hand()))
        results = check_results(player_list, dealer)
        winners = results[0]
        self.assertIn(player, winners)

    def test_user_loses(self):
        """
        Test that a user loses when the dealer's score exceeds theirs and the dealer doesn't bust
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(8, "H"))
        test_shoe.cards.insert(1, card(10, "C"))
        test_shoe.cards.insert(2, card(8, "C"))
        test_shoe.cards.insert(3, card(6, "D"))
        initial_deal(test_shoe, player_list, dealer)
        dealer_play(test_shoe, dealer)
        self.assertLess(player.get_score(), dealer.get_score())
        self.assertFalse(check_blackjack(player.get_score(), player.get_hand()))
        results = check_results(player_list, dealer)
        losers = results[1]
        self.assertIn(player, losers)
    
    def test_user_pushes(self):
        """
        Test that when a user's score and the dealer's score are the same they push
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(8, "H"))
        test_shoe.cards.insert(1, card(10, "C"))
        test_shoe.cards.insert(2, card(9, "C"))
        test_shoe.cards.insert(3, card(6, "D"))
        initial_deal(test_shoe, player_list, dealer)
        dealer_play(test_shoe, dealer)
        self.assertEqual(player.get_score(), dealer.get_score())
        self.assertFalse(check_blackjack(player.get_score(), player.get_hand()))
        results = check_results(player_list, dealer)
        pushers = results[2]
        self.assertIn(player, pushers)

    def test_user_wins_with_blackjack(self):
        """
        Test that the user wins when they get blackjack and they get the custom message
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(10, "H"))
        test_shoe.cards.insert(2, card(1, "H"))
        initial_deal(test_shoe, player_list, dealer)
        self.assertEqual(player.get_score(), 21)
        self.assertTrue(check_blackjack(player.get_score(), player.get_hand()))
        dealer_play(test_shoe, dealer)
        results = check_results(player_list, dealer)
        blackjack_winners = results[3]
        self.assertIn(player, blackjack_winners)


    def test_user_pushes_with_blackjack(self):
        """
        Test that the user pushes with blackjack when the dealer also has a blackjack
        """
        test_shoe = self.test_shoe
        player_list = self.test_player_list
        dealer = self.dealer
        player = player_list[0]
        test_shoe.cards.insert(0, card(10, "H"))
        test_shoe.cards.insert(1, card(10, "C"))
        test_shoe.cards.insert(2, card(1, "H"))
        initial_deal(test_shoe, player_list, dealer)
        self.assertEqual(player.get_score(), 21)
        dealer_play(test_shoe, dealer)
        self.assertTrue(check_blackjack(dealer.get_score(), dealer.get_hand()))
        self.assertTrue(check_blackjack(player.get_score(), player.get_hand()))
        results = check_results(player_list, dealer)
        pushers = results[2]
        self.assertIn(player, pushers)


if __name__ == '__main__':
    unittest.main()
