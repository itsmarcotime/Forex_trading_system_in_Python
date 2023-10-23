from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ema_macd_mp import run_ema_macd
from dateutil import parser
from infrastructure.collect_data import run_collection

if __name__ == '__main__':
    # api = OandaApi()
    instrumentCollection.load_instruments("./data")
    # run_collection(instrumentCollection, api)
    # run_ma_sim()
    run_ema_macd(instrumentCollection)