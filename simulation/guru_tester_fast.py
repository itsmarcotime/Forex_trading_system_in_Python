import pandas as pd
import datetime as dt

BUY = 1
SELL = -1
NONE = 0



def apply_take_profit(row, PROFIT_FACTOR):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            return (row.ask_c - row.ask_o) * PROFIT_FACTOR + row.ask_c
        else:
            return (row.bid_c - row.bid_o) * PROFIT_FACTOR + row.bid_c
    else:
        return 0.0

def apply_stop_loss(row):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            return row.ask_o
        else:
            return row.bid_o
    else:
        return 0.0

def remove_spread(df):
    for a in ["ask", "bid"]:
        for b in ["o", "h", "l", "c"]:
            c = f"{a}_{b}"
            df[c] = df[f"mid_{b}"]

def apply_signals(df, PROFIT_FACTOR, sig):
    df["SIGNAL"] = df.apply(sig, axis=1)
    df["TP"] = df.apply(apply_take_profit, axis=1, PROFIT_FACTOR=PROFIT_FACTOR)
    df["SL"] = df.apply(apply_stop_loss, axis=1)

def create_signals(df, time_d=1):
    df_signals = df[df.SIGNAL != NONE].copy() 
    df_signals['m5_start'] = [x + dt.timedelta(hours=time_d) for x in df_signals.time]
    df_signals.drop(['time', 'mid_o', 'mid_h', 'mid_l', 'bid_o', 'bid_h', 'bid_l',
    'ask_o', 'ask_h', 'ask_l', 'direction'], axis=1, inplace=True)
    df_signals.rename(columns={
        'bid_c' : 'start_price_BUY',
        'ask_c' : 'start_price_SELL',
        'm5_start' : 'time'
    }, inplace=True)
    return df_signals


INDEX_start_price_BUY = 0
INDEX_start_price_SELL = 1
INDEX_SIGNAL = 2
INDEX_TP = 3
INDEX_SL = 4
INDEX_time = 5
INDEX_bid_h = 6
INDEX_bid_l = 7
INDEX_ask_h = 8
INDEX_ask_l = 9
INDEX_name = 10


class Trade:
    def __init__(self, list_values, index, profit_factor, loss_factor):
        self.running = True
        self.start_index_m5 = list_values[INDEX_name][index]
        self.profit_factor = profit_factor
        self.loss_factor = loss_factor
        
        if list_values[INDEX_SIGNAL][index] == BUY:
            self.start_price = list_values[INDEX_start_price_BUY][index]
            self.trigger_price = list_values[INDEX_start_price_BUY][index]
            
        if list_values[INDEX_SIGNAL][index] == SELL:
            self.start_price = list_values[INDEX_start_price_SELL][index]
            self.trigger_price = list_values[INDEX_start_price_SELL][index]
            
        self.SIGNAL = list_values[INDEX_SIGNAL][index]
        self.TP = list_values[INDEX_TP][index]
        self.SL = list_values[INDEX_SL][index]
        self.result = 0.0
        self.end_time = list_values[INDEX_time][index]
        self.start_time = list_values[INDEX_time][index]
        
    def close_trade(self, list_values, index, result, trigger_price):
        self.running = False
        self.result = result
        self.end_time = list_values[INDEX_time][index]
        self.trigger_price = trigger_price
        
    def update(self, list_values, index):
        if self.SIGNAL == BUY:
            if list_values[INDEX_bid_h][index] >= self.TP:
                self.close_trade(list_values, index, self.profit_factor, list_values[INDEX_bid_h][index] )
            elif list_values[INDEX_bid_l][index]  <= self.SL:
                self.close_trade(list_values, index, self.loss_factor, list_values[INDEX_bid_l][index] )
        if self.SIGNAL == SELL:
            if list_values[INDEX_ask_l][index] <= self.TP:
                self.close_trade(list_values, index, self.profit_factor, list_values[INDEX_ask_l][index])
            elif list_values[INDEX_ask_h][index] >= self.SL:
                self.close_trade(list_values, index, self.loss_factor, list_values[INDEX_ask_h][index])   

class GuruTesterFast:
    def __init__(self, df_big,
                    apply_signal, 
                    df_m5,
                    use_spread=True,
                    LOSS_FACTOR = -1.0,
                    PROFIT_FACTOR = 1.5,
                    time_d=1 ):
        self.df_big = df_big.copy()
        self.use_spread = use_spread
        self.apply_signal = apply_signal
        self.df_m5 = df_m5.copy()
        self.LOSS_FACTOR = LOSS_FACTOR
        self.PROFIT_FACTOR = PROFIT_FACTOR
        self.time_d = time_d

        self.prepare_data()
        
    def prepare_data(self):
        
        #print("prepare_data...")

        if self.use_spread == False:
            remove_spread( self.df_big)
            remove_spread( self.df_m5)


        apply_signals(self.df_big,
                    self.PROFIT_FACTOR,
                    self.apply_signal)


        df_m5_slim = self.df_m5[['time','bid_h', 'bid_l', 'ask_h', 'ask_l' ]].copy()
        df_signals = create_signals(self.df_big, time_d=self.time_d)

        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')
        self.merged.fillna(0, inplace=True)
        self.merged.SIGNAL = self.merged.SIGNAL.astype(int)

        



    def run_test(self):
        print("run_test...")
        open_trades_m5 = []
        closed_trades_m5 = []

        list_value_refs = [
            self.merged.start_price_BUY.array,
            self.merged.start_price_SELL.array,
            self.merged.SIGNAL.array,
            self.merged.TP.array,
            self.merged.SL.array,
            self.merged.time.array,
            self.merged.bid_h.array,
            self.merged.bid_l.array,
            self.merged.ask_h.array,
            self.merged.ask_l.array,
            self.merged.index.array,
        ]

        for index in range(self.merged.shape[0]):
            
            if list_value_refs[INDEX_SIGNAL][index] != NONE:
                open_trades_m5.append(Trade(list_value_refs, index, self.PROFIT_FACTOR, self.LOSS_FACTOR))  
                
            for ot in open_trades_m5:
                ot.update(list_value_refs, index)
                if ot.running == False:
                    closed_trades_m5.append(ot)
            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]

        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5]) 
        #print("Result:", self.df_results.result.sum())
