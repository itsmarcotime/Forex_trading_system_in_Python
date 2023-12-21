class TradeDecision:

    def __init__(self, row):
        self.gain = row.GAIN
        self.loss = row.LOSS
        self.signal = row.SIGNAL
        self.sl = row.SL
        self.tp = row.TP
        self.pair = row.PAIR

    def __repr__(self):
        return f"TradeDecision(): {self.pair} dir:{self.signal} gain:{self.gain:.4f} sl:{self.sl:.4f} tp:{self.tp:.4f}"