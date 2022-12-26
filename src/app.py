from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = Dash(
    external_stylesheets=[dbc.themes.FLATLY]
)


# Layout
app.layout = html.Div([
    html.H1('HUT Dashboard'),
    dbc.Row([
        dbc.Col([
            html.H3('Selection Panel')
        ], width = 2),
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label='Routes', tab_id='tab-1'),
                dbc.Tab(label='Families', tab_id='tab-2'),
                dbc.Tab(label='Volunteers', tab_id='tab-3'),
            ],
            id = "tabs",
            active_tab='tab-1',
            ),
            html.Div(id='tabs-content')
        ], width = 10),
    ]),
])

# Callbacks
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'active_tab'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
            dbc.Row([
                dbc.Col([
                    html.H3('Content 1'),
                    dcc.Graph(
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }]
                        }
                    )
                ]),
                dbc.Col([
                    html.H3('Content 2')
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3('Content 3')
                ]),
                dbc.Col([
                    html.H3('Content 4')
                ])
            ])
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3'),
            dcc.Graph(
                id='graph-3-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 1, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
