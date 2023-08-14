from api.oanda_api import oanda_api
from infrastructure.instrument_collection import instrumentCollection

if __name__ == '__main__':
    api = oanda_api()

    instrumentCollection.CreateFile(api.get_instruments(), "./data")
    instrumentCollection.load_instruments("./data")
    instrumentCollection.PrintInstruments()