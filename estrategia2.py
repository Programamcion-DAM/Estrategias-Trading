#Estrategia de reversión a la media con media 50
import yfinance

data = yfinance.download(tickers="TSLA",period="1mo",interval="5m")

data['EMA50'] = data['Close'].rolling(100).mean()

capital = 100000
shares = 0
position = "none"

def openLong(prize,capital):
    shares = capital/prize
    capital = 0
    return shares,capital,"long"

def openShort(prize,capital):
    shares = capital/prize 
    capital += shares*prize
    return shares,capital,"short"

i = 50

while True:
    prize = data.iloc[i,3]
    EMA50 = data.iloc[i,6]
    if position == "none":
        if prize > EMA50:
            shares,capital,position = openLong(prize, capital)
        else:
            shares,capital,position = openShort(prize, capital)
    else:
        if prize < EMA50 and position == "long":
            capital += prize*shares
            position = "none"
            shares = 0
        if prize > EMA50 and position == "short":
            capital -= prize*shares
            position = "none"
            shares = 0
    
    if i > 576 and position == "none":
        break
    else:
        i += 1
    
        
print('Capital: ',capital)
print('Position: ',position)


        
        
        
        
        
        
        
        
        
        
        
        
