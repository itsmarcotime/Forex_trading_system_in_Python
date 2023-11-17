from api.oanda_api import OandaApi
from models.trade_setting import TradeSettings

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):
    