from game_logic import player, dealer, decide_soft_score_print, check_stand, check_blackjack
from cards import shoe, shoe_check
from exceptions import tooManyPlayersError, zeroPlayersError, tooManyDecksError, zeroDecksError

def setup_game(num_players=1, num_decks=1):
    """
    Set up the game using the specified number of players and decks
    """
    players = []
    for i in range (num_players):
        players.append(player(i+1))
    new_dealer = dealer("Dealer")
    play_shoe = shoe(num_decks).shuffle_shoe()
    return players, new_dealer, play_shoe

def initial_deal(play_shoe, player_list, dealer):
    for player in player_list:
        player.new_game_reset()
    dealer.reset_dealer()
    for _ in range(2):
        for player in player_list:
            player.hit_hand(play_shoe)
        dealer.check_hide_card(play_shoe)

def dealer_play(play_shoe, dealer):
    """
    Logic for if the dealer should hit or stand based on their score
    """
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
    """
    Function that allows the user to play
    """
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
    """
    Function that checks if each user has more or less than the dealer and decides if they have
    won or lost then adds them to a list accordingly.
    """
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
    """
    Function that prints the results in a human readable format
    """
    winners = results[0]
    losers = results[1]
    pushers = results[2]
    blackjack_winners = results[3]
    print(generate_results_string(winners, " wins", " win"))
    print(generate_results_string(losers, " loses", " lose"))
    print(generate_results_string(pushers, " pushes", " push"))
    print(generate_results_string(blackjack_winners, " wins with blackjack", " win with blackjack"))

def generate_results_string(player_list, singular_result, plural_result):
    """
    Given a list and a singular and plural result string, function
    generates a string based on length of list containing each of the players in
    that list separated by a comma or & sign as relevant and the relevant result
    string. This is then returned.
    """
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
    """
    Logic for getting the number of players, including
    error handling
    """
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

def get_number_of_decks():
    """
    Logic for getting the number of decks that will
    be in the shoe, including error handling
    """
    number_of_decks = None
    while not(type(number_of_decks)) == int:
        try:
            number_of_decks = int(input("How many decks would you like in the shoe? "))
            if number_of_decks == 0:
                raise zeroDecksError
            elif number_of_decks > 6:
                raise tooManyDecksError
        except zeroDecksError:
            print("The game needs at least 1 player")
            number_of_decks = None
        except tooManyDecksError:
            print("Sorry you can't have more than 6 players")
            number_of_decks= None
        except:
            number_of_decks = None
    return number_of_decks

def play_again():
    """
    Logic for checking if a player wishes to play again
    """
    decision = " "
    while not(decision[0] == "y") and not(decision[0] == "n"):
        decision = input("Would you like to play again? ").lower()
    if decision[0]=="y":
        return True
    else:
        return False
    
def play_game(play_shoe, player_list, dealer, number_of_decks):
    """
    Function that calls all relevant functions for gameplay
    """
    # Check if the shoe is still valid (contains a cut card) if not,
    # create a new shoe
    play_shoe = shoe_check(play_shoe, number_of_decks)
    initial_deal(play_shoe, player_list, dealer)
    for player in player_list:
        user_play(play_shoe, player, dealer)
    dealer_play(play_shoe, dealer)
    display_results(check_results(player_list, dealer))
    if play_again():
        return True, play_shoe
    return False

def main():
    """
    MAIN function, called on file startup that handles
    game setup and if the player wishes to replay
    """
    number_of_players = get_number_of_players()
    number_of_decks = get_number_of_decks()
    game_data = setup_game(number_of_players)

    player_list = game_data[0]
    play_shoe = game_data[2]
    play_dealer = game_data[1]
    play_again = True

    while play_again:
        replay = play_game(play_shoe, player_list, play_dealer, number_of_decks)
        if replay:
            play_shoe = replay[1]
        else:
            play_again = False
    
    print("Thanks for playing")

if __name__ == '__main__':
    main()
