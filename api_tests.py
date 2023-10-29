from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    api.place_trade('EUR_USD', 100, 1, take_profit=1.10200, stop_loss=1.09200)
    