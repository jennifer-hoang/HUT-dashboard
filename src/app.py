from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


# Layout
app.layout = html.Div([
    html.H1('HUT Dashboard'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Routes', value='tab-1-example-graph'),
        dcc.Tab(label='Families', value='tab-2-example-graph'),
        dcc.Tab(label='Volunteers', value='tab-3-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
])

# Callbacks
@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-2-example-graph':
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
    elif tab == 'tab-3-example-graph':
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
