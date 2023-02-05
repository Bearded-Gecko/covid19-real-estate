from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SIMPLEX])



app.layout = html.Div([
    html.H1('Impact of Covid-19 Pandemic on Real Estate', style={'font-family':'sans-serif','text-align': 'center'}),
    

    html.Div(
        [
                dcc.Link(
                    f"\t|\t{page['name']} \t |\t ", href=page["relative_path"] 
                )
            
            for page in dash.page_registry.values()
        ] , style={'font-family':'sans-serif','text-align': 'center'}
    ),
    
    dash.page_container

])

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port=8050, debug=True)