from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from stream_example.streamer import run_streamer

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.load_instruments("./data")
    run_streamer()