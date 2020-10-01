import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import random
import string


class GraphTsne(dcc.Graph):
    def __init__(self, parent_app, id=None):
        super().__init__()
        self.parent_app = parent_app
        # User chosen or randomly generated unique id
        if id is None:
            self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        else:
            self.id = id

        self.config = {
            'displayModeBar': False,
            'scrollZoom': False,
            'displaylogo': False
        }

        Y = np.random.rand(100, 2)

        # Make figure
        fig = make_subplots(rows=1, cols=2)

        scatter_base = go.Scatter(
            x=list(Y[:, 0]),
            y=list(Y[:, 1]),
            mode='markers',
            marker=dict(size=1, color="gray")
        )
        fig.append_trace(scatter_base, row=1, col=1)
        fig.append_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=2, color="red")), row=1, col=1)

        fig.update_layout(
            dict(
                # xaxis=dict(range=[-100, 100], autorange=False),
                # yaxis=dict(range=[-100, 100], autorange=False),
                margin=dict(l=0, r=0, b=0, t=0, pad=0),
            ),
        )

        frames = [
            go.Frame(
                data=[go.Scatter(
                    x=[Y[k, 0]],
                    y=[Y[k, 1]],
                    mode="markers",
                    marker=dict(color="blue", size=10))],
                traces=[1]
            ) for k in range(10)
        ]
        fig.update(frames=frames)

        sliders = [
            {
                'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {'font': {'size': 16}, 'prefix': 'Frame: ', 'visible': True, 'xanchor': 'right'},
                'transition': {'duration': 100.0, 'easing': 'linear'},
                'pad': {'b': 10, 't': 50},
                'len': 0.9, 'x': 0.1, 'y': 0,
                'steps': [{'args': [[k], {'frame': {'duration': 100.0, 'easing': 'linear', 'redraw': False},
                                          'transition': {'duration': 0, 'easing': 'linear'}}],
                           'label': k, 'method': 'animate'} for k in range(10)]
            }
        ]

        updatemenus = [
            dict(
                type='buttons',
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[
                            None,
                            dict(
                                frame=dict(duration=100, redraw=False),
                                transition=dict(duration=0),
                                easing='linear',
                                fromcurrent=True,
                                mode='immediate'
                            )
                        ]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[
                            None,
                            dict(
                                frame=dict(duration=100, redraw=False),
                                transition=dict(duration=0),
                                easing='linear',
                                fromcurrent=True,
                                mode='immediate'
                            )
                        ]
                    )
                ],
                direction='left',
                pad=dict(r=10, t=85),
                showactive=True, x=0.1, y=0, xanchor='right', yanchor='top'
            )
        ]

        fig['layout'].update(
            updatemenus=updatemenus,
            sliders=sliders
        )

        fig.update_yaxes(patch={
            'visible': False,
            "showticklabels": False,
            "ticks": ""
        })
        fig.update_xaxes(patch={
            'visible': False,
            "showticklabels": False,
            "ticks": ""
        })

        self.figure = fig
