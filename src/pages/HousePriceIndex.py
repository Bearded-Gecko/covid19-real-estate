import dash

dash.register_page(__name__)
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from visualize import Visualize,  Visualize2, Visualize3
import random
from urllib.request import urlopen
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import numpy as np
import json

credentials = service_account.Credentials.from_service_account_file(
'./chain-coders-5d47d58b2c33.json')

project_id = 'chain-coders'
client = bigquery.Client(credentials= credentials,project=project_id)
#query = "SELECT * FROM `redfin.redfin-data-state`"
#df = client.query(query).to_dataframe()


# -- Import and clean data (importing csv into pandas)
df = client.query("SELECT * FROM `redfin.HPI_state` ").to_dataframe()
df.dropna(subset=['HPI_base_1980'], inplace=True)
df.year_quarter = pd.to_datetime(df.year_quarter).dt.date
df.sort_values(['state_abbr', 'year_quarter'], inplace=True)
df.reset_index(drop=True, inplace=True)

df2 = client.query("SELECT * FROM `redfin.HPI_state_prediction` ").to_dataframe()
df2.year_quarter = pd.to_datetime(df2.year_quarter).dt.date
df2.sort_values(['state', 'year_quarter'], inplace=True)
df2.reset_index(drop=True, inplace=True)

#property types for drop down
property_set = ['']

#metric types for dropdown
metric_set = ['HPI_base_1980']

#dates for slider
sorted_dates = np.sort(df['year_quarter'].unique())
sorted_dates = ['{}'.format(i) for i in sorted_dates] #convert each date to string within a list
counter = 0
year = 1975

slider_labels = {}
#labels for slider
for index, date in enumerate(sorted_dates):
    if counter == index:
        slider_labels['{}'.format(index)] = str(year)
        year += 1
        counter += 4
    else: 
        slider_labels['{}'.format(index)] = ''
            
#color-scale
color_scale = [[0.0, '#edf8fb'],[0.2, '#ccece6'],[0.4, '#99d8c9'],
       [0.6, '#66c2a4'],[0.8, '#2ca25f'],[1.0, '#006d2c']] # purples

#-------------------------------#

metric_hpi = 'HPI_base_1980'
dash.register_page(__name__)

# ------------------------------------------------------------------------------
# App layout
#what goes inside dash layout are the dash components and any html we need
layout = html.Div([

    html.H1("HPI State Choropleth Data", style={'text-align': 'center'}), #html Title

#     html.Div(id='output_container', children=["Metric"], style = {'font-weight': 'bold'}),

    #components, e.g., drop downs, sliders
    #first drop down by metric
#    dcc.Dropdown(id="metric_hpi",
#                 placeholder = "Select Metric",
#                 options=metric_set,
#                 value=metric_set[0],
#                 style={'width': "60%",}
#                 ),

    html.Br(), #space between dropdowns

#     html.Div(id='output_container', style = {'font-weight': 'bold'}, 
#     children = ["Property Type"]
#     ),

    #second drop down for property type
#    dcc.Dropdown(id="property_type_hpi",
#                 placeholder = "Select Property Type",
##                 options=property_set,
#                 value=property_set[0],
#                 style={'width': "60%"},
#                 ),

    
    html.Br(), #space
    
    #create div element, e.g., text to display dropdown selection
    html.Div(id='output_container_hpi', children=[]),

    html.Br(), #space

    #graph object, e.g., choropleth
    dcc.Graph(id='choropleth_hpi', figure={}),

    

    #slider object
    dcc.Slider(0, len(sorted_dates), step = None, #min value of 0 and max of number of unique dates
               value=0, #where the slider starts
               marks = slider_labels,
               tooltip={"placement": "bottom", "always_visible": True}, #place slider at bottom of graph
               id='date_chosen_hpi'),

    #add line chart
    dcc.Graph(id = "line_chart_hpi", figure = {})

])
#-------------------------------#

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    Output(component_id='output_container_hpi', component_property='children'),
    Output(component_id='choropleth_hpi', component_property='figure'),
    Output(component_id = 'line_chart_hpi', component_property = 'figure'),
    #Input(component_id='property_type_hpi', component_property='value'),
    #Input(component_id = 'metric_hpi', component_property = 'value'),
    Input(component_id='date_chosen_hpi', component_property='value'),
    Input(component_id = 'choropleth_hpi', component_property = 'hoverData'))


def update_graph( date_chosen_hpi, hover):


    container = "Date Selected: {}".format(sorted_dates[date_chosen_hpi])

    dff = df.copy()
    dff = dff[dff['year_quarter'] == pd.to_datetime(sorted_dates[date_chosen_hpi])]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_abbr',
        scope="usa",
        color='{}'.format(metric_hpi),
        hover_data=['state_abbr', '{}'.format(metric_hpi)],
        color_continuous_scale= color_scale
    )
    line_data = px.line(dff, x = "year_quarter", y = [])

    if type(hover) == dict:
        hover_state = hover['points'][0]['customdata'][0]
        hover_df = df2[df2['state'] == hover_state]
        line_data = px.line(hover_df, x = "year_quarter", y = ['predicted', 'actual'], title = '{fmetric_hpi} for {fstate}'.format(fmetric_hpi = metric_hpi, fstate = hover_state))

    return container, fig, line_data
