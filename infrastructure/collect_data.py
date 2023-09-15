import pandas as pd
import datetime as dt
from dateutil import parser
from infrastructure.instrument_collection import InstrumentCollection
from api.oanda_api import OandaApi

CANDLE_COUNT = 3000

INCREMENTS = {
    'M5' : 5 * CANDLE_COUNT,
    'H1' : 60 * CANDLE_COUNT,
    'H4' : 240 * CANDLE_COUNT,
}

def save_file(final_df: pd.DataFrame, file_prefix, granularity, pair):
    pass

def fetch_candles(pair, granularity, date_f: dt.datetime, date_t: dt.datetime, api: OandaApi):
    pass

def collect_data(pair, granularity, date_f, date_t, file_prefix, api: OandaApi):
    pass

def run_collection(ic: InstrumentCollection, api: OandaApi):
    our_curr = ["EUR", "GBP", "AUD"]
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            if pair in ic.instruments_dict.keys():
                for g in ["H1"]:
                    print(pair, g)
                    collect_data(pair, g, "2021-10-01T00:00:00Z", "2021-12-01T00:00:00Z", "./data/", api)