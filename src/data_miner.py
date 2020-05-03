import csv_processor
import helper
import datetime
import json

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

def nowI(gamma, beta, preS, preI):
    return (math.sqrt((1+gamma-beta*(preS+preI))**2+4*beta*(1+gamma)*preI)-(1+gamma-beta*(preS+preI)))/(2*beta*(1+gamma))

def nowS(preS, beta, _nowI):
    return preS/(1+beta*_nowI)

def nowR(preR, gamma, _nowI):
    return preR+gamma*_nowI

def train(country, date):
    """
    Find gamma and beta of a country, given data from the past 31 days.
    """
    data = get_country_data(country, 31, date)
    pop = population[country]

    #Calculate beta and gamma
    beta = gamma = 0
    for i in range(1, len(data)):
        deltaS = (pop-data[i][0])-(pop-data[i-1][0])
        deltaI = data[i][3]-data[i-1][3]
        nowS = pop-data[i][0]
        nowI = data[i][3]

        
        nowBeta = -deltaS/(nowS*nowI)
        nowGamma = (nowBeta*nowS*nowI-deltaI)/nowI

        beta += nowBeta
        gamma += nowGamma

    beta /= 30
    gamma /= 30
    return [beta, gamma]

def predict(country, date):
    """
    Generate a hypethetical scenerio of the epidemic, from the date onwards.
    """
    beta, gamma = train(country, helper.modify_date(date, -1))
    

