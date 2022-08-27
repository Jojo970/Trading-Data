import numpy as np
import pandas as pd
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
    
def isgood_signal(rsi, stoch, price, high, low, momentum):
    g_signal = []
    b_signal = []

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
    slope_mom = []
    mom = []

    standard = 0
    n = -1
    contract = 0
    money = 50000
    moneytwo = 50000
    pnl = 0
    leverage = 2
    equity = .9
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
            money += (money * -0.00075 * equity)
            contract = int((money * equity)/standard) * leverage
            in_long_position = True
            tradedate = date
            

            entries.append(round(moneytwo, 2))
            date_of_entries.append(sdate)
            position_side.append('LONG')
            mom.append(momentum[date])
            som = momentum[date] - momentum[prevdate]
            slope_mom.append(som)
            datelongentry.append(price[date])
            dateshortentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)


        elif rsi[date] < 48 and stoch[date] > 70 and in_short_position == False and in_long_position == False and date == signals[n]:
            standard = float(price[date])
            entryprice.append(standard)
            newstandard = float(price[date])
            money += (money * -0.00075 * equity)
            contract = int((money * equity)/standard) * leverage
            in_short_position = True
            tradedate = date
            

            entries.append(round(moneytwo, 2))
            date_of_entries.append(sdate)
            position_side.append('SHORT')
            mom.append(momentum[date])
            som = momentum[date] - momentum[prevdate]
            slope_mom.append(som)
            dateshortentry.append(price[date])
            datelongentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)


        elif in_short_position == False and in_long_position == False:
            datelongentry.append(np.nan)
            dateshortentry.append(np.nan)
            dateshortexit.append(np.nan)
            datelongexit.append(np.nan)

        prevdate = date

        if in_short_position == True:
            datelongentry.append(np.nan)
            dateshortentry.append(np.nan)
            datelongexit.append(np.nan)
            dateshortexit.append(np.nan)
            for x in range(round(float(low[date]) * 1000), round(float(high[date]) * 1000)): # checking if stop loss is activated on given day
                if (newstandard * 1030) <= x:
                    in_short_position = False 
                    money += (standard - (newstandard * 1.03)) * contract
                    money += (money * -0.00075 * equity)
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


            if ((newstandard * 1.03) - standard) < 0:
                g_signal.append(tradedate)
            elif ((newstandard * 1.03) - standard) > 0:
                b_signal.append(tradedate)

            
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
                money += (money * -0.00075 * equity)
                pnl += (money - moneytwo)/ moneytwo
                gainloss.append(round((money - moneytwo), 2))
                pnllst.append(round(((money - moneytwo)/moneytwo)*100, 2))
                moneytwo = money
                date_of_exits.append(sdate)
                exits.append(round(moneytwo, 2))
                datelongexit[-1] = price[date]
                extprice = newstandard * .97
                exitprice.append(extprice)


                if ((newstandard * .97) - standard) > 0:
                    g_signal.append(tradedate)
                elif ((newstandard * .97) - standard) < 0:
                    b_signal.append(tradedate)
                else:
                    pass
            elif (newstandard * .03) >= (newstandard - low[date]):
                newstandard = float(high[date])

                
        
    profit = money - 50000
    return money, g_signal, b_signal, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, datelongentry, dateshortentry, datelongexit, dateshortexit, dfmoneylst, entryprice, exitprice, slope_mom, mom


df = pd.read_csv('ethusdtmomentum.csv')
df['time'] = pd.to_datetime(df['time'],unit='s')
ndf = df.set_index('time')

l_signal, signals, fdate = lng_signal(ndf['RSI'], ndf['%K'], ndf['close'])
s_signal, signals = shrt_signal(ndf['RSI'], ndf['%K'], ndf['close'])

signals.sort()
money, g_signal, b_signal, profit, pnl, exits, entries, date_of_exits, date_of_entries, position_side, gainloss, pnllst, datelongentry, dateshortentry, datelongexit, dateshortexit, moneylst, entryprice, exitprice, slope_mom, mom = isgood_signal(ndf['RSI'], ndf['%K'], ndf['close'], ndf['high'], ndf['low'], ndf['MOM'])







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
stuff['MOM SLOPE'] = slope_mom
stuff['MOMENTUM'] = mom


df = pd.DataFrame(stuff)

corr = df.corr()
print(corr)

with pd.ExcelWriter('ltcusdtmomentumstuff.xlsx') as writer:  
    df.to_excel(writer, sheet_name='Sheet_name_1')

# hitrate = len(g_signal)/ (len(g_signal) + len(b_signal))

print('TOTAL PROFIT:', profit)
print('ROI:', (money - 50000)/50000)
# print('HITRATE:', hitrate)
print('PNL:', pnl)