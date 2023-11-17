from api.oanda_api import OandaApi
from models.trade_setting import TradeSettings

ADDROWS = 20

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):

    max_rows = trade_settings.n_ma + ADDROWS

    log_message(f"tech_manager: max_rows:{max_rows} candle_time:{candle_time}, granularity:{granularity}", pair)

    return None