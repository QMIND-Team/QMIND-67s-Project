rink_shapes = []

outer_rink_shapes = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-250',
    y0='0',
    x1='250',
    y1='516.2',
    line=dict(
        width=1,
    )
)

rink_shapes.append(outer_rink_shapes)

outer_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='200',
    y0='580',
    x1='-200',
    y1='580',
    line=dict(
        width=1,
    )
)

rink_shapes.append(outer_line_shape)

outer_arc1_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M 200 580 C217 574, 247 532, 250 516.2',
    line=dict(
        width=1,
    )
)

outer_arc2_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M -200 580 C-217 574, -247 532, -250 516.2',
    line=dict(
        width=1,
    )
)

rink_shapes.append(outer_arc1_shape)
rink_shapes.append(outer_arc2_shape)

center_red_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-250',
    y0='0',
    x1='250',
    y1='0',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    )
)

rink_shapes.append(center_red_line_shape)

end_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-250',
    y0='516.2',
    x1='250',
    y1='516.2',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    )
)

rink_shapes.append(end_line_shape)

blue_line_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='250',
    y0='150.8',
    x1='-250',
    y1='145',
    line=dict(
        width=1,
        color='rgba(0, 0, 255, 1)'
    ),
    fillcolor='rgba(0, 0, 255, 1)'
)

rink_shapes.append(blue_line_shape)

center_red_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='2.94',
    y0='2.8',
    x1='-2.94',
    y1='-2.8',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    )
)

rink_shapes.append(center_red_circle_shape)

red_spot1_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='135.5',
    y0='121.8',
    x1='123.5',
    y1='110.2',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    ),
    fillcolor='rgba(255, 0, 0, 1)'
)

red_spot2_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='-135.5',
    y0='121.8',
    x1='-123.5',
    y1='110.2',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    ),
    fillcolor='rgba(255, 0, 0, 1)'
)
rink_shapes.append(red_spot1_shape)
rink_shapes.append(red_spot2_shape)

red_circle1_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='217.6',
    y0='487.2',
    x1='41.2',
    y1='313.2',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    )
)

red_circle2_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='-217.6',
    y0='487.2',
    x1='-41.2',
    y1='313.2',
    line=dict(
        width=1,
        color='rgba(255, 0, 0, 1)'
    )
)
rink_shapes.append(red_circle1_shape)
rink_shapes.append(red_circle2_shape)

goal_line1_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='64.7',
    y0='516.2',
    x1='82.3',
    y1='580',
    line=dict(
        width=1
    )
)

goal_line2_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='23.5',
    y0='516.2',
    x1='23.5',
    y1='493',
    line=dict(
        width=1
    )
)

goal_line3_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-64.7',
    y0='516.2',
    x1='-82.3',
    y1='580',
    line=dict(
        width=1
    )
)

goal_line4_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-23.5',
    y0='516.2',
    x1='-23.5',
    y1='493',
    line=dict(
        width=1
    )
)

goal_arc1_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M 23.5 493 C 20 480, -20 480, -23.5 493',
    line=dict(
        width=1
    )
)

goal_arc2_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M 17.6 516.2 C 15 530, -15 530, -17.6 516.2',
    line=dict(
        width=1
    )
)

rink_shapes.append(goal_line1_shape)
rink_shapes.append(goal_line2_shape)
rink_shapes.append(goal_line3_shape)
rink_shapes.append(goal_line4_shape)
rink_shapes.append(goal_arc1_shape)
rink_shapes.append(goal_arc2_shape)

from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import random

"""listx = []
for i in range(0, 50):
    x = random.randint(-230,231)
    listx.append(x)

listy = []
for j in range(0, 50):
    y = random.randint(150, 501)
    listy.append(y)

trace = go.Scatter(x=listx, y=listy, mode='markers')"""

#dataframe = pd.read_csv(Sample_Data.csv)
def hockey_plot(df):
    reb1 = data.loc[data['reb1'] == 1]
    reb2 = data.loc[data['reb2'] == 1]
    reb3 = data.loc[data['reb3'] == 1]
    total = pd.concat([reb1, reb2, reb3])

    trace_reb1 = go.Scatter(
        x=reb1['x']-250,
        y=580 - reb1['y'],
        mode='markers'
        )

    trace_reb2 = go.Scatter(
        x=reb2['x'] - 250,
        y=580 - reb2['y'],
        mode='markers'
        )

    trace_reb3 = go.Scatter(
        x=reb3['x'] - 250,
        y=580 - reb3['y'],
        mode='markers'
    )

    heatmap_trace = go.Histogram2dContour(
        x=total['x']-250, y=580 - total['y'], name='density', ncontours=1,
        colorscale='Blues', reversescale=True, showscale=False,
        contours=dict(coloring='heatmap')
    )

    data = [trace_reb1, trace_reb2, trace_reb3, heatmap_trace]

    updatemenus = list([
        dict(active=-1,
             buttons=list([
                 dict(label='1 Second Rebounds',
                      method='update',
                      args=[{'visible': [True, False, False, False]}]),
                 dict(label='2 Second Rebounds',
                      method='update',
                      args=[{'visible': [False, True, False, False]}]),
                 dict(label='3 Second Rebounds',
                      method='update',
                      args=[{'visible': [False, False, True, False]}]),
                 dict(label='All Rebounds',
                      method='update',
                      args=[{'visible': [True, True, True, False]}]),
                 dict(label='Heatmap',
                      method='update',
                      args=[{'visible': [True, True, True, True]}])
             ]))
    ])

    layout = dict(
        shapes=rink_shapes,
        updatemenus=updatemenus
    )

    fig = dict(data=data, layout=layout)

    plot(fig)