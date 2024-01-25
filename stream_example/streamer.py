import json
import threading
import time
from stream_example.stream_prices import PriceStreamer
from stream_example.stream_processor import PriceProcessor

def load_settings():
    with open("./bot/settings.json", "r") as f:
        return json.loads(f.read())

def run_streamer():
    settings = load_settings()

    shared_prices = {}
    shared_prices_events = {}
    shared_prices_lock = threading.Lock()

    for p in settings['pairs'].keys():
        shared_prices_events[p] = threading.Event()
        shared_prices[p] = {}

    threads = []

    price_stream_t = PriceStreamer(shared_prices, shared_prices_lock, shared_prices_events)
    price_stream_t.daemon = True
    threads.append(price_stream_t)
    price_stream_t.start()

    for p in settings['pairs'].keys():
        processing_t = PriceProcessor(shared_prices, shared_prices_lock, shared_prices_events, f"PriceProcessor_{p}", p)
        processing_t.daemon = True
        threads.append(processing_t)
        processing_t.start()

    # **** For MAC or Linux use!!!!!!! ***
    # try:
    #     for t in threads:
    #         t.join()
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    print("ALL DONE")