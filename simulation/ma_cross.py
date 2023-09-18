import pandas as pd
import os.path
from infrastructure.instrument_collection import instrumentCollection as ic
from simulation.ma_excel import create_ma_res

class MA_Result:
    def __init__(self, df_trades, pairname, ma_l, ma_s, granularity):
        self.df_trades = df_trades
        self.pairname = pairname
        self.ma_l = ma_l
        self.ma_s = ma_s
        self.granularity = granularity
        self.result = self.result_ob()

    def __repr__(self):
        return str(self.result)

    def result_ob(self):
        return dict(
            pair = self.pairname,
            num_trades = self.df_trades.shape[0],
            total_gain = int(self.df_trades.GAIN.sum()),
            mean_gain = int(self.df_trades.GAIN.mean()),
            min_gain = int(self.df_trades.GAIN.min()),
            max_gain = int(self.df_trades.GAIN.max()),
            ma_l = self.ma_l,
            ma_s = self.ma_s,
            cross = f"{self.ma_s}_{self.ma_l}",
            granularity = self.granularity
        )

BUY = 1
SELL = -1
NONE = 0
get_ma_col = lambda x: f"MA_{x}"
add_cross = lambda x: f"{x.ma_s}_{x.ma_l}"

def is_trade(row):
    if row.DELTA >= 0 and row.DELTA_PREV < 0:
        return BUY
    elif row.DELTA < 0 and row.DELTA_PREV >= 0:
        return SELL
    return NONE

def load_price_data(pair, granularity, ma_list):
    df = pd.read_pickle(f"./data/{pair}_{granularity}.pkl")
    for ma in ma_list:
        df[get_ma_col(ma)] = df.mid_c.rolling(window=ma).mean()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_trades(df_analysis, instrument, granularity):
    df_trades = df_analysis[df_analysis.TRADE != NONE].copy()
    df_trades["DIFF"] = df_trades.mid_c.diff().shift(-1)
    df_trades.fillna(0, inplace=True)
    df_trades["GAIN"] = df_trades.DIFF / instrument.pipLocation
    df_trades["GAIN"] = df_trades["GAIN"] * df_trades["TRADE"]
    df_trades["granularity"] = granularity
    df_trades["pair"] = instrument.name
    df_trades["GAIN_C"] = df_trades["GAIN"].cumsum()
    return df_trades

def assess_pair(price_data, ma_l, ma_s, instrument, granularity):
    df_analysis = price_data.copy()
    df_analysis["DELTA"] = df_analysis[ma_s] - df_analysis[ma_l]
    df_analysis["DELTA_PREV"] = df_analysis["DELTA"].shift(1)
    df_analysis["TRADE"] = df_analysis.apply(is_trade, axis=1)
    df_trades = get_trades(df_analysis, instrument, granularity)
    df_trades["ma_l"] = ma_l
    df_trades["ma_s"] = ma_s
    df_trades["cross"] = df_trades.apply(add_cross, axis=1)
    return MA_Result(
        df_trades,
        instrument.name,
        ma_l,
        ma_s,
        granularity,
    )

def append_df_to_file(df, filename):
    # if this file exits
    if os.path.isfile(filename):
        fd = pd.read_pickle(filename)
        df = pd.concat([fd, df])
    
    df.reset_index(inplace=True, drop=True)
    df.to_pickle(filename)
    print(filename, df.shape)
    print(df.tail(2))

def get_fullname(filepath, filename):
    return f"{filepath}/{filename}.pkl"

def process_macro(results_list, filename):
    rl = [x.result for x in results_list]
    df = pd.DataFrame.from_dict(rl)
    append_df_to_file(df, filename)

def process_trades(results_list, filename):
    df = pd.concat([x.df_trades for x in results_list])
    append_df_to_file(df, filename)

def process_results(results_list, filepath):
    process_macro(results_list, get_fullname(filepath, "ma_res"))
    process_trades(results_list, get_fullname(filepath, "ma_trades"))

    # rl = [x.result for x in results_list]
    # df = pd.DataFrame.from_dict(rl)
    # print(df)
    # print(results_list[0].df_trades.head(2))

def analyse_pair(instrument, granularity, ma_long, ma_short, filepath):

    ma_list = set(ma_long + ma_short)
    pair = instrument.name

    price_data = load_price_data(pair, granularity, ma_list)
    #print(pair)
    #print(price_data.head(3))

    results_list = []

    for ma_l in ma_long:
        for ma_s in ma_short:
            if ma_l <= ma_s:
                continue

            ma_result = assess_pair(
                price_data,
                get_ma_col(ma_l),
                get_ma_col(ma_s),
                instrument,
                granularity
            )
            print(ma_result)
            results_list.append(ma_result)
    process_results(results_list, filepath)
    pass
            

def run_ma_sim(curr_list=["CAD", "JPY", "GBP", "NZD"],
                granularity=["H1"],
                ma_long=[20,40],
                ma_short=[10],
                filepath="./data"):
    ic.load_instruments("./data")
    for g in granularity:
        for p1 in curr_list:
            for p2 in curr_list:
                pair = f"{p1}_{p2}"
                if pair in ic.instruments_dict.keys():
                    analyse_pair(ic.instruments_dict[pair], g, ma_long, ma_short, filepath)
        create_ma_res(g)
        