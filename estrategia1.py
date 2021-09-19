import yfinance
import time

capital = 100000
insideMarket = False 

bitcoinsShort = 0
bitcoinsLarge = 0
stopLossLarge = 0
stopLossShort = 0
entrance = "none"

def enterMarket(prize,capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,insideMarket):
    bitcoinsShort = capital/prize/2
    bitcoinsLarge = capital/prize/2
    capital -= bitcoinsLarge*prize
    capital += bitcoinsShort*prize
    stopLossLarge = prize - 20
    stopLossShort = prize + 20
    insideMarket = True 
    return bitcoinsShort,bitcoinsLarge,capital,stopLossLarge,stopLossShort,insideMarket

def checkPrize(prize,capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,entrance,insideMarket):
    if prize <= stopLossLarge and entrance == "none":
        entrance = "short"
        capital += bitcoinsLarge*prize
        stopLossLarge = 0
    if prize >= stopLossShort and entrance == "none":
        entrance = "large"
        capital -= bitcoinsShort*prize
        stopLossShort = 99999999999
        
    if entrance == "large":
        if prize <= stopLossLarge:
            capital,entrance,insideMarket = outMarketLong(prize,capital,bitcoinsLarge,entrance,insideMarket)
        else:
            stopLossLarge = (stopLossLarge+prize)/2
    if entrance == "short":
        if prize >= stopLossShort:
            capital,entrance,insideMarket = outMarketShort(prize,capital,bitcoinsShort,entrance,insideMarket)
        else:
            stopLossShort = (stopLossShort+prize)/2

    return capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,entrance,insideMarket


def outMarketLong(prize,capital,bitcoins,entrance,insideMarket):
    capital += prize*bitcoins
    entrance = "none"
    insideMarket = False 
    return capital,entrance,insideMarket

def outMarketShort(prize,capital,bitcoins,entrance,insideMarket):
    capital -= prize*bitcoins
    entrance = "none"
    insideMarket = False 
    return capital,entrance,insideMarket

for i in range(600):
    data = yfinance.download(tickers="BTC-USD",period="1d",interval="1m")
    prize = data.iloc[0,3]
    
    if insideMarket == False:
        bitcoinsShort,bitcoinsLarge,capital,stopLossLarge,stopLossShort,insideMarket = enterMarket(prize,capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,insideMarket)
    else:
        capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,entrance,insideMarket = checkPrize(prize,capital,bitcoinsShort,bitcoinsLarge,stopLossLarge,stopLossShort,entrance,insideMarket)
        
    print("Precio: ",prize)
    print("Capital:",capital)
    print("Entrada:",entrance)















"""
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import yfinance

#start = dt.datetime(2015, 9, 11)
#end = dt.datetime(2021, 9, 11)
#df = web.DataReader('AAPL','yahoo',start,end)

data = yfinance.download(tickers="AAPL",period="10d",interval="1d")

data['price'] = data['Adj Close']

SMA13 = 13
SMA48 = 48
data['SMA13'] = data['price'].rolling(window=SMA13).mean()
data['SMA48'] = data['price'].rolling(window=SMA48).mean()

#data['SMA+STD'] = data['SMA'] + data['STD']
#data['SMA-STD'] = data['SMA'] - data['STD']

plt.style.use('seaborn')
data[['price','SMA13','SMA48']].plot(figsize=(10,6))
#data[['price','SMA+STD','SMA-STD']].plot(figsize=(10,6))

#data['position'] = np.where(data['SMA13'] > data['SMA48'],1,-1)
#data['position'] = np.where(data['price'] > data['SMA+STD'],-1,0)
#data['position'] = np.where(data['price'] < data['SMA-STD'],1,data['position'])

def determineMove(separation,tendency):
    if separation > 0 & separation < 0.003 & tendency == "alcist":
        return 1
    if separation < 0 & separation > -0.003 & tendency == "bearish":
        return -1
    return 0
    

data['separation'] = data['SMA13'] - data['SMA48']
data['tendency'] = np.where(data['SMA13'] > data['SMA48'],"alcist","bearish")
#data['position'] = np.where(determineMove(separation = data['separation'], tendency = data['tendency']),1,0)
#data['position'] = np.where(determineMove(data['separation'], data['tendency']),-1,data['position'])
data['position'] = determineMove(data['separation'],data['tendency'])
data['position'] = data['position'].fillna(0)

data['returns'] = data['price']/data['price'].shift(1)
data['strategy'] = data['returns'] ** data['position'].shift(1)
data[['returns','strategy']].dropna().cumprod().plot(figsize=(10,6))

"""
