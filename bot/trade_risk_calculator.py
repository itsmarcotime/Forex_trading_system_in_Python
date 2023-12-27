from api.oanda_api import OandaApi
import constants.defs as defs
from infrastructure.instrument_collection import instrumentCollection as ic

def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):
    prices = api.get_prices([pair])