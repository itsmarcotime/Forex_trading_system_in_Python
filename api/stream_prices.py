import json
import requests
import constants.defs as defs
from models.live_api_price import LiveApiPrice

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

def stream_prices(pairs_list):

    params = dict(
        instruments = ",".join(pairs_list)
    )

    url = f"{STREAM_URL}/accounts/{defs.ACCOUNT_ID}/pricing/stream"

    response = requests.get(url, params=params, headers=defs.SECURE_HEADER, stream=True)

    for price in response.iter_lines():
        if price:
            decoded_price = json.loads(price.decode('utf-8'))
            # print(decoded_price)
            # print()
            if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                print(LiveApiPrice(decoded_price))