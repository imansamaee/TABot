import numpy as np
import plotly.graph_objects as go

config = dict({'scrollZoom': True})


# noinspection PyTypeChecker
def draw_chart(data):
    df = data.df
    ind = data.indicators
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01, subplot_titles=(df.title, 'volume'),
                        row_width=[.5,.5, .5, 1.5])

    fig.add_trace(go.Candlestick(x=df.index, open=df["open"], high=df["high"],
                                 low=df["low"], close=df["close"], name=df.title),
                  row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=df["bband_low"], marker_color='grey', name="bband_low"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=df["bband_high"], marker_color='lightgrey', name="bband_high"), row=1, col=1)

    ## MACD
    # ---------------------------------------

    macd = df.ta.macd()
    fig.add_trace(
        go.Bar(x=df.index, y=macd['MACDh_12_26_9'], marker_color=np.where(macd['MACDh_12_26_9'] < 0, 'red', 'green'),
               showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=macd['MACDs_12_26_9'], marker_color='pink', name="macd_signal"), row=2,
                  col=1)
    fig.add_trace(go.Scatter(x=df.index, y=macd['MACD_12_26_9'], marker_color='blue', name="macd"), row=2, col=1)

    ## RSI
    # ---------------------------------------

    rsi = ind.smma(period=21, column_name='smma_21', apply_to='close')
    fig.add_trace(
        go.Bar(x=df.index, y=rsi, marker_color=np.where(rsi < 0, 'red', 'green'), name="RSI"),
        row=3, col=1)



    ## scotch
    # ---------------------------------------

    stoch = df.ta.stoch()

    fig.add_trace(go.Scatter(x=df.index, y=stoch['STOCHk_14_3_3'], marker_color='pink', name="macd_signal"), row=4,
                  col=1)
    fig.add_trace(go.Scatter(x=df.index, y=stoch['STOCHd_14_3_3'], marker_color='blue', name="macd"), row=4, col=1)



    cs = fig.data[0]

    # Set line and fill colors
    cs.increasing.fillcolor = '#3D9970'
    cs.increasing.line.color = '#3D9970'
    cs.decreasing.fillcolor = '#FF4136'
    cs.decreasing.line.color = '#FF4136'

    fig.update_layout(
        title=df.title + ' - ' + df.timeframe,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price ($/share)',
            titlefont_size=14,
            tickfont_size=12,

        ),
        autosize=False,
        width=2500,
        height=1100,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        template="plotly_dark"
    )

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show(config=config)
