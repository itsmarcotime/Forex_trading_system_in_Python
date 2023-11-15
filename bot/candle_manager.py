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

    def update_timings(self):
        triggered = []

        for pair in self.pairs_list:
            current = self.api.last_complete_candle(pair, self.granularity)
            if current is None:
                self.log_message("Unable to get candle", pair)
                continue
            self.timings[pair].is_ready = False
            if current > self.timings[pair].last_time:
                self.timings[pair].is_ready = True
                self.timings[pair].last_time = current
                self.log_message(f"CandleManager() new candle:{self.timings[pair]}", pair)
                triggered.append(pair)

        return triggered

