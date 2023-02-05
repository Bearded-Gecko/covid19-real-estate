import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import matplotlib.dates as dates
import random
import json
import pandas as pd
import numpy as np
import requests
from bigQuery import BigQuery

class Visualize():
    
    def __init__(self):
        
        
        #color-scale
        self.color_scale = [[0.0, '#DAF7A6'],[0.2, '#FFC300'],[0.4, '#FF5733'],[0.6, '#C70039'],[0.8, '#900C3F'],[1.0, '#581845']] 
    
    def createSlider(self, df):
        
        self. data_slider = []
        for date in sorted_dates:
            df_segmented =  df[(df['period_end']== date)]

        #for col in df_segmented.columns:
            #df_segmented[col] = df_segmented[col].astype(str)

        data_each_date = dict(
                            type='choropleth',
                            showlegend = False,
                            locations = df_segmented['state_code'],
                            z=df_segmented['median_ppsf'].astype(float), #choropleth value-to-color mapping set in 'z'
                            locationmode='USA-states',
                            colorscale = color_scale,
                            colorbar= {'title':'Median Sale Prices'})

        self.data_slider.append(data_each_date)
        
class Visualize2():

    def __init__(self):
        
        self.r = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
        self.df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv', dtype={'fips': str})
        
        
        self.fig = self.updateState(['1','14','42'])
        self.fig.show()

        # Keep track of the clicked region by using the variable "selections" 
        self.selections = set()

    def updateState(self, target_states = ['36']):
        print (target_states)
        
        self.counties = json.loads(self.r.text)
        self.counties['features'] = [f for f in self.counties['features'] if f['properties']['STATE'] in target_states]
        
        self.fig = px.choropleth(
                            self.df, 
                            geojson=self.counties, 
                            locations='fips', 
                            color='unemp',
                            color_continuous_scale='Viridis',
                            range_color=(0, 12),
                            scope='usa',
                            labels={'unemp': 'unemployment rate'}
                            )
        
        self.fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        self.fig.update_geos(fitbounds="locations") 
        return self.fig
    
class Visualize3():

    def __init__(self):
        
        
        bq = BigQuery()
        query = "SELECT * FROM `redfin.redfin-data-state` "
        bq.createDF(query)
        
        self.df_state = bq.df[['period_end','property_type_id','median_ppsf' ,'state_code' ]]
        
        self.sorted_dates = np.sort(self.df_state['period_end'].unique())

        
        data_slider = []
        for date in self.sorted_dates:
            df_segmented =  self.df_state[(self.df_state['period_end']== date)]

            #for col in df_segmented.columns:
            #    df_segmented[col] = df_segmented[col].astype(str)

            data_each_date = dict(
                                type='choropleth',
                                showlegend = False,
                                locations = df_segmented['state_code'],
                                z=df_segmented['median_ppsf'].astype(float), #choropleth value-to-color mapping set in 'z'
                                locationmode='USA-states',
                                colorscale = 'Sunset',
                                colorbar= {'title':'Median Sale Prices'})

            data_slider.append(data_each_date)
            
            #builds the actual slider object
            steps = []
            for i in range(len(data_slider)):
                step = dict(method='restyle',
                            args=['visible', [False] * len(data_slider)],
                            label='{}'.format(self.sorted_dates[i]))
                step['args'][1][i] = True
                steps.append(step)

            sliders = [dict(active=0, pad={"t": 1}, steps=steps)]
            
            layout = dict(
                title ='Median Sale Prices in US (2012 - 2022)',
                geo=dict(scope='usa',projection={'type': 'albers usa'}),
                sliders=sliders)
            
            self.fig = dict(data=data_slider, layout=layout)
            pio.show(self.fig)


    def updateState(self, target_states = ['36']):
        print (target_states)
        
        self.counties = json.loads(self.r.text)
        self.counties['features'] = [f for f in self.counties['features'] if f['properties']['STATE'] in target_states]
        
        self.fig = px.choropleth(
                            self.df, 
                            geojson=self.counties, 
                            locations='fips', 
                            color='unemp',
                            color_continuous_scale='Viridis',
                            range_color=(0, 12),
                            scope='usa',
                            labels={'unemp': 'unemployment rate'}
                            )
        
        self.fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        self.fig.update_geos(fitbounds="locations") 
        return self.fig