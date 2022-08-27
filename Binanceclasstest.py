import talib, time
import numpy as np
from binance.client import Client as BClient


class GetBinanceClient:

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

        self.lsthighs = []
        self.lstlows = []
        self.lstcloses = []

        self.inposition = False
    def b_getclient(self):
        self.client = BClient(self.api_key, self.api_secret)
    
    def b_getdata(self):
        self.candles = self.client.futures_klines(symbol=binance_coin, interval = BClient.KLINE_INTERVAL_4HOUR)
        for data in self.candles:
            highs = float(data[2])
            lows = float(data[3])
            closes = float(data[4])

            self.lsthighs.append(highs)
            self.lstlows.append(lows)
            self.lstcloses.append(closes)
        self.lastcloses = self.lstcloses[-50:]
        self.lasthighs = self.lsthighs[-50:]
        self.lastlows = self.lstlows[-50:]

        self.np_closes = np.array(self.lastcloses)
        self.np_highs = np.array(self.lasthighs)
        self.np_lows = np.array(self.lastlows)

        self.USDT_balance = self.client.futures_account_balance()
        self.funds = float(self.USDT_balance[0]['balance'])
        self.funds_to_trade = self.funds * .5
        self.current_price = self.client.futures_symbol_ticker(symbol= binance_coin)
        self.quantity = self.funds_to_trade / float(self.current_price['price'])
        # print(self.quantity)
    def b_get_rsi_stoch(self):
        self.b_slowk, self.b_slowd = talib.STOCH(self.np_highs, self.np_lows, self.np_closes, 8, 3, 0, 3, 0)
        self.b_rsi = talib.RSI(self.np_closes, 14)
        self.b_realslowk = self.b_slowk[-1]
        self.b_realrsi = self.b_rsi[-1]
        self.b_realslowd = self.b_slowd[-1]
        # print('BINANCE DATASET FOR:', binance_coin)
        # print('%K:',self.b_realslowk)
        # print('%D:',self.b_realslowd)
        # print('RSI:',self.b_realrsi)
  
    def b_signal(self):
        if self.b_realslowk < 25 and self.b_realrsi > 48:
            if self.inposition == False:
                print('SIGNAL SAYS LONG FOR', binance_coin, 'ON 4HOUR CANDLE!!!')
                self.client.futures_create_order(symbol = binance_coin, side = 'BUY', position_side = 'LONG', type = 'TRAILING_STOP_MARKET', quantity = self.quantity, callbackRate = 5)
                time = time.gmtime(time.time())
                print(time)
                self.inposition = True
        if self.b_realslowk > 75 and self.b_realrsi < 48:
            if self.inposItion == False:
                print('SIGNAL SAYS SHORT FOR', binance_coin, 'ON 4HOUR CANDLE!!!')
                self.client.futures_create_order(symbol = binance_coin, side = 'BUY', position_side = 'SHORT', type = 'TRAILING_STOP_MARKET', quantity = self.quantity, callbackRate = 5)
                time = time.gmtime(time.time())
                print(time)
                self.inposition = True

    def b_order(self):
        try:
            self.client.futures_get_open_orders()
            self.client.futures_position_information()
        except:
            self.inposition = False
        

binance_coin = input('Enter Binance Pair (ex. BNBBTC):')

binance = GetBinanceClient('Wu1e4Thcwnlt8lRCxh5hrlV7XzLA8Ai7mLC5xfkkzUnouVb6D71RtCJXfFvVIa0v',
 'XKmqS1PSB0zcE6Cn9j4WuDzrgekgGCkb43SVaCKbUlWUa48r8zc01u7KGSf0oiQE')
binance.b_getclient()

while True:
    binance.b_getdata()
    binance.b_get_rsi_stoch()
    binance.b_signal()
    binance.b_order()
    time.sleep(3)