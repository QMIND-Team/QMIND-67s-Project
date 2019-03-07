def plot_rebounds(low, middle, high):
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

    low_shape = dict(
        type='path',
        xref='x',
        yref='y',
        path='M -100, 150.8 L 100, 150.8 L 135, 313.2 L -135, 313.2 Z',
        fillcolor='rgba(255, 255, 0, 0.3)'
    )

    middle_shape = dict(
        type='path',
        xref='x',
        yref='y',
        path='M 135, 313.2 L 90, 450 L 0, 380 L -90, 450 L -135, 313.2 Z',
        fillcolor='rgba(0, 128, 0, 0.3)'
    )

    high_shape = dict(
        type='path',
        xref='x',
        yref='y',
        path='M 0, 380 L 90, 450 L 68.2, 516.2 L -68.2, 516.2 L -90, 450 Z',
        fillcolor='rgba(255, 0, 0, 0.3)'
    )

    rink_shapes.append(low_shape)
    rink_shapes.append(middle_shape)
    rink_shapes.append(high_shape)
    rink_shapes.append(goal_line1_shape)
    rink_shapes.append(goal_line2_shape)
    rink_shapes.append(goal_line3_shape)
    rink_shapes.append(goal_line4_shape)
    rink_shapes.append(goal_arc1_shape)
    rink_shapes.append(goal_arc2_shape)

    from plotly.offline import plot
    import plotly.graph_objs as go
    import numpy as np

    layout = dict(
        shapes=rink_shapes
    )

    x0 = np.random.normal(0, 35, high)
    y0 = np.random.normal(448, 27.5, high)

    x1 = np.random.normal(70, 25, middle)
    y1 = np.random.normal(370, 25, middle)

    x2 = np.random.normal(-70, 25, middle)
    y2 = np.random.normal(370, 25, middle)

    x3 = np.random.normal(0, 50, low)
    y3 = np.random.normal(232, 28, low)

    trace0 = go.Scatter(x=x0, y=y0, mode='markers')
    trace1 = go.Scatter(x=x1, y=y1, mode='markers')
    trace2 = go.Scatter(x=x2, y=y2, mode='markers')
    trace3 = go.Scatter(x=x3, y=y3, mode='markers')

    data = [trace0, trace1, trace2, trace3]

    fig = dict(data=data, layout=layout)

    plot(fig)

    return
