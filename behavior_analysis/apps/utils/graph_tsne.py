import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import random
import string


class GraphTsne(dcc.Graph):
    def __init__(self, parent_app, df, id=None):
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

        # Calculate tsne form dataframe
        df = df.sample(frac=0.1).sort_index().reset_index()
        cols = [c for c in df.columns if ('_x' in c or '_y' in c)]
        X = df[cols].to_numpy()

        tsne = TSNE(n_components=2, init='pca')
        Y = tsne.fit_transform(X)

        # Make figure
        fig = make_subplots(rows=1, cols=2)

        scatter_tsne = go.Scatter(
            x=list(Y[:, 0]),
            y=list(Y[:, 1]),
            mode='markers',
            marker=dict(size=1, color="gray")
        )
        fig.append_trace(scatter_tsne, row=1, col=1)
        fig.append_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=1, color="red")), row=1, col=1)

        scatter_markers = self.body_traces(df=df, frame=0)
        for sc in scatter_markers:
            fig.append_trace(sc, row=1, col=2)

        fig.update_layout(
            dict(
                # xaxis=dict(range=[-100, 100], autorange=False),
                # yaxis=dict(range=[-100, 100], autorange=False),
            ),
        )

        n_frames = 500
        frames = [
            go.Frame(
                data=[
                    go.Scatter(
                        x=[Y[fr, 0]],
                        y=[Y[fr, 1]],
                        mode="markers",
                        marker=dict(color="blue", size=10)
                    )
                ] + self.body_traces(df=df, frame=fr),
                traces=[1, 2, 3, 4, 5, 6, 7, 8]
            ) for fr in range(n_frames)
        ]
        fig.update(frames=frames)

        sliders = [
            {
                'yanchor': 'top',
                'xanchor': 'left',
                'currentvalue': {'visible': False},
                'transition': {'duration': 0.0, 'easing': 'linear'},
                'pad': {'b': 10, 't': 10},
                'len': 0.9, 'x': 0.1, 'y': 0,
                'steps': [{'args': [None, {'frame': {'duration': 0.0, 'easing': 'linear', 'redraw': False},
                                          'transition': {'duration': 0, 'easing': 'linear'}}],
                           'label': k, 'method': 'animate'} for k in range(n_frames)]
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
        #                     [f'{k}' for k in range(10)],
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
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                transition=dict(duration=0),
                                easing='linear',
                                fromcurrent=True,
                                mode='immediate'
                            )
                        ]
                    )
                ],
                direction='left',
                pad=dict(r=10, t=10),
                showactive=True, x=0.1, y=0, xanchor='right', yanchor='top'
            )
        ]

        fig['layout'].update(
            updatemenus=updatemenus,
            sliders=sliders,
            showlegend=False,
            margin=dict(l=0, r=0, b=0, t=0, pad=0),
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

    @staticmethod
    def body_traces(df, frame=0):
        """Returns list of Scatter traces with body strcture"""
        traces = [
            # Head traces
            go.Scatter(
                x=[df.loc[frame, 'Nose_x'], df.loc[frame, 'LeftEye_x'], df.loc[frame, 'RightEye_x'], df.loc[frame, 'Nose_x']],
                y=[df.loc[frame, 'Nose_y'], df.loc[frame, 'LeftEye_y'], df.loc[frame, 'RightEye_y'], df.loc[frame, 'Nose_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            # Left whiskers traces
            go.Scatter(
                x=[df.loc[frame, 'L1-1_x'], df.loc[frame, 'L1-2_x'], df.loc[frame, 'L1-3_x'], df.loc[frame, 'L1-4_x']],
                y=[df.loc[frame, 'L1-1_y'], df.loc[frame, 'L1-2_y'], df.loc[frame, 'L1-3_y'], df.loc[frame, 'L1-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            go.Scatter(
                x=[df.loc[frame, 'L2-1_x'], df.loc[frame, 'L2-2_x'], df.loc[frame, 'L2-3_x'], df.loc[frame, 'L2-4_x']],
                y=[df.loc[frame, 'L2-1_y'], df.loc[frame, 'L2-2_y'], df.loc[frame, 'L2-3_y'], df.loc[frame, 'L2-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            go.Scatter(
                x=[df.loc[frame, 'L3-1_x'], df.loc[frame, 'L3-2_x'], df.loc[frame, 'L3-3_x'], df.loc[frame, 'L3-4_x']],
                y=[df.loc[frame, 'L3-1_y'], df.loc[frame, 'L3-2_y'], df.loc[frame, 'L3-3_y'], df.loc[frame, 'L3-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            # Right whiskers traces
            go.Scatter(
                x=[df.loc[frame, 'R1-1_x'], df.loc[frame, 'R1-2_x'], df.loc[frame, 'R1-3_x'], df.loc[frame, 'R1-4_x']],
                y=[df.loc[frame, 'R1-1_y'], df.loc[frame, 'R1-2_y'], df.loc[frame, 'R1-3_y'], df.loc[frame, 'R1-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            go.Scatter(
                x=[df.loc[frame, 'R2-1_x'], df.loc[frame, 'R2-2_x'], df.loc[frame, 'R2-3_x'], df.loc[frame, 'R2-4_x']],
                y=[df.loc[frame, 'R2-1_y'], df.loc[frame, 'R2-2_y'], df.loc[frame, 'R2-3_y'], df.loc[frame, 'R2-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            ),
            go.Scatter(
                x=[df.loc[frame, 'R3-1_x'], df.loc[frame, 'R3-2_x'], df.loc[frame, 'R3-3_x'], df.loc[frame, 'R3-4_x']],
                y=[df.loc[frame, 'R3-1_y'], df.loc[frame, 'R3-2_y'], df.loc[frame, 'R3-3_y'], df.loc[frame, 'R3-4_y']],
                mode='lines+markers',
                marker=dict(color="black", size=10),
                line=dict(color='black', width=2)
            )
        ]

        return traces
