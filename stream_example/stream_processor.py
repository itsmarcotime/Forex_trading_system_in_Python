import copy
import random
import threading
import time
from stream_example.stream_base import StreamBase

class PriceProcessor(StreamBase):
    def __init__(self, shared_prices, price_lock: threading.Lock, price_events, logname, pair):
        super().__init__(shared_prices, price_lock, price_events, logname)
        self.pair = pair

    def process_price(self):
        price = None

        try:
            self.price_lock.acquire()
            price = copy.deepcopy(self.shared_prices[self.pair])
        except Exception as error:
            self.log_message(f"CRASH: {error}", error=True)
        finally:
            self.price_lock.release()

        if price is None:
            self.log_message("NO PRICE", error=True)
        else:
            self.log_message(f"Found price: {price}")
            time.sleep(random.randint(2,5))
            self.log_message(f"Done processing price: {price}")


    def run(self):
        while True:
            self.price_events[self.pair].wait()
            self.process_price()
            self.price_events[self.pair].clear()