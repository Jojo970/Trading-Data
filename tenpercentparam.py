import numpy as np
import pandas as pd
import mplfinance as mpf

def lng_signal(rsi, stochslowk, price):
    l_signal = []
    l_date = []
    fdate = []
    for date,value in rsi.iteritems():
        fdate.append(date)
        if value > 48 and stochslowk[date] < 30:
            l_signal.append(price[date])
            l_date.append(date)
        else:
            l_signal.append(np.nan)
    return l_signal, l_date, fdate
    
def isgood_lng_signal(rsi, stoch, price, high, low):
    gl_signal = []
    bl_signal = []
    pnl = 0
    standard = 0
    n = -1
    in_position = False
    for date in fdate:
        if rsi[date] > 48 and stoch[date] < 30:
            n += 1
        if in_position == False:
            if date == l_date[n]:
                standard = float(price[date])
                profit = standard * 1.10
                loss = standard * .97
                in_position = True
                tradedate = date


            else:
                pass
        elif in_position == True:
            for x in range(round(float(low[date])), round(float(high[date]))):
                if profit <= x:
                    gl_signal.append(tradedate)
                    pnl += 0.1
                    in_position = False
                else:
                    pass
            for x in range(round(float(low[date])), round(float(high[date]))):
                if loss >= x:
                    in_position = False
                    pnl += -0.03
                    bl_signal.append(tradedate)
                else:
                    pass
            else:
                pass
        
        
    return pnl, gl_signal, bl_signal

def isgood_shrt_signal(rsi, stoch, price, high, low):
    gs_signal = []
    bs_signal = []
    spnl = 0
    sstandard = 0
    sn = -1
    is_in_position = False
    for sdate in fdate:
        if rsi[sdate] < 48 and stoch[sdate] > 70:
            sn += 1
        if is_in_position == False:
            if sdate == s_date[sn]:
                sstandard = float(price[sdate])
                sprofit = sstandard * .9
                sloss = sstandard * 1.03
                is_in_position = True
                stradedate = sdate

            else:
                pass
        
        elif is_in_position == True:
            for x in range(round(float(low[sdate])), round(float(high[sdate]))):
                if sprofit >= x:
                    spnl += 0.1
                    gs_signal.append(stradedate)
                    is_in_position = False
                else:
                    pass
            for x in range(round(float(low[sdate])), round(float(high[sdate]))):
                if sloss <= x:
                    spnl += -0.03
                    bs_signal.append(stradedate)
                    is_in_position = False
                else:
                    pass
            else:
                pass
                
    return spnl, gs_signal, bs_signal


def shrt_signal(rsi, stochslowk, price):
    s_signal = []
    s_date = []
    for date,value in rsi.iteritems():
        if value < 48 and stochslowk[date] > 70:
            s_signal.append(price[date])
            s_date.append(date)
        else:
            s_signal.append(np.nan)
    return s_signal, s_date

df = pd.read_csv('ltcusdtstoch14.csv')
df['time'] = pd.to_datetime(df['time'],unit='s')
ndf = df.set_index('time')
tdf = ndf.loc['20-01-2020': '20-01-2021']

l_signal, l_date, fdate = lng_signal(tdf['RSI'], tdf['%K'], tdf['close'])
s_signal, s_date = shrt_signal(tdf['RSI'], tdf['%K'], tdf['close'])

pnl, gl_signal, bl_signal = isgood_lng_signal(tdf['RSI'], tdf['%K'], tdf['close'], tdf['high'], tdf['low'])
spnl, gs_signal, bs_signal = isgood_shrt_signal(tdf['RSI'], tdf['%K'], tdf['close'], tdf['high'], tdf['low'])


hitrate = (len(gl_signal) + len(gs_signal))/(len(gl_signal) + len(bl_signal) + len(gs_signal) + len(bs_signal))

print('OVERALL PNL:', (pnl + spnl))
print('HIT RATE:', hitrate)




# apd = mpf.make_addplot(l_signal,type='scatter',markersize=200,marker='^')
cpd = mpf.make_addplot(s_signal,type='scatter',markersize=200,marker='v')

# mpf.plot(tdf, type = 'candle', addplot = apd, datetime_format='%d-%m-%Y')
mpf.plot(tdf, type = 'candle', addplot = cpd, datetime_format='%d-%m-%Y')