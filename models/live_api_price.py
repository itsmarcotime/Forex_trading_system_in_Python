from models.base_api_price import BaseApiPrice

class LiveApiPrice(BaseApiPrice):

    def __init__(self, api_ob):
        super().__init__(api_ob)

    def __repr__(self):
        return f"LiveApiPrice() {self.instrument} {self.ask} {self.bid}"