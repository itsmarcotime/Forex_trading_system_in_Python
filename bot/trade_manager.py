from api.oanda_api import OandaApi
from models.trade_decision import TradeDecision

def trade_is_open(pair, api: OandaApi):
    open_trades = api.get_open_trades()

    for ot in open_trades:
        if ot.instrument == pair:
            return ot
    return None

def place_trade(trade_decision: TradeDecision, api: OandaApi, log_message, log_error):
    ot = trade_is_open(trade_decision.pair, api)

    if ot is not None:
        log_message(f"Failed to place trade {trade_decision}, already open: {ot}", trade_decision.pair)
        return None
    
    