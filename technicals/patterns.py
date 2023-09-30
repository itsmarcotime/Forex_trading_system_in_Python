import pandas as pd

def apply_candle_props(df: pd.DataFrame):
    df_an = df.copy()
    direction = df_an.mid_c - df_an.mid_o
    body_size = abs(direction)
    direction = [1 if x >= 0 else -1 for x in direction]
    full_range = df_an.mid_h - df_an.mid_l
    body_perc = (body_size / full_range) * 100
    body_lower = df_an[['mid_c', 'mid_o']].min(axis=1)
    body_upper = df_an[['mid_c', 'mid_o']].max(axis=1)
    body_bottom_perc = ((body_lower - df_an.mid_l) / full_range) * 100
    body_top_perc = 100 - (((df_an.mid_h - body_upper) / full_range) * 100)

    low_change = df_an.mid_l.pct_change() * 100
    high_change = df_an.mid_h.pct_change() * 100
    body_size_change = body_size.pct_change() * 100

    df_an['body_lower'] = body_lower
    df_an['body_upper'] = body_upper
    df_an['body_bottom_perc'] = body_bottom_perc
    df_an['body_top_perc'] = body_top_perc
    df_an['body_perc'] = body_perc
    df_an['direction'] = direction
    df_an['body_size'] = body_size
    df_an['low_change'] = low_change
    df_an['high_change'] = high_change
    df_an['body_size_change'] = body_size_change

    return df_an

def apply_patterns(df: pd.DataFrame):
    df_an = apply_candle_props(df)
    return df_an