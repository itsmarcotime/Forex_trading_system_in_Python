import requests
import pandas as pd
import json
import constants.defs as defs
from dateutil import parser
from datetime import datetime as dt
from infrastructure.instrument_collection import instrumentCollection as ic
from models.open_trade import OpenTrade
from models.api_price import ApiPrice


class OandaApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(defs.SECURE_HEADER)
    
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url = f'{defs.OANDA_URL}/{url}'

        if data is not None:
            data = json.dumps(data)
        
        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url, params=params, data=data, headers=headers)
            
            if verb == "post":
                response = self.session.post(full_url, params=params, data=data, headers=headers)

            if verb == "put":
                response = self.session.put(full_url, params=params, data=data, headers=headers)
            
            if response == None:
                return False, {'error': 'verb not found'}
            
            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json() 
        except Exception as error:
            return False, {'Exception': error}
        
    def get_accoount_ep(self, ep, data_key):
        url = f'accounts/{defs.ACCOUNT_ID}/{ep}'
        ok, data = self.make_request(url)

        if ok == True and data_key in data:
            return data[data_key]
        else:
            print("ERROR get_account_ep()", data)
            return None
        
    def get_account_summary(self):
        return self.get_accoount_ep("summary", "account")
    
    def get_instruments(self):
        return self.get_accoount_ep("instruments", "instruments")
    
    def fetch_candles(self, pair_name, count=10, granularity="H1", price="MBA", date_f=None, date_t=None):
        url = f"instruments/{pair_name}/candles"
        params = dict(
            granularity = granularity,
            price = price
            )
        
        if date_f is not None and date_t is not None:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params["from"] = dt.strftime(date_f, date_format)
            params["to"] = dt.strftime(date_t, date_format)
        else:
            params["count"] = count

        ok, data = self.make_request(url, params=params)

        if ok == True and 'candles' in data:
            return data['candles']
        else:
            print("ERROR fetch_candles()", params, data)
            return None

    def get_candles_df(self, pair_name, **kwargs):

        data = self.fetch_candles(pair_name, **kwargs)

        if data is None:
            return None 
        if len(data) == 0:
            return pd.DataFrame()
        
        prices = ["mid", "bid", "ask"]
        ohlc = ["o", "h", "l", "c"]

        final_data = []
        for candle in data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volume'] = candle['volume']

            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f'{p}_{o}'] = float(candle[p][o])
            final_data.append(new_dict)

        df = pd.DataFrame.from_dict(final_data)
        return df
    
    def last_complete_candle(self, pair_name, granularity):
        df = self.get_candles_df(pair_name, granularity=granularity, count=10)
        if df.shape[0] == 0:
            return None
        return df.iloc[-1].time
    
    def place_trade(self, pair_name: str, units: float, direction: int, stop_loss:float=None, take_profit: float=None):

        url = f"accounts/{defs.ACCOUNT_ID}/orders"

        instrument = ic.instruments_dict[pair_name]
        units = round(units, instrument.tradeUnitsPrecision)

        if direction == defs.SELL:
            units = units * -1


        data = dict(
            order=dict(
                units=str(units),
                instrument=pair_name,
                type="MARKET"
            )
        )

        if stop_loss is not None:
            sld = dict(price=str(round(stop_loss, instrument.displayPrecision)))
            data['order']['stopLossOnFill'] = sld

        if take_profit is not None:
            tpd = dict(price=str(round(take_profit, instrument.displayPrecision)))
            data['order']['takeProfitOnFill'] = tpd

        #print(data)

        ok, response = self.make_request(url, verb="post", data=data, code=201)

        #print(ok, response)

        if ok == True and 'orderFillTransaction' in response:
            return response['orderFillTransaction']['id']
        else:
            return None
        
    def close_trade(self, trade_id):
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        ok, _ = self.make_request(url, verb='put', code=200)

        if ok == True:
            print(f"closed {trade_id} successfully")
        else:
            print(f"Failed to close {trade_id}")

        return ok
    
    def get_open_trade(self, trade_id):
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}"
        ok, response = self.make_request(url)

        if ok == True and 'trade' in response:
            return OpenTrade(response['trade'])
        
    def get_open_trades(self):
        url = f"accounts/{defs.ACCOUNT_ID}/openTrades"
        ok, response = self.make_request(url)

        if ok == True and 'trades' in response:
            return [OpenTrade(x) for x in response['trades']] 
        
    def get_prices(self, instruments_list):
        url = f"accounts/{defs.ACCOUNT_ID}/pricing"

        params = dict(
            instruments = ",".join(instruments_list),
            includeHomeConversions = True
        )

        ok, response = self.make_request(url, params=params)

        if ok == True and 'prices' in response and 'homeConversions' in response:
            return [ApiPrice(x, response['homeConversions']) for x in response['prices']] 
        
        return None