from urllib.request import urlopen
from os import path
import json
import csv
from io import StringIO

def fetch_data(date):
    """
    Fetch data for the date (in dd-mm-yyyy format) from a Github repository.
    Index:			    0123456789
    """

    #URL builder
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master"
    url += "/csse_covid_19_data/csse_covid_19_daily_reports/"
    url += date[3:5] + "-" + date[:2] + "-" + date[6:] + ".csv"

    #Download CSV
    try:
	    downloaded_data = list(urlopen(url))
    except:
        print("[Fatal] No dataset found for {}".format(date))
        exit()

    downloaded_data = list(map(lambda a: str(a, "utf-8")[:-1], downloaded_data))

    return list(csv.reader(StringIO("\n".join(downloaded_data))))

def parse_data(date):
    """
    Return a dictionary of country and their respective Covid-19 statistics.
    Return format: Dictionary(country_name, List(confirmed, deaths, recovered, active))
    
    For countries with multiple entries (i.e US, Canada, Australia), their state
    and provincial entries will be merged under one single entry.
    """

    #Check if data set already exists
    filename = "".join(date.split("-")) + ".json"
    if path.isfile("../cache/" + filename):
        f = open("../cache/" + filename)
        data_set = json.load(f)	
        f.close()
        return data_set
    
    #Retrive data
    data = fetch_data(date)
    data.pop(0)		#Ignore first line
	
    # CSV format:
    # FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key
    # 
    # Use only: Country_Region(3), Confirmed(7), Deaths(8), Recovered(9), Active(10)
    #
    # For countries with multiple entries, merge them.

    #Process
    data_set = dict()
    for entry in data:
        country_name = entry[3]
        confirmed = int(entry[7])
        deaths = int(entry[8])
        recovered = int(entry[9])
        active = int(entry[10])

        if country_name in data_set.keys():
            data_set[country_name][0] += confirmed
            data_set[country_name][1] += deaths
            data_set[country_name][2] += recovered
            data_set[country_name][3] += active
        else:
            data_set[country_name] = [confirmed, deaths, recovered, active]
	
    #Save processed data for future use
    filename = "".join(date.split("-")) + ".json"
    f = open("../cache/" + filename, "w")
    f.write(json.dumps(data_set))
    f.close()

    #Return data set
    return data_set
