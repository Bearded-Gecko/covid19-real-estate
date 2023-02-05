import plotly.express as px
import requests
import json
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
import random 

app = Dash(__name__)


r = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
counties = json.loads(r.text)
target_states = ['23']
counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] in target_states]

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv', dtype={'fips': str})

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                    color_continuous_scale='Viridis',
                    range_color=(0, 12),
                    scope='usa',
                    labels={'unemp': 'unemployment rate'}
                    )
fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig.update_geos(fitbounds="locations") 
fig.show()


app.layout = html.Div([    
    dcc.Graph(
        id='choropleth',
        figure=fig
    )
])

def updateState(state):
    target_states = [state]
    
    counties = json.loads(r.text)

    counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] in target_states]

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv', dtype={'fips': str})

    fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                        color_continuous_scale='Viridis',
                        range_color=(0, 12),
                        scope='usa',
                        labels={'unemp': 'unemployment rate'}
                        )
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.update_geos(fitbounds="locations") 
    
    return fig

@app.callback(
    Output('choropleth', 'figure'),
    [Input('choropleth', 'clickData')])

def update_figure(clickData):    
    if clickData is not None:            
        location = clickData['points'][0]['location']

    state = random.randint(10,50)
    print("state", state)
    return updateState(str(state))



if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port=8050, debug=True)