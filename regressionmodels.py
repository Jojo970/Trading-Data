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
    entries = []
    exits = []
    entryprice = []
    exitprice = []
    date_of_entries = []
    date_of_exits = []
    position_side = []
    gainloss = []
    pnllst = []
    dfmoneylst = []
    datelongentry = []
    dateshortentry= []
    datelongexit = []
    dateshortexit = []
    macdlst = []
    macdhist = []
    signallst = []


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
        
        dfmoneylst.append(money)
        
        sdate = str(date)
        
        if rsi[date] > 48 and stoch[date] < 30:
            n += 1

        elif rsi[date] < 48 and stoch[date] > 70:
            n += 1

        if rsi[date] > 48 and stoch[date] < 30 and in_long_position == False and in_short_position == False and date == signals[n]:
            standard = float(price[date])
            entryprice.append(standard)
            newstandard = float(price[date])
            money += money * -0.00075
            contract = int((money * .9)/standard) * leverage
            in_long_position = True
            

            entries.append(round(moneytwo, 2))
            date_of_entries.append(sdate)
            position_side.append('LONG')
            datelongentry.append(price[date])
            dateshortentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)
            macdlst.append(macd[date])
            macdhist.append(histogram[date])
            signallst.append(signal[date])

        elif rsi[date] < 48 and stoch[date] > 70 and in_short_position == False and in_long_position == False and date == signals[n]:
            standard = float(price[date])
            entryprice.append(standard)
            newstandard = float(price[date])
            money += money * -0.00075
            contract = int((money * .9)/standard) * leverage
            in_short_position = True

            

            entries.append(round(moneytwo, 2))
            date_of_entries.append(sdate)
            position_side.append('SHORT')
            dateshortentry.append(price[date])
            datelongentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)
            macdlst.append(macd[date])
            macdhist.append(histogram[date])
            signallst.append(signal[date])


        elif in_short_position == False and in_long_position == False:
            datelongentry.append(np.nan)
            dateshortentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)


        if in_short_position == True:
            datelongentry.append(np.nan)
            dateshortentry.append(np.nan)
            datelongexit.append(np.nan)
            dateshortexit.append(np.nan)
            for x in range(round(float(low[date]) * 1000), round(float(high[date]) * 1000)): # checking if stop loss is activated on given day
                if (newstandard * 1030) <= x:
                    in_short_position = False 
                    money += (standard - (newstandard * 1.03)) * contract
                    money += money * -0.00075
                    pnl += (money - moneytwo)/ moneytwo
                    gainloss.append(round((money - moneytwo), 2))
                    pnllst.append(round(((money - moneytwo)/moneytwo)*100, 2))
                    moneytwo = money
                    date_of_exits.append(sdate)
                    exits.append(round(moneytwo, 2))
                    dateshortexit[-1] = price[date]
                    extprice = newstandard * 1.03
                    exitprice.append(extprice)

                    break

            
            if in_short_position == True and newstandard > low[date]:
                newstandard = float(low[date])


        
        
        elif in_long_position == True:
            datelongentry.append(np.nan)
            dateshortentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)
            if (newstandard * .03) <= (newstandard - low[date]):
                in_long_position = False
                money += ((newstandard * .97) - standard) * contract
                money += money * -0.00075
                pnl += (money - moneytwo)/ moneytwo
                gainloss.append(round((money - moneytwo), 2))
                pnllst.append(round(((money - moneytwo)/moneytwo)*100, 2))
                moneytwo = money
                date_of_exits.append(sdate)
                exits.append(round(moneytwo, 2))
                datelongexit[-1] = price[date]
                extprice = newstandard * .97
                exitprice.append(extprice)

            elif (newstandard * .03) >= (newstandard - low[date]):
                newstandard = float(high[date])

                
        
    profit = money - 50000
    return money, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, datelongentry, dateshortentry, datelongexit, dateshortexit, dfmoneylst, entryprice, exitprice, macdlst, macdhist, signallst


df = pd.read_csv('ltcusdtMACD.csv')
df['time'] = pd.to_datetime(df['time'],unit='s')
ndf = df.set_index('time')

l_signal, signals, fdate = lng_signal(ndf['RSI'], ndf['%K'], ndf['close'])
s_signal, signals = shrt_signal(ndf['RSI'], ndf['%K'], ndf['close'])

signals.sort()
money, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, datelongentry, dateshortentry, datelongexit, dateshortexit, moneylst, entryprice, exitprice, macdlst, macdhist, signallst = isgood_signal(ndf['RSI'], ndf['%K'], ndf['close'], ndf['high'], ndf['low'], ndf['MACD'], ndf['Histogram'], ndf['Signal'])

value = []
values = []
valuesig = []
signalsstuff = []

for(x,y) in zip(macdlst, macdhist):
    if x == None or y == None:
        value.append(0)
    else:
        z = x/y
        value.append(z)

for(l,p) in zip(macdlst, macdhist):
    if l == None or p == None:
        values.append(0)
    else:
        o = p/l
        values.append(o)

for(mac,sig) in zip(macdlst, signallst):
    if mac == None or sig == None:
        values.append(0)
    else:
        c = mac/sig
        valuesig.append(c)



for x in signallst:
    if x == None:
        signalsstuff.append(0)
    else:
        signalsstuff.append(x)



vislst = {}
vislsts = {}
signalsdict = {}

badtrades = 0

for (k,v) in zip(pnllst, value):
    vislst[k] = v

for (r,stuff) in zip(pnllst, valuesig):
    vislsts[r] = stuff 

for (t,p) in zip(pnllst, signalsstuff):
    signalsdict[t] = p

tlist = sorted(vislst.items())

tlst = sorted(vislsts.items())

singles = sorted(signalsdict.items())


x,y = zip(*singles)




# plt.scatter(y,x)
# plt.show()



stuff = {}
stuff['Position Side'] = position_side
stuff['Entry Dates'] = date_of_entries
stuff['Exit Dates'] = date_of_exits
stuff['Entry Price'] = entryprice
stuff['Exit Price'] = exitprice
stuff['Entry Balance'] = entries
stuff['Exit Balance'] = exits
stuff['PNL'] = gainloss
stuff['PNL%'] =pnllst
stuff['MACD'] = macdlst
stuff['MACD Histogram'] = macdhist
stuff['SIGNAL'] = signallst
stuff['QUOTIANT'] = value



trade_df = pd.DataFrame(stuff)

with pd.ExcelWriter('LTCusdtperpMACDFILE.xlsx') as writer:  
    df.to_excel(writer, sheet_name='Sheet_name_1')

model = df.to_csv(index = False)





print('TOTAL PROFIT:', profit)
print('ROI:', (money - 50000)/50000)
# print('HITRATE:', hitrate)
print('PNL:', pnl)