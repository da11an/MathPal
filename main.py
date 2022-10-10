import random
import time

# list of trusted people
people = ['holly', 'madison', 'dallan', 'carrie', 'hannah', 'evangeline', 'phoenix', 'caleb', 'leah', 'kambria', 'kinsley']

# list of secrets
secret_list = [
    "Hannah's birthday is August 28",
    "Leah's birthday is January 16",
    "we like to say weird words",
    "we like to call Daddy Doodleluxadisiousiousiousiousious",
    "our mother is pregnant with a boy"]


def secrets():

    # what is your name
    player = input("what is your name? ")
    
    # check if name is in list
    if player.lower() in people:
        time.sleep(0.5)
        print("You are in our special list, we have a secret for you!")
        time.sleep(0.5)
        print(random.choice(secret_list))
        time.sleep(5)
        player_secret = input("If you would like to hear another secret, type in a secret, otherwise just press Enter to quit: ")
        if len(player_secret.split()) >= 3:
            print("That sounds like a secret, here is one of ours:")
            print(random.choice(secret_list))
        else:
            print("That's okay. Come back and play again later")
    else:
        print("Sorry we can't help you.")
    # if name is in list tell a secret

    # else say sorry we can't help you


