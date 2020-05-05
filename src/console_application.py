from data_miner import plot_tally
from helper import clear
from helper import print_error as stderr
from json import load

population = None
try:
    with open("../cache/population.json") as f:
        population = json.load(f)
    if population == None or len(population) == 0:
        stderr("Unable to load population! Aborting...")
        input("Press Enter to continue...")
        raise RuntimeError("Unable to load population!")
except:
    exit(-1)
        
def main():
    welcome_options = [
        "Show country tally plot",
        "Show world tally plot"
    ]
    option = welcome_screen_option(welcome_options)
    return 0

def ct_plot():
    def get_ct():
        countries = []
        flag = False
        while True:
            clear()
            print("Step 1: Choose the countries you want to plot")
            # TODO: Add instruction here, same as in the notebooks.
            print("Leave empty to proceed to Step 2.\n")
            if flag:
                print("Country name is invalid! Try again.\n")
            ct = input("Enter country name > ")
            flag = False
            if ct == "":
                if len(countries) == 0:
                    clear()
                    print("You did not enter any valid country! Please enter at least one.")
                    input("Press Enter to go back to try again")
                else:
                    clear()
                    break
            elif ct not in population.keys():
                flag = True
            else:
                countries.append(ct)
        clear()
        return countries    

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
