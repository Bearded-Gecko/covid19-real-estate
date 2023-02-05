FROM python:3.7
LABEL maintainer="bcrama" 
LABEL version="1.0" 
LABEL description="docker image for dva project development env"  
RUN pip install --upgrade pip 
RUN pip install jupyter numpy pandas matplotlib statsmodels tensorflow scikit-learn plotly dash google-cloud-bigquery[pandas] click flash jupyterlab pmdarima
EXPOSE 8050 8070 8080 8888 
SHELL ["/bin/bash", "-ec"]
CMD [ "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root" ]