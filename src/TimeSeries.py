import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div(children=[
    html.H4(children='Real Estate Data by Time'),
    html.Div([
        "Select a city: ",
        dcc.RadioItems(['New York City', 'Montreal','San Francisco'],
        'Montreal',
        id='timeseries-input')
    ]),
    html.Br(),
    html.Div(id='timeseries-output'),
])


@callback(
    Output(component_id='timeseries-output', component_property='children'),
    Input(component_id='timeseries-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'