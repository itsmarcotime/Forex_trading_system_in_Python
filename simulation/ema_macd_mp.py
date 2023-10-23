from multiprocessing import Process

import pandas as pd
from dateutil import parser
from technicals.indicators import MACD
from simulation.guru_tester import GuruTester
from infrastructure.instrument_collection import InstrumentCollection

BUY = 1
SELL = -1
NONE = 0

def apply_signal(row):
    if row.direction == BUY and row.mid_l > row.EMA:
        return BUY
    if row.direction == SELL and row.mid_h < row.EMA:
        return SELL
    return NONE 

def apply_cross(row):
    if row.macd_delta > 0 and row.mad_delta_prev < 0:
        return BUY
    if row.macd_delta < 0 and row.macd_delta_prev > 0:
        return SELL
    return NONE

def prepare_data(df: pd.DataFrame, slow, fast, signal, ema):
    df_an = df.copy()
    df_an = MACD(df_an, n_slow=slow, n_fast=fast, n_signal=signal)
    df_an['macd_delta'] = df_an.MACD - df_an.SIGNAL
    df_an['macd_delta_prev'] = df_an.macd_delta.shift(1)
    df_an['direction'] = df_an.apply(apply_cross, axis=1)
    df_an['EMA'] = df_an.mid_c.ewm(span=ema, min_periods=ema).mean()
    df_an.dropna(drop=True, inplace=True)
    return df_an

def load_data(pair, time_d=1):
    start = parser.parse("2020-10-01T00:00:00Z")
    end = parser.parse("2021-01-01T00:00:00Z")

    df = pd.read_pickle(f"./data/{pair}_H{time_d}.pkl")
    df_m5 = pd.read_pickle(f"./data/{pair}_M5.pkl")

    df = df[(df.time >= start) & (df.time < end)]
    df_m5 = df_m5[(df_m5.time >= start) & (df_m5.time < end)]

    df.reset_index(drop=True, inplace=True)
    df_m5.reset_index(drop=True, inplace=True)

    return df, df_m5

def simulate_params(pair, df, df_m5, slow, fast, signal, ema, time_d):
    prepped_df = prepare_data(df, slow, fast, signal, ema)
    gt = GuruTester(prepped_df, apply_signal, df_m5, use_spread=True, time_d=time_d)
    gt.run_test()

    gt.df_results['slow'] = slow
    gt.df_results['fast'] = fast
    gt.df_results['signal'] = signal
    gt.df_results['ema'] = ema
    gt.df_results['pair'] = pair

    return gt.df_results

def run_pair(pair):
    time_d = 4

    df, df_m5 = load_data(pair, time_d=time_d)

    results = []
    trades = []

    print("\n--> Running", pair)

    for slow in [26,52]:
        for fast in [12,18]:
            if slow <= fast:
                continue
            for signal in [9,12]:
                for ema in [50,100]:
                    sim_res_df = simulate_params(pair, df, df_m5, slow, fast, signal, ema, time_d)
                    r = sim_res_df.result.sum()
                    trades.append(sim_res_df)
                    print(f"--> {pair} {slow} {fast} {ema} {signal} {r}")
                    results.append(dict(pair=pair, slow=slow, fast=fast, ema=ema, results=r, signal=signal))
    pd.concat(trades).to_pickle(f"./exploration/macd_ema/macd_ema_trades_{pair}.pkl")
    return pd.DataFrame.from_dict(results)

def run_ema_macd(ic: InstrumentCollection):
    results = []
    our_curr = ['USD', 'GBP', 'JPY', 'NZD']
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}"
            if pair in ic.instruments_dict.keys():
                results = run_pair(pair)
                results.to_pickle(f"./exploration/macd_ema/macd_ema_res_{pair}.pkl")

import time
import random

def run_process(name):
    print("PROCESS", name, "STARED")

    time.sleep(random.randint(3, 8))

    print("PROCESS", name, "ENDED")

def get_sim_pairs(l_curr, ic: InstrumentCollection):
    pairs = []
    
    for p1 in l_curr:
        for p2 in l_curr:
            pair = f"{p1}_{p2}"
            if pair in ic.instruments_dict.keys():
                pairs.append(pair)
    return pairs

def run_processes(ic: InstrumentCollection):
    pairs = get_sim_pairs(['USD', 'GBP', 'JPY', 'NZD', 'AUD', 'CAD'], ic) 

    limit = 4
    current = 0

    while current < len(pairs):
        print("\n NEW LOOP", len(pairs))
        print("current", current)

        processes = []
        todo = len(pairs) - current
        if todo < limit:
            limit = todo

        for _ in range(limit):
            processes.append(Process(target=run_process, args=(pairs[current],)))
            current += 1
        
        for p in processes:
            p.start()

        for p in processes:
            p.join()

    print("ALL DONE")