from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from api.stream_prices import stream_prices
from stream_example.streamer import run_streamer

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    # stream_prices(['GBP_JPY', 'AUD_NZD'])
    run_streamer()