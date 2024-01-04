from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import time
from models.candle_timing import CandleTiming
from bot.trade_risk_calculator import get_trade_units
import constants.defs as defs

def lm(msg, pair):
    # print(msg, pair)
    pass

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")

    # print(api.get_prices(["GBP_JPY"]))

    print('GBP_JPY', get_trade_units(api, 'GBP_JPY', defs.BUY, 0.4, 20, lm))
    print('AUD_NZD', get_trade_units(api, 'AUD_NZD', defs.BUY, 0.004, 20, lm))
    print('USD_CAD', get_trade_units(api, 'USD_CAD', defs.BUY, 0.004, 20, lm))
    