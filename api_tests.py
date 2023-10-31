from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import time

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    # trade_id = api.place_trade('EUR_USD', 100, 1)
    # print('opened:', trade_id)
    # time.sleep(10)
    # print(f"Closing {trade_id}", api.close_trade(trade_id))
    [print(x) for x in api.get_open_trades()]