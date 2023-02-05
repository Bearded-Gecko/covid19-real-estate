import math
import json
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account
from urllib.request import urlopen

from datetime import datetime

class BigQuery():
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file('./chain-coders-5d47d58b2c33.json')
        project_id = 'chain-coders'
        self.client = bigquery.Client(credentials= credentials,project=project_id)

        datasets = self.client.list_datasets()
        for dataset in datasets:
            self.did = dataset.dataset_id
            # Optional to verify that you are able to access the datasets.
            print(self.did)
        
    def createDF(self,query):
        
        self.df = self.client.query(query).to_dataframe()
        self.regions = self.df.region.unique()
        self.property_types = self.df.property_type_id.unique()
        
    
    def filterRegion(self, region, ptype):
        
        mask1 = self.df['region'] == region
        mask2 = self.df['property_type_id'] == ptype
    
        df_filtered = self.df[mask1 & mask2]
        df_filtered = df_filtered.set_index('period_end').sort_values(by=['period_end'])
        df_filtered.index = pd.to_datetime(df_filtered.index)
        df_filtered.index = df_filtered.index.to_period('M')
        return df_filtered
    
    
    def addColumn(self):
        pass
    
    
    