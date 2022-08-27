import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import openpyxl
from collections import Counter
    
def lng_signal(rsi, stochslowk, price):
    l_signal = []
    signals = []
    fdate = []
    for date,value in rsi.iteritems():
        fdate.append(date)
        if value > 48 and stochslowk[date] < 30:
            l_signal.append(price[date])
            signals.append(date)
        else:
            l_signal.append(np.nan)
    return l_signal, signals, fdate


def shrt_signal(rsi, stochslowk, price):
    s_signal = []

    for date,value in rsi.iteritems():
        if value < 48 and stochslowk[date] > 70:
            s_signal.append(price[date])
            signals.append(date)
        else:
            s_signal.append(np.nan)
    return s_signal, signals
    
def isgood_signal(rsi, stoch, price, high, low, macd, histogram, signal):


    standard = 0
    n = -1
    contract = 0
    money = 50000
    moneytwo = 50000
    pnl = 0
    leverage = 2
    in_long_position = False
    in_short_position = False
    for date in fdate:
        param = macd[date]/histogram[date]

        params = histogram[date]/macd[date]
        
        sparam = histogram[date]/signal[date]

        sparams = macd[date]/signal[date]
        
        
        if #strategy goes here 
            n += 1

        elif #strategy goes here 
            n += 1

        if #strategy goes here  and in_long_position == False and in_short_position == False and date == signals[n]:
            if param > 10 or params > 2 or params < -2 or sparam < -.65 or sparams > 2 or sparams < .3:
                pass

            else:
            
                standard = float(price[date])
                newstandard = float(price[date])
                money += money * -0.00075
                contract = int((money * .9)/standard) * leverage
                in_long_position = True
                entryprice = price[date]
    

        elif #strategy goes here  and in_short_position == False and in_long_position == False and date == signals[n]:
            if param > 10 or params > 2 or params < -2 or sparam < -.65 or sparams > 2 or sparams < .3:
                pass
            
            else:
                standard = float(price[date])
                newstandard = float(price[date])
                money += money * -0.00075
                contract = int((money * .9)/standard) * leverage
                in_short_position = True
                entryprice = price[date]



        if in_short_position == True:
            for x in range(round(float(low[date]) * 1000), round(float(high[date]) * 1000)): # checking if stop loss is activated on given day
                if (newstandard * 1030) <= x:
                    in_short_position = False 
                    money += (standard - (newstandard * 1.03)) * contract
                    money += money * -0.00075
                    pnl += (entryprice - (newstandard *1.03))/entryprice
                    moneytwo = money
                    


                    break

            
            if in_short_position == True and newstandard > low[date]:
                newstandard = float(low[date])


        
        
        elif in_long_position == True:

            if (newstandard * .03) <= (newstandard - low[date]):
                in_long_position = False
                money += ((newstandard * .97) - standard) * contract
                money += money * -0.00075
                pnl += ((newstandard * .97) - entryprice)/ entryprice
                moneytwo = money


            elif (newstandard * .03) >= (newstandard - low[date]):
                newstandard = float(high[date])

                
        
    profit = money - 50000
    return money, profit, pnl


df = pd.read_csv('ethusdtMACD.csv')
df['time'] = pd.to_datetime(df['time'],unit='s')
ndf = df.set_index('time')

l_signal, signals, fdate = lng_signal(ndf['RSI'], ndf['%K'], ndf['close'])
s_signal, signals = shrt_signal(ndf['RSI'], ndf['%K'], ndf['close'])

signals.sort()
money, profit, pnl = isgood_signal(ndf['RSI'], ndf['%K'], ndf['close'], ndf['high'], ndf['low'], ndf['MACD'], ndf['Histogram'], ndf['Signal'])





print('TOTAL PROFIT:', profit)
print('ROI:', (money - 50000)/50000)
# print('HITRATE:', hitrate)
print('PNL:', pnl)





duplst = usuablelst
dupclose = dayclose
dupopen = dayclose
dup_prevopen = prevopen
dup_prevclose = prevclose

for (entry, close, opn, p_open, p_close) in zip(duplst, dupclose, dupopen, dup_prevopen, dup_prevclose):
    
    if z >= 96.0:
        break

    else:
        if entry[0:10] == date_of_entries[z][0:10]:
            z += 1
            if z >= 96.0:
                break
            else:
                if entry[0:10] == date_of_entries[z][0:10]:
                    usuablelst.insert(x, entry)
                    dayclose.insert(x,close)
                    dayopen.insert(x,opn)
                    prevopen.insert(x, p_open)
                    prevclose.insert(x, p_close)
                    z += 1
                    if z >= 96.0:
                        break
                    else:
                        if entry[0:10] == date_of_entries[z][0:10]:
                            usuablelst.insert(x, entry)
                            dayclose.insert(x,close)
                            dayopen.insert(x,opn)
                            prevopen.insert(x, p_open)
                            prevclose.insert(x, p_close)
                            z += 1
                            if z >= 96.0:
                                break
                            else:
                                if entry[0:10] == date_of_entries[z][0:10]:
                                    usuablelst.insert(x, entry)
                                    dayclose.insert(x,close)
                                    dayopen.insert(x,opn)
                                    prevopen.insert(x, p_open)
                                    prevclose.insert(x, p_close)

                                    z += 1
        x+=1

daycandle = []
prevcandle = []

daychange = []
prevchange = []



for (opn, close) in zip(dayopen, dayclose):
    opnday = float(opn)
    closeday = float(close)

    change = ((closeday - opnday)/opnday) * 100

    daychange.append(change)

    if opnday > closeday:
        daycandle.append('RED')
    else:
        daycandle.append('GREEN')


for (popn, pclose) in zip(prevopen, prevclose ):
    popnday = float(popn)
    pcloseday = float(pclose)

    pchange = ((pcloseday - popnday)/popnday) * 100

    prevchange.append(pchange)

    if popnday > pcloseday:
        prevcandle.append('RED')
    else:
        prevcandle.append('GREEN')

stuff = {}

stuff['Position Side'] = position_side
stuff['Entry Dates'] = date_of_entries
stuff['PNL%'] = pnllst
stuff['PREVCANDLE'] = prevcandle
stuff['PREVCHANGE'] = prevchange
stuff['DAYCANDLE'] = daycandle
stuff['DAYCHANGE'] = daychange

df = pd.DataFrame(stuff)

with pd.ExcelWriter('ltcusdt4hwith1day.xlsx') as writer:  
    df.to_excel(writer, sheet_name='Sheet_name_1')

print(len(date_of_entries))
print('FILE CREATED')