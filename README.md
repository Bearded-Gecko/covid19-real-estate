# DVA Project



## DESCRIPTION - Describe the package in a few paragraphs

The package is a docker setup built of a python 3.7 base. 
The image is built around python libraries for plotting , machine learning , visualization and running webserver
We have used Plotly and matplot for choropleths/line chart interactive visualizations. Additionally statsmodel and 
Scikitlearn is used for ML models ( prediction and evaluations)
Dash and Flask are used for python webserver.
Python libraries to access GCP - Google Big Query 
We developed our application using conda environment in Jupyter lab.
The package contains the source folder(DVAProject/src) that has the required python scripts to run the webserver along with visualizations.
It has also has Jupyter notebooks that was used for running the Machine Learning models to predict the house prices.




## INSTALLATION - How to install and setup your code

Unzip DVAProject.zip and navigate to DVAProject folder on terminal. 

Run below commands on terminal

docker build -t proto_image .

docker run --name dva_env_c1 -v <local path to your DVAProject>/dva_env:/dva_env -w /dva_env -p 8888:8888 proto_image

Navigate to src folder on terminal and run - python app.py . This will bring up the DASH server and you should be 
    able to access the webapplication using this url - http://0.0.0.0:8050/

## EXECUTION - How to run a demo on your code
 Navigate to this url - http://0.0.0.0:8050/ in your browser
    By default you will navigate to landing page/home page of the application. This page provides basic definitions of the 
    metrics used in the project. From home page you will also see a menu to navigate to other pages. Below are the pages
    you can navigate to.
    
    1.State - This page will show a cloropleth with all the US states. There are two dropdowns to select Metric and property     Types. Select any metric or property type you want to see in the cloropleth and corresponding line charts.There is a         timeline slider below cloropleth that can be used to point to a year/month for which you want to see the state level 
    metrics visulaized in cloropleth and line chart. Finally you can hover over the cloropleth chart to see pricing and 
    state code along with its historical data in line chart. This page also has a legend to depict the visulaization colors 
    against the chosen metric.
    
    2.Drilldowntocounty - This page will show a cloropleth with all the US states. There are two dropdowns to select Metric 
    and property Types. Select any metric or property type you want to see in the cloropleth and subsequently its counties. 
    There is a timeline slider below cloropleth that can be used to point to a year/month for which you want to see the 
    state level metrics visulaized in cloropleth. Finally you can click over any of the states in the chart to see county 
    level metrics for that state. This page also has a legend to depict the visulaization colors against the chosen metric.


    
    3.Housepriceindex - This page will show a cloropleth with all the US states. There is a timeline slider below cloropleth 
    that can be used to point to a year for which you want to see the state level house prices indexes. You can hover over 
    the cloropleth chart of states to see state code and house price index. Upon hover over the cloropleth chart of states 
    it will also show line chart of predicted house price index for these states. This page also has a legend to depict the 
    visulaization colors against the house price index.
    
    
       
    4.Housepriceindexcounty - This page will show a cloropleth with all the US counties. There is a timeline slider below 
    cloropleth that can be used to point to a year for which you want to see the county level house prices indexes.You can 
    hover over the cloropleth chart of counties to see county name and house price index. Upon hover over the cloropleth 
    chart of counties it will also show line chart of predicted house price index for these counties. This page also has a 
    legend to depict the visulaization colors against the house price index.
     

## DEMO VIDEO - https://www.youtube.com/watch?v=pIQIaSKqCxw


## Members

Shashank, Giang, Mike, Michael, Rama, Enrico



