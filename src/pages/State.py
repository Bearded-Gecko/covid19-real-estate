import dash
from dash import Dash, dcc, html, Input, Output, callback
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

credentials = service_account.Credentials.from_service_account_file(
'./chain-coders-5d47d58b2c33.json')

project_id = 'chain-coders'
client = bigquery.Client(credentials= credentials,project=project_id)
query = "SELECT * FROM `redfin.redfin-data-state-with-predictions2`"
df = client.query(query).to_dataframe()


# -- Import and clean data (importing csv into pandas)
#df = pd.read_csv("state_market_tracker.csv")

#format data type for time
#df['period_begin'] = pd.to_datetime(df['period_begin'], format="%m/%d/%Y").dt.date
#df['period_end'] = pd.to_datetime(df['period_end'], format="%m/%d/%Y").dt.date


#format data type for time
df['period_begin'] = pd.to_datetime(df['period_begin'], format="%Y/%m/%d").dt.date
df['period_end'] = pd.to_datetime(df['period_end'], format="%Y/%m/%d").dt.date


#property types for drop down
#property_set = list(set(df['property_type'].values.tolist()))

property_set = ['Multi_Family' ,  "All_Residential" , "Townhouse" ,"Condo", "Single_Family_Residential"]
property_dict ={4:'Multi_Family' , -1 : "All_Residential" , 13:"Townhouse" , 3:"Condo", 6:"Single_Family_Residential"}
property_rev_dict ={'Multi_Family':4 , "All_Residential":-1 , "Townhouse":13 , "Condo":3, "Single_Family_Residential":6}

#metric types for dropdown
metric_set = ['median_sale_price', 'median_ppsf', 'median_sale_price_mom', 'median_ppsf_mom', 'median_ppsf_without_covid', 'median_ppsf_with_covid','covid_impact']

#dates for slider
sorted_dates = np.sort(df['period_end'].unique())
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
            
#color-scale
color_scale = [[0.0, '#edf8fb'],[0.2, '#ccece6'],[0.4, '#99d8c9'],
       [0.6, '#66c2a4'],[0.8, '#2ca25f'],[1.0, '#006d2c']] # purples

color_scale2 = [[0.0, '#31a354'],[0.5, '#f8f000'],[1.0, '#fee5d9']] # stoplight
color_scale3 = [[0.0, '#edf8e9'],[0.5, '#ffffb2'],[1.0, '#a50f15']] # stoplight
color_scale4 = [[0.0, '#bae4b3'],[0.5, '#ffffb2'],[1.0, '#a50f15']] # stoplight
#-------------------------------#


dash.register_page(__name__)

# ------------------------------------------------------------------------------
# App layout
#what goes inside dash layout are the dash components and any html we need
layout = html.Div(children=[

    html.H2("Real Estate Data By State", style={'font-family':'sans-serif','text-align': 'center'}), #html Title

    html.Div(id='metric_title', children=["Metric"], style = {'font-family':'sans-serif','font-weight': 'bold'}),

    #components, e.g., drop downs, sliders
    #first drop down by metric
    dcc.Dropdown(id="metric",
                 placeholder = "Select Metric",
                 options=metric_set,
                 value=metric_set[0],
                 style={'width': "60%",}
                 ),

    html.Br(), #space between dropdowns

    html.Div(id='property_title', style = {'font-family':'sans-serif','font-weight': 'bold'}, children = ["Property Type"]),

    #second drop down for property type
    dcc.Dropdown(id="property_type",
                 placeholder = "Select Property Type",
                 options=property_set,
                 value=property_set[0],
                 style={'width': "60%"},
                 ),

    html.Br(), #space
    
    #create div element, e.g., text to display dropdown selection
    html.Div(id='output_container', children=[]),

    html.Br(), #space

    #graph object, e.g., choropleth
    dcc.Graph(id='choropleth', figure={}), 

    #slider object
    dcc.Slider(0, len(sorted_dates[:-39]), step = None, #min value of 0 and max of number of unique dates
               value=0, #where the slider starts
               marks = slider_labels,
               tooltip={"placement": "bottom", "always_visible": True}, #place slider at bottom of graph
               id='date_chosen'),
    
    #add line chart
    dcc.Graph(id = "line_chart", figure = {})
])
#-------------------------------#

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    Output(component_id='output_container', component_property='children'),
    Output(component_id='choropleth', component_property='figure'),
    Output(component_id= 'line_chart', component_property = 'figure'),
    Input(component_id='property_type', component_property='value'),
    Input(component_id = 'metric', component_property = 'value'),
    Input(component_id='date_chosen', component_property='value'),
    Input(component_id = 'choropleth', component_property = 'hoverData'))


def update_graph(property_type, metric, date_chosen, hover):
    # print(property_type)
    # print(type(property_type))

    container = "Date Selected: {}".format(sorted_dates[date_chosen])

    df['period_end'] = pd.to_datetime(df['period_end'] )
    df_sorted = df.sort_values('period_end',ascending = True)
    
    dff = df_sorted.copy()
    df2 = df_sorted.copy()
    dff = dff[['period_begin', 'period_end', 'state_code', 'median_sale_price', 'median_sale_price_mom', 
    'median_ppsf', 'median_ppsf_mom', 'property_type_id','median_ppsf_without_covid', 'median_ppsf_with_covid', 'covid_impact']]
    dff = dff[dff['property_type_id'] == property_rev_dict[property_type]]
    dff = dff[dff['period_end'] == pd.to_datetime(sorted_dates[date_chosen], format="%Y/%m/%d")]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='{}'.format(metric),
        hover_data=['state_code', '{}'.format(metric)],
        color_continuous_scale= color_scale3 #deep#color_scale2#'portland    
        )
    

    line_data = px.line(df2, x = "period_end", y = [])
    if type(hover) == dict:
        hover_state = hover['points'][0]['customdata'][0]
        
        hover_df = df2[(df2['property_type_id'] == property_rev_dict[property_type]) & (df2['state_code'] == hover_state)]
        # print(hover_df["period_end"])

        line_data = px.line(hover_df, x = "period_end", y = ["median_ppsf_without_covid", "median_ppsf_with_covid"])
        
        line_data.update_layout(
            title='Predicted Median Prices per SqFt modelled with and without Covid-19 for {fstate}'.format(fmetric = metric, fstate = hover_state),
            xaxis_title="Year",
            yaxis_title="Median PPSF ($) ",
            legend_title="Models",
            font=dict(
                family="Courier New, monospace",
                size=18,
            )
)

    return container, fig, line_data