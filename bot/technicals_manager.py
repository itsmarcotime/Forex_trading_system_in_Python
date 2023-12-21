import pandas as pd
from models.trade_decision import TradeDecision
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', None)
from technicals.indicators import BollingerBands
from api.oanda_api import OandaApi
from models.trade_setting import TradeSettings
import constants.defs as defs

ADDROWS = 20

def apply_signal(row, trade_settings: TradeSettings):
    if row.SPREAD <= trade_settings.maxspread:
        if row.mid_c > row.BB_UP and row.mid_o < row.BB_UP:
            return defs.SELL
        elif row.mid_c < row.BB_LW and row.mid_o > row.BB_LW:
            return defs.BUY
    return defs.NONE

def apply_SL(row, trade_settings: TradeSettings):
    if row.SIGNAL == defs.BUY:
        return row.mid_c - (row.GAIN / trade_settings.riskreward)
    elif row.SIGNAL == defs.SELL:
        return row.mid_c + (row.GAIN / trade_settings.riskreward)
    
    return 0.0

def apply_TP(row):
    if row.SIGNAL == defs.BUY:
        return row.mid_c + row.GAIN
    elif row.SIGNAL == defs.SELL:
        return row.mid_c - row.GAIN
    
    return 0.0

def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message):
    df.reset_index(drop=True, inplace=True)
    df['PAIR'] = pair
    df['SPREAD'] = df.ask_c - df.bid_c

    df = BollingerBands(df, trade_settings.n_ma, trade_settings.n_std)
    df['SIGNAL'] = df.apply(apply_signal, axis=1, trade_settings=trade_settings)
    df['GAIN'] = abs(df.mid_c - df.BB_MA)
    df['TP'] = df.apply(apply_TP, axis=1)
    df['SL'] = df.apply(apply_SL, axis=1, trade_settings=trade_settings)
    df['LOSS'] = abs(df.mid_c - df.SL)

    log_cols = ['PAIR', 'time', 'mid_c', 'mid_o', 'SL', 'TP', 'SPREAD', 'GAIN', 'SIGNAL']
    log_message(f"process_candles:\n{df[log_cols].tail()}", pair)

    return df[log_cols].iloc[-1]

def fetch_candles(pair, row_count, candle_time, granularity, api: OandaApi, log_message):
    df = api.get_candles_df(pair, count=row_count, granularity=granularity)

    if df is None or df.shape[0] == 0:
        log_message('tech_manager fetch_candles failed to get candles', pair)
        return None
    
    if df.iloc[-1].time != candle_time:
        log_message(f'tech_manager fetch_candles {df.iloc[-1].time} not correct', pair)
        return None
    
    return df

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):

    max_rows = trade_settings.n_ma + ADDROWS

    log_message(f"tech_manager: max_rows:{max_rows} candle_time:{candle_time}, granularity:{granularity}", pair)

    df = fetch_candles(pair, max_rows, candle_time, granularity, api, log_message)

    if df is not None:
        last_row = process_candles(df, pair, trade_settings, log_message)
        return TradeDecision(last_row)

    return None