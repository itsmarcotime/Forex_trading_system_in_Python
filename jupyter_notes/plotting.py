import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CandlePlot:
    def __init__(self, df, candles=True):
        self.df_plot = df.copy()
        self.candles = candles
        self.create_candle_fig()

    def add_timestr(self):
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]
        
    def create_candle_fig(self):
        self.add_timestr()
        self.fig = make_subplots(specs=[[{'secondary_y': True}]])
        if self.candles == True:
            self.fig.add_trace(go.Candlestick(
                x = self.df_plot.sTime,
                open = self.df_plot.mid_o,
                high = self.df_plot.mid_h,
                low = self.df_plot.mid_l,
                close = self.df_plot.mid_c,
                line = dict(width=1), 
                opacity = 1,
                increasing_fillcolor='#24A06B',
                decreasing_fillcolor='#CC2E3C',
                increasing_line_color='#2EC886',
                decreasing_line_color='#FF3A4C',
            ))

    def update_layout(self, width, height, nticks):
        self.fig.update_yaxes(
        gridcolor="#1f292f"
        )
        self.fig.update_xaxes(
            gridcolor="#1f292f",
            rangeslider=dict(visible=False),
            nticks=nticks
        )
        self.fig.update_layout(
            width = width,
            height = height,
            margin = dict(l=10, r=10, b=10, t=10),
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            font=dict(size=12, color="#e1e1e1"),
        )

    def add_traces(self, line_traces, is_sec=False):
        for t in line_traces:
            self.fig.add_trace(go.Scatter(
                x=self.df_plot.sTime,
                y=self.df_plot[t],
                line=dict(width=2),
                line_shape='spline',
                name=t
            ), secondary_y=is_sec)

    def show_plot(self, width=900, height=400, nticks=5, line_traces=[], sec_traces=[]):
        self.add_traces(line_traces)
        self.add_traces(sec_traces, is_sec=True)
        self.update_layout(width, height, nticks)
        self.fig.show()
