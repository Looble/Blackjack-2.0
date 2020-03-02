from game_logic import player, dealer, decide_soft_score_print, check_stand, check_blackjack
from cards import shoe
from exceptions import tooManyPlayersError, zeroPlayersError

def setup_game(num_players=1, num_decks=1):
    players = []
    for i in range (num_players):
        players.append(player(i+1))
    new_dealer = dealer("Dealer")
    play_shoe = shoe(num_decks).shuffle_shoe()
    return players, new_dealer, play_shoe

def initial_deal(play_shoe, player_list, dealer):
    for _ in range(2):
        for player in player_list:
            player.hit_hand(play_shoe)
        dealer.check_hide_card(play_shoe)

def dealer_play(play_shoe, dealer):
    dealer.reveal_hidden_card()
    print("Now for the dealer")
    print("Dealer reveals: " + dealer.get_hidden_card_only().get_card_details())
    print("Dealer's hand:" + dealer.get_viewable_hand())
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

def user_play(play_shoe, player, dealer):
    print("\nDealer shows:" + dealer.get_viewable_hand())
    hit = True
    while hit == True:
        decision = " "
        if len(player.get_hand()) == 2:
            print("\nPlayer " + player.get_name() + " your hand is:" + player.get_viewable_hand())
        else:
            print("\nYour hand is now:" + str(player.get_viewable_hand()))
        decide_soft_score_print(player)
        if not(check_blackjack(player.get_score(), player.get_hand())):
            if not(player.check_bust()) and player.get_score() < 21:
                while not(decision[0] == "h") and not(decision[0] == "s"):
                    decision = input("Would you like to Hit or Stand? ").lower()
                if decision[0]=="h":
                    player.hit_hand(play_shoe)
                else:
                    hit = False
            else:
                hit = False
        else:
            hit = False
    check_stand(player)

def check_results(player_list, dealer):
    dealer_score = dealer.get_score()
    dealer_hand = dealer.get_hand()
    blackjack_winners = []
    winners = []
    losers = []
    pushers = []
    dealer_plays = True
    if dealer_score > 21:
        dealer_plays = False
    for player in player_list:
        player_score = player.get_score()
        player_hand = player.get_hand()
        if dealer_plays and check_blackjack(dealer_score, dealer_hand):
            if check_blackjack(player_score, player_hand):
                pushers.append(player)
            else:
                losers.append(player)
        elif dealer_plays:
            if player_score > dealer_score and not(player.check_bust()):
                if check_blackjack(player_score, player_hand):
                    blackjack_winners.append(player)
                else:
                    winners.append(player)
            elif player_score == dealer_score:
                pushers.append(player)
            else:
                losers.append(player)
        else:
            if check_blackjack(player_score, player.get_hand()):
                blackjack_winners.append(player)
                break
            elif player_score <= 21:
                winners.append(player)
            else:
                losers.append(player)
    return winners, losers, pushers, blackjack_winners

def display_results(results):
    winners = results[0]
    losers = results[1]
    pushers = results[2]
    blackjack_winners = results[3]
    print(generate_results_string(winners, " wins", " win"))
    print(generate_results_string(losers, " loses", " lose"))
    print(generate_results_string(pushers, " pushes", " push"))
    print(generate_results_string(blackjack_winners, " wins with blackjack", " win with blackjack"))

def generate_results_string(player_list, singular_result, plural_result):
    string = ""
    plural = len(player_list) > 1
    player_number = 1
    if len(player_list) != 0:
        string += "Player "
        for player in player_list:
            string += player.get_name()
            if player_number < len(player_list) - 1:
                string += ", "
            elif player_number < len(player_list):
                string += " & "
            player_number += 1
        if plural:
            string = string[:6] + "s" + string[6:] + plural_result
        else:
            string += singular_result
    return string

def get_number_of_players():
    number_of_players = None
    while not(type(number_of_players)) == int:
        try:
            number_of_players = int(input("How many players are there? "))
            if number_of_players == 0:
                raise zeroPlayersError
            elif number_of_players > 6:
                raise tooManyPlayersError
        except zeroPlayersError:
            print("The game needs at least 1 player")
            number_of_players = None
        except tooManyPlayersError:
            print("Sorry you can't have more than 6 players")
            number_of_players = None
        except:
            number_of_players = None
    return number_of_players

def main():
    number_of_players = get_number_of_players()
    game_data = setup_game(number_of_players)

    player_list = game_data[0]
    play_shoe = game_data[2]
    play_dealer = game_data[1]

    initial_deal(play_shoe, player_list, play_dealer)
    for player in player_list:
        user_play(play_shoe, player, play_dealer)
    dealer_play(play_shoe, play_dealer)
    display_results(check_results(player_list, play_dealer))

if __name__ == '__main__':
    main()
