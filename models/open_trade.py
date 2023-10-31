from dateutil import parser

class OpenTrade:
    def __init__(self, api_ob):
        self.id = api_ob['id']
        self.instrument = api_ob['instrument']
        self.price = float(api_ob['price'])
        self.currentUnits = float(api_ob['currentUnits'])
        self.unrealizedPL = float(api_ob['unrealizedPL'])
        self.marginUsed = float(api_ob['marginUsed'])
        
    def __repr__(self):
        return str(vars(self))