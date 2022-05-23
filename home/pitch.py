from home.models import MatchResult, SituationMatch, League
import plotly.graph_objects as go
import numpy as np


def draw_pitch(x_min=0, y_min=0, x_max=108, y_max=68):
    layout = {
        # 'title': 'Title of the figure',
        # 'template': 'plotly_dark'
        'paper_bgcolor': '#002430',
        'plot_bgcolor': '#303640',
        # 'xaxis_title': 'X',
        # 'yaxis_title': 'Y',
        'height': 700,
        # 'width': 900,

    }

    x_conversion = x_max / 100
    y_conversion = y_max / 100

    pitch_x = [0, 5.8, 11.5, 17, 50, 83,
               88.5, 94.2, 100]  # pitch x markings
    pitch_x = [x * x_conversion for x in pitch_x]

    pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100]  # pitch y markings
    pitch_y = [x * y_conversion for x in pitch_y]

    goal_y = [45.2, 54.8]  # goal posts
    goal_y = [x * y_conversion for x in goal_y]

    points = [
        [pitch_x[6], pitch_y[3]],
        [pitch_x[2], pitch_y[3]],
        [pitch_x[4], pitch_y[3]]
    ]
    radius = x_max / 10

    circle_points = [pitch_x[4] - radius, pitch_y[3] - radius, pitch_x[4] + radius, pitch_y[3] + radius]
    arc_point = [pitch_x[6] - radius, pitch_y[3] - radius, pitch_x[6] + radius, pitch_y[3] + radius]
    arc_point_2 = [pitch_x[2] - radius, pitch_y[3] - radius, pitch_x[2] + radius, pitch_y[3] + radius]

    points_x = [pitch_x[6], pitch_x[2], pitch_x[4]]
    points_y = [pitch_y[3], pitch_y[3], pitch_y[3]]

    fig = go.Figure(
        data=[go.Scatter(x=points_x, y=points_y, mode="markers", showlegend=False,
                         marker=dict(size=10, color="LightSeaGreen"))], layout=layout)
    # fig.update_layout(width=900, height=500)

    fig.update_xaxes(range=[x_min - 10, x_max + 10],
                     showticklabels=False, showgrid=False, visible=False)
    fig.update_yaxes(range=[y_min - 5, y_max + 5],
                     showticklabels=False, showgrid=False, visible=False)

    # side and goal lines
    lx1 = [x_min, x_max, x_max, x_min, x_min]
    ly1 = [y_min, y_min, y_max, y_max, y_min]

    lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
    ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    lx3 = [0, pitch_x[3], pitch_x[3], 0]
    ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    # goals
    lx4 = [x_max, x_max + 2, x_max + 2, x_max]
    ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    lx5 = [0, -2, -2, 0]
    ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    # 6 yard boxes
    lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
    ly6 = [pitch_y[2], pitch_y[2], pitch_y[4], pitch_y[4]]

    lx7 = [0, pitch_x[1], pitch_x[1], 0]
    ly7 = [pitch_y[2], pitch_y[2], pitch_y[4], pitch_y[4]]

    # Halfway line, penalty spots, and kickoff spot
    lx8 = [pitch_x[4], pitch_x[4]]
    ly8 = [0, y_max]

    lines = [
        [lx1, ly1],
        [lx2, ly2],
        [lx3, ly3],
        [lx4, ly4],
        [lx5, ly5],
        [lx6, ly6],
        [lx7, ly7],
        [lx8, ly8],
    ]

    # line = [lx1[0], ly1[0], lx1[1], ly1[1]]
    # line_2 = [lx1[1], ly1[1], lx1[2], ly1[2]]

    for line in lines:
        i = 0
        for x, y in zip(line[0], line[1]):
            if i == 0:
                x0 = x
                y0 = y
            else:
                x1 = x
                y1 = y
                fig.add_shape(type='line',
                              #   xref="paper", yref="paper",
                              x0=x0,
                              y0=y0,
                              x1=x1,
                              y1=y1,
                              line=dict(
                                  color="#d3d3d3",
                                  width=1,
                              ))
                x0 = x1
                y0 = y1
            i += 1

    al, beta = alpha(pitch_x[6], pitch_y[3], pitch_x[5], radius)
    fig.add_shape(type="circle",
                  x0=circle_points[0], y0=circle_points[1], x1=circle_points[2], y1=circle_points[3],
                  line_color="LightSeaGreen",
                  )
    fig.add_shape(type='path',
                  path=ellipse_arc(pitch_x[6], pitch_y[3], a=radius, b=radius, start_angle=beta, end_angle=beta + al,
                                   N=160),
                  line_color='LightSeaGreen')

    fig.add_shape(type='path',
                  path=ellipse_arc(pitch_x[2], pitch_y[3], a=radius, b=radius, start_angle=-al / 2,
                                   end_angle=al / 2, N=160),
                  line_color='LightSeaGreen')

    return fig


def ellipse_arc(x_center=0, y_center=0, a=1, b=1, start_angle=0, end_angle=2 * np.pi, N=100, closed=False):
    t = np.linspace(start_angle, end_angle, N)
    x = x_center + a * np.cos(t)
    y = y_center + b * np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    if closed:
        path += ' Z'
    return path


def alpha(xo, yo, lx, r):
    dx = xo - lx
    dy = np.sqrt(r ** 2 - dx ** 2)
    xs_1 = xo - dx
    ys_1 = yo - dy
    xs_2 = xo - dx
    ys_2 = yo + dy
    xs_3 = xo + r
    ys_3 = yo

    k = np.sqrt((xs_2 - xs_1) ** 2 + (ys_2 - ys_1) ** 2)
    alpha = np.arcsin(k / 2 / r)  # arc lenght

    k = np.sqrt((xs_3 - xs_1) ** 2 + (ys_3 - ys_1) ** 2)
    beta = np.arcsin(k / 2 / r)  # since

    return alpha * 2, beta * 2


def get_info_situations(match) -> dict:
    print(match)
    situations = match.situation_result.all()
    situations_home = situations.filter(h_a='h')
    situations_away = situations.filter(h_a='a')
    print('situations_away :', situations_away)
    print()
    goals_home = situations_home.filter(result='Goal')
    goals_away = situations_away.filter(result='Goal')
    shots_home = situations_home.exclude(result='Goal')
    shots_away = situations_away.exclude(result='Goal')

    def iter_to_list(column_name, value=goals_home, dtype_='float'):
        return np.fromiter(value.values_list(column_name, flat=True), dtype=dtype_)

    x_goals_home = iter_to_list('x')
    y_goals_home = iter_to_list('y')
    player_goals_home = iter_to_list('player', dtype_='U60')
    xg_goals_home = iter_to_list('xg')
    x_shots_home = iter_to_list('x', shots_home)
    y_shots_home = iter_to_list('y', shots_home)
    player_goals_shots = iter_to_list('player', shots_home, dtype_='U60')
    xg_shots_home = iter_to_list('xg')

    x_goals_away = iter_to_list('x', goals_away)
    y_goals_away = iter_to_list('y', goals_away)
    player_goals_away = iter_to_list('player', goals_away, 'U60')
    xg_goals_away = iter_to_list('xg', goals_away)
    x_shots_away = iter_to_list('x', shots_away)
    y_shots_away = iter_to_list('y', shots_away)
    player_goals_shots = iter_to_list('player', shots_away, dtype_='U60')
    xg_shots_away = iter_to_list('xg', goals_away)

    home_s = {
        'x_goals_home': x_goals_home,
        'y_goals_home': y_goals_home,
        'player_goals_home': player_goals_home,
        'xg_goals_home': xg_goals_home,
        'x_shots_home': x_shots_home,
        'y_shots_home': y_shots_home,
        'player_goals_shots': player_goals_shots,
        'xg_shots_home': xg_shots_home
    }
    print('home: ', home_s)
    print()
    away_s = {
        'x_goals_away': x_goals_away,
        'y_goals_away': y_goals_away,
        'player_goals_away': player_goals_away,
        'xg_goals_away': xg_goals_away,
        'x_shots_away': x_shots_away,
        'y_shots_away': y_shots_away,
        'player_goals_shots': player_goals_shots,
        'xg_shots_away': xg_shots_away
    }
    print('away ', away_s)
    return home_s, away_s


def add_situations_to_pitch(fig, home_s, away_s, xmax=108, ymax=68):
    fig.add_scatter(x=home_s['x_goals_home']* xmax ,
                    y = home_s['y_goals_home']*ymax ,
                    mode = 'markers',
                    text = home_s['player_goals_home'],
                    hovertemplate = '<b>%{text}</b>',
                    marker=dict(size=home_s['xg_goals_home'] * 1000,
                                sizemode='area',
                                color='rgba(235, 79, 56, .6)',
                                line=dict(width=0))
                    )
    fig.add_scatter(x=(1 - away_s['x_goals_away'] )* xmax ,
                    y = (1 - away_s['y_goals_away']) *ymax ,
                    mode = 'markers',
                    text = away_s['player_goals_away'],
                    hovertemplate = '<b>%{text}</b>',
                    marker=dict(size=away_s['xg_goals_away'] * 1000,
                                sizemode='area',
                                color='rgba(235, 79, 222, .6)',
                                line=dict(width=0))
                    )
    # situation away

    # fig.add_scatter(x=x_a * 108, y=y_a * 68, mode="markers", text=players_situation_a, hovertemplate='<b>%{text}</b>',
    #                 marker=dict(size=s_xG_a * 1000,
    #                             sizemode='area',
    #                             color='rgba(235, 79, 56, .6)',
    #                             line=dict(width=0)))
