import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/')

colors = {
    'background': '#111111',
    'text': '#111111'
}

markdown_steps = '''
## How to use this interective webapp:


* ** Home:** This is the current landing page with basic instructions and definitions of various metrics used in this webapp. 

* ** State:** This page will show a cloropleth with all the US states. There are two dropdowns to select Metric and property Types. Select any metric or property type you want to see in the cloropleth and corresponding line charts.There is a timeline slider below cloropleth that can be used to point to a year/month for which you want to see the state level metrics visulaized in cloropleth and line chart. Finally you can hover over the cloropleth chart to see pricing and state code along with its historical data in line chart. This page also has a legend to depict the visulaization colors against the chosen metric.

* ** Drilldowntocounty:** This page will show a cloropleth with all the US states. There are two dropdowns to select Metric and property Types. Select any metric or property type you want to see in the cloropleth and subsequently its counties. There is a timeline slider below cloropleth that can be used to point to a year/month for which you want to see the state level metrics visulaized in cloropleth. Finally you can click over any of the states in the chart to see county level metrics for that state. This page also has a legend to depict the visulaization colors against the chosen metric.

* ** Housepriceindex:** This page will show a cloropleth with all the US states. There is a timeline slider below cloropleth that can be used to point to a year for which you want to see the state level house prices indexes. You can hover over the cloropleth chart of states to see state code and house price index. Upon hover over the cloropleth chart of states it will also show line chart of predicted house price index for these states. This page also has a legend to depict the visulaization colors against the house price index.

* ** Housepriceindexcounty:** This page will show a cloropleth with all the US counties. There is a timeline slider below cloropleth that can be used to point to a year for which you want to see the county level house prices indexes.You can hover over the cloropleth chart of counties to see county name and house price index. Upon hover over the cloropleth chart of counties it will also show line chart of predicted house price index for these counties. This page also has a legend to depict the visulaization colors against the house price index.

'''

markdown_text = '''
## Definitions

* **Median Price Per Square Foot (PPSF):** The median price per square foot for a given US state or county and property type, over 3 months, ending on a chosen date, e.g., September 31st, 2016.

* ** Median Sale Price:**  The median sale price for a given US state or county and property type, over 3 months, ending on a chosen date, e.g., September 31st, 2016. 

* ** Housing Price Index:**  The average price changes in sales or refinancing for a given US state or county and property type for a chosen year, e.g., 1987, 
based on a tracked subset of chosen properties since 1975 for said US state or county.

* ** Median PPSF without COVID:**  The predicted median ppsf using a SARIMA model trained on median ppsf data up to 2020.

* ** Median PPSF with COVID:**  The predicted median ppsf using a SARIMA model trained on median ppsf data up to September 31st, 2022.

* ** Covid Impact:**  The change in Median PPSF with COVID with respect to Median PPSF without COVID as a percentage.

'''

markdown_team = '''
## Credits

* ** Team 182: Chaincoders **

        Michael Ho, Ramakrishna Bijanapalli, Michael Mow, Shashank Tripathi, Enrico Edwardo, Giang Duong

'''

layout = html.Div(children=[

    dcc.Markdown(children=markdown_steps),

    dcc.Markdown(children=markdown_text),
    
    dcc.Markdown(children=markdown_team),

    
  
])
