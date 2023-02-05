import dash
from dash import Dash, dcc, html, Input, Output, callback, ctx
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from visualize import Visualize,  Visualize2, Visualize3
import random

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

credentials = service_account.Credentials.from_service_account_file(
'./chain-coders-5d47d58b2c33.json')

project_id = 'chain-coders'
client = bigquery.Client(credentials= credentials,project=project_id)
query = "SELECT * FROM `redfin.redfin-data-state-with-predictions2`"
df_state = client.query(query).to_dataframe()

# -- Import stateand clean data (importing csv into pandas)
# df_state= pd.read_csv("state_market_tracker.csv")
#format data type for time
df_state['period_begin'] = pd.to_datetime(df_state['period_begin'], format="%Y/%m/%d").dt.date
df_state['period_end'] = pd.to_datetime(df_state['period_end'], format="%Y/%m/%d").dt.date

# -- Import county and clean data (importing csv into pandas)
# df_county = pd.read_csv("redfin-data-county-fips.csv") 
query = "SELECT * FROM `chain-coders.redfin.redfin-data-county-with-pred_all`"
df_county = client.query(query).to_dataframe()

#convert county fips codes to string type to preserve leading 0
df_county.county_fips = df_county.county_fips.astype(str) #convert to string
df_county['county_fips'] = df_county['county_fips'].str.zfill(5)
#format data type for time
df_county['period_begin'] = pd.to_datetime(df_county['period_begin'], format="%Y/%m/%d").dt.date
df_county['period_end'] = pd.to_datetime(df_county['period_end'], format="%Y/%m/%d").dt.date

# lookup from state code to county_fips code
state_list = df_county[['state_code', 'county_fips']].drop_duplicates(subset = "state_code").sort_values(by="state_code")
state_list['county_fips'] = state_list['county_fips'].str[:2]
state_list.index = state_list['state_code']
state_list.drop('state_code', axis = 1, inplace=True)

#property types for drop down
property_set = list(set(df_county['property_type'].values.tolist()))

#metric types for dropdown
metric_set = ['median_sale_price', 'median_ppsf', 'median_sale_price_mom', 'median_ppsf_mom', 'covid_impact']

# a few global variables to track
settings_last = [property_set[0], metric_set[0], 0]
state_flag = True
state_num = '01'

#dates for slider
sorted_dates = np.sort(df_county['period_end'].unique())
sorted_dates = ['{}'.format(i) for i in sorted_dates] #convert each date to string within a list
counter = 0
year = 2012
slider_labels = {}
#labels for slider
for index, date in enumerate(sorted_dates[:-39]):
    if counter == index:
        slider_labels['{}'.format(index)] = str(year)
        year += 1
        counter += 12
    else: 
        slider_labels['{}'.format(index)] = ''

# labels = {index: date for index, date in enumerate(sorted_dates)} #labels of dates for slider object

#color-scale
color_scale = [[0.0, '#edf8fb'],[0.2, '#ccece6'],[0.4, '#99d8c9'],[0.6, '#66c2a4'],[0.8, '#2ca25f'],[1.0, '#006d2c']] # purples
color_scale3 = [[0.0, '#edf8e9'],[0.5, '#ffffb2'],[1.0, '#a50f15']] # stoplight

#-------------------------------#
#get geojson for counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties_geojson = json.load(response)
    
dash.register_page(__name__)


# ------------------------------------------------------------------------------
# App layout
#what goes inside dash layout are the dash components and any html we need
layout = html.Div(children=[

    html.H1("Real Estate Data by State (with Drilldown to County)", style={'text-align': 'center'}), #html Title

    html.Div(id='metric_title_drilldown', children=["Metric"], style = {'font-family':'sans-serif','font-weight': 'bold'}),

    #components, e.g., drop downs, sliders
    #first drop down by metric
    dcc.Dropdown(id="metric_drilldown",
                 placeholder = "Select Metric",
                 options=metric_set,
                 value=metric_set[0],
                 style={'width': "60%",}
                 ),

    html.Br(), #space between dropdowns

    html.Div(id='property_type_title_drilldown', style = {'font-family':'sans-serif','font-weight': 'bold'}, 
    children = ["Property Type"]
    ),

    #second drop down for property type
    dcc.Dropdown(id="property_type_drilldown",
                 placeholder = "Select Property Type",
                 options=property_set,
                 value=property_set[0],
                 style={'width': "60%"},
                 ),

    html.Br(), #space

    html.Button('Back to All States', id='back_to_all', n_clicks=0),

    html.Br(), #space
    
    #create div element, e.g., text to display dropdown selection
    html.Div(id='output_container_drilldown', children=[]),

    html.Br(), #space

    #graph object, e.g., choropleth
    dcc.Graph(id='choropleth_drilldown', figure={}), 

    #slider object
    dcc.Slider(0, len(sorted_dates[:-39]), step = None, #min value of 0 and max of number of unique dates
               value=0, #where the slider starts
               marks = slider_labels,
               tooltip={"placement": "bottom", "always_visible": True}, #place slider at bottom of graph
               id='date_chosen_drilldown')

])

#-------------------------------#

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    Output(component_id='output_container_drilldown', component_property='children'),
    Output(component_id='choropleth_drilldown', component_property='figure'),
    Input(component_id='property_type_drilldown', component_property='value'),
    Input(component_id='back_to_all', component_property='n_clicks'),
    Input(component_id = 'metric_drilldown', component_property = 'value'),
    Input(component_id='date_chosen_drilldown', component_property='value'),
    Input(component_id='choropleth_drilldown', component_property='clickData'))

def update_figure(property_type_drilldown, _, metric_drilldown, date_chosen_drilldown, clickData):

    global settings_last
    global state_flag
    global state_num
    global cased

    container = "Date Selected: {}".format(sorted_dates[date_chosen_drilldown])

    # if back button is pressed or 1st loading
    if "back_to_all" == ctx.triggered_id or clickData is None:
        dff = df_state.copy()
        dff = dff[['period_begin', 'period_end', 'state_code', 'median_sale_price', 'median_sale_price_mom', 
        'median_ppsf', 'median_ppsf_mom', 'property_type', 'covid_impact']]
        dff = dff[dff['property_type'] == property_type_drilldown]
        dff = dff[dff['period_end'] == pd.to_datetime(sorted_dates[date_chosen_drilldown], format="%Y/%m/%d")]

        fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='{}'.format(metric_drilldown),
        hover_data=['state_code', '{}'.format(metric_drilldown)],
        color_continuous_scale= color_scale3
        )
        state_flag = True

    # if a state is clicked
    elif clickData and state_flag and settings_last[0] == property_type_drilldown and settings_last[1] == metric_drilldown and settings_last[2] == date_chosen_drilldown:
        location = clickData['points'][0]['location']
        state_num = state_list.loc[location, 'county_fips']     
        
        dff = df_county.copy()
        dff = dff[['period_begin', 'period_end', 'region', 'median_sale_price', 'median_sale_price_mom', 
        'median_ppsf', 'median_ppsf_mom', 'property_type', 'county_fips', 'covid_impact']]
        dff = dff[dff['property_type'] == property_type_drilldown]
        dff = dff[dff['period_end'] == pd.to_datetime(sorted_dates[date_chosen_drilldown], format="%Y/%m/%d")]

        counties = counties_geojson.copy()
        counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] == state_num]

        fig = px.choropleth(
            data_frame = dff,
            geojson = counties,
            #featureidkey="id",
            locations='county_fips',
            scope="usa",
            color='{}'.format(metric_drilldown),
            hover_data=['region', '{}'.format(metric_drilldown)],
            color_continuous_scale= color_scale3
        )
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        fig.update_geos(fitbounds="locations") 

        state_flag = False

    # if a setting is changed on the county view
    elif clickData and not state_flag:    
        dff = df_county.copy()
        dff = dff[['period_begin', 'period_end', 'region', 'median_sale_price', 'median_sale_price_mom', 
        'median_ppsf', 'median_ppsf_mom', 'property_type', 'county_fips', 'covid_impact']]
        dff = dff[dff['property_type'] == property_type_drilldown]
        dff = dff[dff['period_end'] == pd.to_datetime(sorted_dates[date_chosen_drilldown], format="%Y/%m/%d")]

        counties = counties_geojson.copy()
        counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] == state_num]

        fig = px.choropleth(
            data_frame = dff,
            geojson = counties,
            #featureidkey="id",
            locations='county_fips',
            scope="usa",
            color='{}'.format(metric_drilldown),
            hover_data=['region', '{}'.format(metric_drilldown)],
            color_continuous_scale= color_scale3
        )
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        fig.update_geos(fitbounds="locations") 

    # if a setting is changed on the state view
    else:
        dff = df_state.copy()
        dff = dff[['period_begin', 'period_end', 'state_code', 'median_sale_price', 'median_sale_price_mom', 
        'median_ppsf', 'median_ppsf_mom', 'property_type', 'covid_impact']]
        dff = dff[dff['property_type'] == property_type_drilldown]
        dff = dff[dff['period_end'] == pd.to_datetime(sorted_dates[date_chosen_drilldown], format="%Y/%m/%d")]

        fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='{}'.format(metric_drilldown),
        hover_data=['state_code', '{}'.format(metric_drilldown)],
        color_continuous_scale= color_scale3
        )

    settings_last = [property_type_drilldown, metric_drilldown, date_chosen_drilldown]

    return container, fig

