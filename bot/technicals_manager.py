import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', None)
from api.oanda_api import OandaApi
from models.trade_setting import TradeSettings

ADDROWS = 20

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
        log_message(f"\n{df.tail()}", pair)

    return None