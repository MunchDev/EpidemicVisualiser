import csv_processor
import helper
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt

f = open("../cache/population.json")
population = json.load(f)
f.close()

def get_country_data(country, days, date):
    """
    Get data for <country> within the last <days> ago, from the <date>.
    Data is endexed so that the most recent entry is at the end of the list.
    Return format: List(date-days, date-days+1, ..., date-1, date)
    """
    
    entries = []
    for i in range(days-1, -1, -1):
        entries.append(csv_processor.parse_data(helper.modify_date(date, -i))[country])

    return entries

def country_tally_plot(country, date, timespan, scale, plot_type):
    data = get_country_data(country, timespan, date)
    confirmed = [x[0] for x in data]
    deaths = [x[1] for x in data]
    recovered = [x[2] for x in data]
    active = [x[3] for x in data]

    x_data = np.linspace(-(timespan-1), 0, num=timespan)
    confirmed = np.array(confirmed)
    deaths = np.array(deaths)
    recovered = np.array(recovered)
    active = np.array(active)

    plt.yscale(scale)

    if "c" in plot_type:
        plt.plot(x_data, confirmed, '.b-', label="Confirmed")
    if "r" in plot_type:
        plt.plot(x_data, recovered, '.g-', label="Recovered")
    if "d" in plot_type:
        plt.plot(x_data, deaths, '.k-', label="Deaths")
    if "a" in plot_type:
        plt.plot(x_data, active, '.r-', label="Active")

    plt.xlabel("Number of days since the latest report")
    plt.ylabel("Number of cases")
    plt.title("COVID-19 tally for " + country)
    plt.legend(loc="best")
    plt.show()
    return

def world_tally_plot(countries, colours, date, timespan, scale):
    plt.xlabel("Number of days since the latest report")
    plt.ylabel("Number of cases")
    plt.title("COVID-19 tallies over the world")
    plt.legend(loc="best")
    
    for country, colour in zip(countries, colours):
        data = get_country_data(country, timespan, date)
        confirmed = [x[0] for x in data]
        x_data = np.linspace(-(timespan-1), 0, num=timespan)
        confirmed = np.array(confirmed)
        
        plt.plot(x_data, confirmed, color=colour, marker=".", linestyle="-", label=country)
    
    plt.show()
    return
