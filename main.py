from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser
from infrastructure.collect_data import run_collection

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    run_collection(instrumentCollection, api)