import pandas as pd
from dateutil import parser
from technicals.indicators import MACD
from simulation.guru_tester import GuruTester
from infrastructure.instrument_collection import InstrumentCollection

BUY = 1
SELL = -1
NONE = 0

def apply_signal(row):
    if row.direction == BUY and row.mid_l > row.EMA:
        return BUY
    if row.direction == SELL and row.mid_h < row.EMA:
        return SELL
    return NONE 

def apply_cross(row):
    if row.macd_delta > 0 and row.mad_delta_prev < 0:
        return BUY
    if row.macd_delta < 0 and row.macd_delta_prev > 0:
        return SELL
    return NONE

def prepare_data(df: pd.DataFrame, slow, fast, signal, ema):
    df