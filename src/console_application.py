from data_miner import plot_tally
from helper import clear, is_valid_date
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

def ct_plot(t=False):
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
                    input("Press Enter to go back and try again")
                else:
                    break
            elif ct not in population.keys():
                flag = True
            else:
                countries.append(ct)
        clear()
        return countries
    def get_date():
        date = None
        flag = False
        while True:
            clear()
            print("Step 2: Choose a date")
            # TODO: Add instruction here, same as in the notebooks.
            if flag:
                print("\nDate is invalid! Try again.\n")
            date = input("Enter date > ")
            if is_valid_date(date):
                break
            else:
                flag = True
        return date
    def get_ts():
        ts = None
        flag = False
        while True:
            clear()
            print("Step 3: Choose a suitable timespan")
            # TODO: Add instruction here, same as in the notebooks.
            if flag:
                print("\nTimespan is invalid! Try again.\n")
            date = input("Enter timespan > ")
            if ts.isdigit():
                ts = int(ts)
                if 0 < ts < 0x7fffffff:
                    break
            flag = True
        return ts
    def get_scale():
        scale = []
        flag = False
        while True:
            clear()
            print("Step 4: Choose the scale you will be using")
            # TODO: Add instruction here, same as in the notebooks.
            print("Leave empty to proceed to Step 5.\n")
            if flag:
                print("Scale is invalid! Try again.\n")
            s = input("Enter scale name ('log' or 'linear') > ")
            flag = False
            if s == "":
                if len(scale) == 0:
                    clear()
                    print("You did not enter any valid scale! Please enter at least one.")
                    input("Press Enter to go back and try again")
                if len(scale) == 1:
                    scale = scale[0]
                    break
                else:
                    break
            elif s != "log" and s != "linear":
                flag = True
            else:
                scale.append(s)
        clear()
        return scale
    def get_pltype():
        pltype = []
        flag = False
        while True:
            clear()
            print("Step 5: Choose the plot type(s) you will be using")
            # TODO: Add instruction here, same as in the notebooks.
            print("Leave empty to proceed to finish.\n")
            if flag:
                print("Plot type is invalid! Try again.\n")
            p = input("Enter plot type > ")
            flag = False
            if p == "":
                if len(pltype) == 0:
                    clear()
                    print("You did not enter any valid plot type! Please enter at least one.")
                    input("Press Enter to go back and try again")
                if len(pltype) == 1:
                    pltype = pltype[0]
                    break
                else:
                    break
            elif ("c" not in p) and ("d" not in p) and ("r" not in p) and ("a" not in p):
                flag = True
            else:
                pltype.append(p)
        clear()
        return pltype
    data = {"c":get_ct(), "d":get_date(), "t":get_ts(), "s":get_scale(), "p":get_pltype()}
    opt = "invalid"
    while opt == "invalid:
        p = input("Do you want to change (c)ountries, (t)imespan, (s)cale, (p)lot type or are you (o)kay? > ").lower()
        opt = {"c":get_ct, "d":get_date, "t":get_ts, "s":get_scale, "p":get_pltype}.get(p, "invalid")
        if p == "o":
            break
        if type(opt) != str:
            data[p] = opt()
    plot_tally(data["c"], data["d"], data["t"], scale=data["s"], plot_type=data["p"], transpose=t)
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
