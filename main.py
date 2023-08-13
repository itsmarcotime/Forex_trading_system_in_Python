from api.oanda_api import oanda_api
from infrastructure.instrument_collection import instrumentCollection

if __name__ == '__main__':
    api = oanda_api()

    #data = api.get_account_summary()
    #print(data)

    #instrumentCollection.load_instruments("./data")
    #instrumentCollection.PrintInstruments()