import requests
import pandas as pd
import constants.defs as defs
from dateutil import parser
from datetime import datetime as dt

class oanda_api:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {defs.API_KEY}",
            "Content-Type": "application/json"
        })
    
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url = f'{defs.OANDA_URL}/{url}'
        
        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url, params=params, data=data, headers=headers)
            
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

    def get_candles_df(self, data):
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
                for o in ohlc:
                    new_dict[f'{p}_{o}'] = float(candle[p][o])
            
            final_data.append(new_dict)

        df = pd.DataFrame.from_dict(final_data)
        return df