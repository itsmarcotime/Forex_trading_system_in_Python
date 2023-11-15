from api.oanda_api import OandaApi
from models.candle_timing import CandleTiming

class CandleManager:
    def __init__(self, api: OandaApi, trade_settings, log_message, granularity):
        self.api = api
        self.trade_settings = trade_settings
        self.log_message = log_message
        self.granularity = granularity
        self.pairs_list = list(self.trade_settings.keys())
        self.timings = { p: CandleTiming(self.api.last_complete_candle(p, self.granularity)) for p in self.pairs_list }
        for p, t in self.timings.items():
            self.log_message(f"CandleManager() init last_candle:{t}", p)