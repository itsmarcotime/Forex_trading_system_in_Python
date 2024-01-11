import json
import threading
import time

def load_settings():
    with open("./bot/settings.json", "r") as f:
        return json.loads(f.read())
    
def run_price_streamer():
    print("run_price_streamer START")
    time.sleep(3)
    print("run_price_streamer END")

def run_streamer():
    settings = load_settings()

    shared_prices = {}
    shared_prices_events = {}
    shared_prices_lock = threading.Lock()

    for p in settings['pairs'].keys():
        shared_prices_events[p] = threading.Event()
        shared_prices[p] = {}

    threads = []

    price_stream_t = threading.Thread(target=run_price_streamer)
    threads.append(price_stream_t)
    price_stream_t.start()

    for t in threads:
        t.join()

    print("ALL DONE")