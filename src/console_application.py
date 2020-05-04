from data_miner import *
from helper import *

def main():
    welcome_options = [
        "Show country tally plot",
        "Show world tally plot",
        "Show statistics"
    ]
    option = welcome_screen_option(welcome_options)
    return 0

def welcome_screen_option(options):
    i = None
    while True:
        clear()
        print("Welcome to Epidemic Simulator -- Console version")
        print("What do you like to do? (-1 to exit)\n")
        for i, option in zip(range(len(options)), options):
            print("({0}) {1}".format(i + 1, option))
        i = input("Your option > ")
        if i == "-1":
            exit(0)
        if i.isdigit() and 0 < int(i) <= len(options):
            i = int(i)
            break
    clear()
    return i - 1
    
if __name__ == "__main__":
    main()
