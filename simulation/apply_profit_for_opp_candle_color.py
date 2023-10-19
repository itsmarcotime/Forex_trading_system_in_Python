def apply_take_profit(row, PROFIT_FACTOR):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            if row.direction == BUY:
                return (row.ask_c - row.ask_o) * PROFIT_FACTOR + row.ask_c
            else:
                return (row.ask_o - row.ask_c) * PROFIT_FACTOR + row.ask_o
        else:
            if row.direction == SELL:
                return (row.bid_c - row.bid_o) * PROFIT_FACTOR + row.bid_c
            else:
                return (row.bid_o - row.bid_c) * PROFIT_FACTOR + row.bid_o
    else:
        return 0.0

def apply_stop_loss(row):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            if row.direction == BUY:
                return row.ask_o
            else:
                return row.ask_c
        else:
            if row.direction == SELL:
                return row.bid_o
            else:
                return row.bid_c
    else:
        return 0.0