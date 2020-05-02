import csv_processor
import helper
import datetime

def get_country_data(country, days, date):
    """
    Get data for <country> within the last <days> ago, from the <date>.
    Data is endexed so that the most recent entry is at the end of the list.
    Return format: List(date-days, date-days+1, ..., date-1, date)
    """
    
    entries = []
    for i in range(days, -1, -1):
        entries.append(csv_processor.parse_data(helper.modify_date(date, -i))[country])

    return entries

def nowI(gamma, beta, preS, preI):
    return (math.sqrt((1+gamma-beta*(preS+preI))**2+4*beta*(1+gamma)*preI)-(1+gamma-beta*(preS+preI)))/(2*beta*(1+gamma))

def nowS(preS, beta, _nowI):
    return preS/(1+beta*_nowI)

def nowR(preR, gamma, _nowI):
    return preR+gamma*_nowI

def nowBetaFromData(deltaS, _nowS, _nowI):
    return -deltaS/(_nowS*_nowI)

def nowGammaFromData(nowBeta, _nowS, _nowI, deltaI):
    return (nowBeta*_nowS*_nowI-deltaI)/_nowI

def train(country, date):
    """
    Find gamma and beta of a country, given data from the past 30 days.
    """
    data = get_country_data(country, 30, date)
    
