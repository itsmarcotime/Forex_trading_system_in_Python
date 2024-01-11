import json
import requests
import constants.defs as defs
from models.live_api_price import LiveApiPrice
import threading
from infrastructure.log_wrapper import LogWrapper

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

class PriceStreamer(threading.Thread):
    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        super().__init__()
        self.pairs_list = shared_prices.keys()
        self.price_lock = price_lock
        self.price_events = price_events
        self.shared_prices = shared_prices
        self.log = LogWrapper("PriceStreamer")
        print(self.pairs_list)

    def run(self):

        params = dict(
            instruments = ",".join(self.pairs_list)
        )

        url = f"{STREAM_URL}/accounts/{defs.ACCOUNT_ID}/pricing/stream"

        response = requests.get(url, params=params, headers=defs.SECURE_HEADER, stream=True)

        for price in response.iter_lines():
            if price:
                decoded_price = json.loads(price.decode('utf-8'))
                if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                    print(LiveApiPrice(decoded_price).get_dict())