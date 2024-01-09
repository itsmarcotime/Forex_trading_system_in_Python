# class ApiPrice:
#     def __init__(self, api_ob):
#         self.instrument = api_ob['instrument']
#         self.ask = float(api_ob['asks'][0]['price'])
#         self.bid = float(api_ob['bids'][0]['price'])
#         self.sell_conv = float(api_ob['quoteHomeConversionFactors']['negativeUnits'])
#         self.buy_conv = float(api_ob['quoteHomeConversionFactors']['positiveUnits'])

#     def __repr__(self):
#         return f"ApiPrice() {self.instrument} {self.ask} {self.bid} {self.sell_conv:.6f} {self.buy_conv:.6f}"
from models.base_api_price import BaseApiPrice

class ApiPrice(BaseApiPrice):

    def __init__(self, api_ob, homeConversions):
        super().__init__(api_ob)

        base_instrument = self.instrument.split('_')[1]
        for hc in homeConversions:
            if hc ['currency'] == base_instrument:
                self.sell_conv = float(hc['positionValue'])
                self.buy_conv = float(hc['positionValue'])

    def __repr__(self):
        return f"ApiPrice() {self.instrument} {self.ask} {self.bid} {self.sell_conv:.6f} {self.buy_conv:.6f}"
        