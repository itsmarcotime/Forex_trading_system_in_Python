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