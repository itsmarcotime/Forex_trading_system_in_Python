from api.oanda_api import oanda_api
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim

if __name__ == '__main__':
    api = oanda_api()
    print(api.fetch_candles("EUR_USD", granularity='D', price="MB"))

    # instrumentCollection.CreateFile(api.get_instruments(), "./data")
    # instrumentCollection.load_instruments("./data")
    # instrumentCollection.PrintInstruments()
    #run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "AUD", "CAD"])