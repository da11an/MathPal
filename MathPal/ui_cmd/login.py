
import time
from .utils import clear_screen, let_user_pick, let_user_pick, duration_str
from ..data import read_log, add_player


def login(filename):

    clear_screen()
    print("WELCOME to MATH GAMES! I'm Math Pal.\n\nWho are you?\n")
    
    player_log = read_log(filename)
    player_list = list(player_log.keys())
    if type(player_list) != list:
        player_list = [player_list]

    player = let_user_pick(options = ["Add me, I'm new"] + player_list)

    clear_screen()
    if player == "Add me, I'm new":
        player = add_player_dialog(filename)
        session = 1
    else: # player stats!!!     
        print("")
        print(f'Welcome back {player}!')
        if player_log[player]['session']:
            session = player_log[player]['session'][-1] + 1
            last_seen = duration_str(time.time() - player_log[player]['timestamp'][-1])
        else:
            session = 1
            last_seen = "forever"
        print(f'It has been {last_seen} since you played.')
        print("")
        time.sleep(1)

    return player, session

def add_player_dialog(filename):
    player = input("What's your name: ")
    if len(player) > 2:
        add_player(player, filename)
        session = 1
    else:
        print("Please choose a name with at least 3 characters.")
        player = add_player_dialog()
    return player

