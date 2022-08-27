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


def isgood_signal(rsi, stoch, price, high, low):
    entries = []
    exits = []
    entryprice = []
    exitprice = []
    date_of_entries = []
    date_of_exits = []
    position_side = []
    gainloss = []
    pnllst = []
    prevdatelst = []

    standard = 0
    n = -1
    contract = 0
    money = 50000
    moneytwo = 50000
    pnl = 0
    leverage = 2
    
    in_long_position = False
    in_short_position = False
    loop = False
    
    for date in fdate:
        
        loop == False
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
            prevdatelst.append(prevdate)
            loop = True



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
            prevdatelst.append(prevdate)
            loop = True

        
        
        prevdate = date

        if in_short_position == True and loop == False:
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
                    extprice = newstandard * 1.03
                    exitprice.append(extprice)

                    break

            
            if in_short_position == True and newstandard > low[date]:
                newstandard = float(low[date])



        
        elif in_long_position == True and loop == False:

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
                extprice = newstandard * .97
                exitprice.append(extprice)

            elif (newstandard * .03) >= (newstandard - low[date]):
                newstandard = float(high[date])

                
        
    profit = money - 50000
    return money, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, entryprice, exitprice, prevdatelst

def dailysignal(price, opn):
    dailydatelst = []
    dailyclose = []
    dailyopen = []
    dailydictopen = {}
    dailydictclose = {}

    for date,value in price.iteritems():
        day = str(date)
        dailyclose.append(value)
        dailyopen.append(opn[date])
        dailydatelst.append(day)
        dailydictopen[day] = value
        dailydictclose[day] = opn[date]

    return dailydatelst, dailyclose, dailyopen, dailydictopen, dailydictclose

df = pd.read_csv('ltcusdtMACD.csv')
df['time'] = pd.to_datetime(df['time'],unit='s')
ndf = df.set_index('time')

l_signal, signals, fdate = lng_signal(ndf['RSI'], ndf['%K'], ndf['close'])
s_signal, signals = shrt_signal(ndf['RSI'], ndf['%K'], ndf['close'])

signals.sort()
money, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, entryprice, exitprice, prevdatelst = isgood_signal(ndf['RSI'], ndf['%K'], ndf['close'], ndf['high'], ndf['low'])

daydf = pd.read_csv('ltcusdt1d.csv')
daydf['time'] = pd.to_datetime(daydf['time'],unit='s')
timedaydf = daydf.set_index('time')



dailydatelst, dailyclose, dailyopen,dailydictopen, dailydictclose = dailysignal(timedaydf['close'], timedaydf['opn'])

fhentries = []
dailyentrydates = []
dayopen = []
dayclose = []
prevlst = []
usuablelst = []
prevdaylst = []
prevclose = []
prevopen = []
prev = 'l'


f = 0
n = 0
x = 0
z = 0
p = 0

prevdate = '0000000000000'

for day in date_of_entries:
    if day[0:10] != prevdate[0:10]:
        fhentries.append(day)
        prevdate = day

    else: pass


for date in dailydatelst:
    if f >= 82:
        break
    else:
        if date[0:10] == fhentries[f][0:10]:
            dailyentrydates.append(date)
            f+=1
        else:
            dailyentrydates.append('nan')

for x in [1,2,3,4,5,6,7,8,9,0,11]:
    dailyentrydates.append('nan')



for sav in dailydatelst:
    if prev == 'l':
        prev = sav
    else:
        prevdaylst.append(prev)
        prev = sav

prevdaylst.append('nan')

for (entry, date) in zip(dailyentrydates, dailydatelst):
    if entry == date:
        usuablelst.append(entry)
    else: pass



for (dailydate, close, opn, prev) in zip(dailyentrydates, dailyclose, dailyopen, prevdaylst):
    if dailydate != 'nan':
        dayopen.append(opn)
        dayclose.append(close)
        prevlst.append(prev)
    else:
        pass


for pr in prevlst:
    prevopen.append(dailydictopen[pr])
    prevclose.append(dailydictclose[pr])







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