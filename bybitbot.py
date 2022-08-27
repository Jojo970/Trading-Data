import numpy as np
import talib, time, pprint, logging
import bybit
from BybitWebsocket import BybitWebsocket

def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    logger = setup_logger()

client  = bybit.bybit(test=False, api_key="hmhKvvaNEdJk1ESb9k", api_secret="cy4QoUlyvnwMVIdN4NodN4x82jLDMp63XWro")
ws = BybitWebsocket(wsURL="wss://stream.bybit.com/realtime_public",
                         api_key="hmhKvvaNEdJk1ESb9k", api_secret="cy4QoUlyvnwMVIdN4NodN4x82jLDMp63XWro"
                        )


# gotdata = client.LinearKline.LinearKline_get(symbol="LTCUSDT", interval="240", limit=50, **{'from':1613690000}).result()

# kline = gotdata[0]['result']
# print(kline)

ws.subscribe_kline("LTCUSD", '240')

while(1):
    logger.info(ws.get_kline('LTCUSDT', '240'))
    
    time.sleep(5)


