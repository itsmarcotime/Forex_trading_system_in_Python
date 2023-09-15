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
    return None

def collect_data(pair, granularity, date_f, date_t, file_prefix, api: OandaApi):
    
    time_step = INCREMENTS[granularity]

    end_date = parser.parse(date_t)
    from_date = parser.parse(date_f)

    candle_dfs = []

    to_date = from_date

    while to_date < end_date:
        to_date = from_date + dt.timedelta(minutes=time_step)
        if to_date > end_date:
            to_date = end_date

        candles = fetch_candles(pair, granularity, from_date, to_date, api)

        if candles is not None and candles.empty == False:
            candle_dfs.append(candles)
        else:
            print(f"{pair} {granularity} {from_date} {to_date} --> NO CANDLES")

        from_date = to_date

    if len(candle_dfs) > 0:
        final_df = pd.concat(candle_dfs)
        save_file(final_df, file_prefix, granularity, pair)
    else:
        print(f"{pair} {granularity} --> NO DATA SAVED")


def run_collection(ic: InstrumentCollection, api: OandaApi):
    our_curr = ["EUR", "GBP", "AUD"]
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            if pair in ic.instruments_dict.keys():
                for g in ["M5"]:
                    print(pair, g)
                    collect_data(pair, g, "2021-06-01T00:00:00Z", "2021-12-01T00:00:00Z", "./data/", api)