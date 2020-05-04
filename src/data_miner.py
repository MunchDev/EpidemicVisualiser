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
        data = csv_processor.parse_data(helper.modify_date(date, -i)).get(country, None)
        if data == None:   
            return -1
        entries.append(data)
    return entries

def country_tally_plot(country, date, *args, **kwargs):
    # Check whether provided a single country or a list of countries
    multiple_countries = False
    if type(country) != str:
        if type(country) == list:
            multiple_countries = True
        else:
            print("Invalid input")
            return -1 
    #-----------------------------------------------------------------------------
    #---------------------Get/validate positional arguments-----------------------
    #-----------------------------------------------------------------------------
    if type(date) != str:
        print("Expected type of date is <class \"str\", but given ", type(date))
    if not helper.is_valid_date(date):
        print("Expected format for date is 'dd-mm-yyyy', but given ", type(date))
        return -1
    #-----------------------------------------------------------------------------
    
    # If a single country is provided    
    if not multiple_countries:
        #----------------------------------------------------------------
        #-----------------Get/validate keyword arguments-----------------
        #----------------------------------------------------------------
        timespan = kwargs.get("timespan", 30)
        if timespan == None:
            timespan == 30
        if timespan <= 0:
            print("Invalid timespan! Timespan must be positive") 
            return -1                                            
        
        scale = kwargs.get("scale", "log")
        if scale == None:
            scale = "log"
        if scale != "log" and scale != "linear":
            print("Invalid scale")
            return -1
            
        plot_type = kwargs.get("plot_type", "cdra")
        if plot_type == None:
            scale = "cdra"
        #----------------------------------------------------------------
        
        #---------------------------------------------------------------
        #-----------------Data retrieval and processing-----------------
        #---------------------------------------------------------------
        data = get_country_data(country, timespan, date)
        if data == -1:
            print("'{}' is unavailable!".format(country))
            return -1
 
        confirmed = [x[0] for x in data]  
        deaths = [x[1] for x in data]
        recovered = [x[2] for x in data]
        active = [x[3] for x in data]

        x_data = np.linspace(-(timespan-1), 0, num=timespan)
        confirmed = np.array(confirmed)
        deaths = np.array(deaths)
        recovered = np.array(recovered)
        active = np.array(active)
        #---------------------------------------------------------------
        
        #----------------------------------------------------------------
        #----------------------------Plotting----------------------------
        #----------------------------------------------------------------
        plot_enabled = False
        if "c" in plot_type:
            plt.plot(x_data, confirmed, '.b-', label="Confirmed")
            plot_enabled = True
        if "r" in plot_type:
            plt.plot(x_data, recovered, '.g-', label="Recovered")
            plot_enabled = True
        if "d" in plot_type:
            plt.plot(x_data, deaths, '.k-', label="Deaths")
            plot_enabled = True
        if "a" in plot_type:
            plt.plot(x_data, active, '.r-', label="Active")
            plot_enabled = True  
        if not plot_enabled:
            print("No valid plot type is provided")
            return -1
        
        plt.yscale(scale)
        plt.xlabel("Number of days since the latest report")
        plt.ylabel("Number of cases")
        plt.title("COVID-19 tally for " + country)
        plt.legend(loc="best")
        plt.show()
        #----------------------------------------------------------------    
        return 0
    else:
        n = len(country)
        timespan = kwargs.get("timespan", 30)
        
        scale = kwargs.get("scale", ["log"] * n)
        if type(scale) != list:
            print("Expected type of scale is <class \"list\">, but given ", type(scale))
            return -1
        if len(scale) < n:
            scale += [None] * (n - len(scale))
            
        plot_type = kwargs.get("plot_type", ["cdra"] * n)      
        if type(plot_type) != list:
            print("Expected type of scale is <class \"list\">, but given ", type(scale))
            return -1
        if len(plot_type) < n:
            plot_type += [None] * (n - len(scale))
            
        for _country in country:
            country_tally_plot(_country, date, timespan, scale, plot_type)
        return 0

def world_tally_plot(countries, colours, date, timespan = 30, scale = "log", plot_type = "c"):
    if type(countries) != list or type(colours) != list or type(date) != str or type(timespan) != int:
        print("Invalid input type")
        return -1
    
    if scale != "log" and scale != "linear":
        print("Invalid scale")
        return -1
    plt.yscale(scale)
    
    chosen_option = None
    options = {"c" : 0, "d" : 1, "r" : 2, "a" : 3}
    for letter in plot_type:
        if letter in options.keys():
            chosen_option = options[letter]
            break          
    if chosen_option == None:
        print("Invalid plot type")
        return -1
    
    if not helper.is_valid_date(date):
        print("Invalid date")
        return -1
    if timespan <= 0:
        print("Invalid timespan! Timespan must be positive")
        return -1
    for country, colour in zip(countries, colours):
        data = get_country_data(country, timespan, date)
        if data == -1:
            print("'{}' is unavailable!".format(country))
            return -1
        
        cases = [x[chosen_option] for x in data]
        x_data = np.linspace(-(timespan-1), 0, num=timespan)
        cases = np.array(cases)
        
        plt.plot(x_data, cases, color=colour, marker=".", linestyle="-", label=country)
    
    ylabel = "Number of "
    if chosen_option == 0:
        ylabel += "confirmed cases"
    elif chosen_option == 1:
        ylabel += "deaths"
    elif chosen_option == 2:
        ylabel += "recovered cases"
    else:
        ylabel += "active cases"
    
    plt.xlabel("Number of days since the latest report")
    plt.ylabel(ylabel)
    plt.title("COVID-19 tallies over the world")
    plt.legend(loc="best")
    plt.show()
    return 0
