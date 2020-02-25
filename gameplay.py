from game_logic import player, dealer, decide_soft_score_print, check_stand, check_blackjack
from cards import shoe

def setup_game(num_players=1, num_decks=1):
    players = []
    for _ in range (num_players):
        players.append(player())
    new_dealer = dealer()
    play_shoe = shoe(num_decks).shuffle_shoe()
    return players, new_dealer, play_shoe

def initial_deal(play_shoe, player_list, dealer):
    for _ in range(2):
        for player in player_list:
            player.hit_hand(play_shoe)
        dealer.check_hide_card(play_shoe)

def dealer_play(play_shoe, dealer):
    dealer.reveal_hidden_card()
    print("Dealer shows " + dealer.get_hidden_card_only().get_card_details())
    print("Dealer's hand " + dealer.get_viewable_hand())
    decide_soft_score_print(dealer)
    if dealer.get_score() < 17:
        hit = True
        while hit:
            print("Dealer hits")
            dealer.hit_hand(play_shoe)
            print("Dealer's hand " + dealer.get_viewable_hand())
            decide_soft_score_print(dealer)
            hit = dealer.check_hit(play_shoe)
    check_stand(dealer)

def user_play(play_shoe, player):
    hit = True
    while hit == True:
        print("Your hand is " + str(player.get_viewable_hand()))
        decide_soft_score_print(player)
        if not(check_blackjack(player.get_score(), player.get_hand())):
            if not(player.check_bust()):
                decision = input("Would you like to Hit or Stand? ").lower()
                if decision[0]=="h":
                    player.hit_hand(play_shoe)
                else:
                    hit = False
    check_stand(player)

game_data = setup_game()

player_list = game_data[0]
play_shoe = game_data[2]
play_dealer = game_data[1]

initial_deal(play_shoe, player_list, play_dealer)
for player in player_list:
    user_play(play_shoe, player)
dealer_play(play_shoe, play_dealer)
