import requests
import constants.defs as defs

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