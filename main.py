from api.oanda_api import oanda_api
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from dateutil import parser

if __name__ == '__main__':
    api = oanda_api()

    dfr = parser.parse("2021-04-21T01:00:00Z")
    dto = parser.parse("2021-04-28T16:00:00Z")

    df_candles = api.get_candles_df("EUR_USD", granularity='H1', date_f=dfr, date_t=dto)

    print(df_candles.head())
    print()
    print(df_candles.tail())



    #print(api.fetch_candles("EUR_USD", granularity='D', price="MB"))

    # instrumentCollection.CreateFile(api.get_instruments(), "./data")
    # instrumentCollection.load_instruments("./data")
    # instrumentCollection.PrintInstruments()
    #run_ma_sim(curr_list=["EUR", "USD", "GBP", "JPY", "AUD", "CAD"])