import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotting
import pyleoclim as pyleo
import os

# Load data
df = pd.read_csv('assets/all-data.csv', header=[0,1])    # stores data & age
df2 = pd.read_csv('assets/all-data2.csv', header=[0,1])  # stores name, variable and y_invert

app = dash.Dash(__name__) #, external_stylesheets=[dbc.themes.BOOTSTRAP]
server = app.server

app.layout = dbc.Container([ 
    html.Div(className='app-header', children=[
        html.H1("Meta Database Dashboard", className='display-3')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {'label':'LR04', 'value':'LR04'},
                    {'label':'Westerhold et al. (2020) - δ18O_b - CENOGRID Stack', 'value':'Westerhold et al. (2020) - δ18O_b - CENOGRID Stack'},
                    {'label':'PROBSTACK TUNED - Westerhold et al. (2020) - δ18O_b - CENOGRID Stack', 'value':'PROBSTACK TUNED - Westerhold et al. (2020) - δ18O_b - CENOGRID Stack'},
                    {'label':'Probstack', 'value':'Probstack'},
                    {'label':'Clark et al. (2025) - Probstack /wo trend', 'value':'Clark et al. (2025) - Probstack /wo trend'},
                    {'label':'Elderfield et al. (2012) - δ18O_b - ODP 1123', 'value':'Elderfield et al. (2012) - δ18O_b - ODP 1123'},
                    {'label':'PROBSTACK TUNED - Elderfield et al. (2012) - δ18O_b - ODP 1123', 'value':'PROBSTACK TUNED - Elderfield et al. (2012) - δ18O_b - ODP 1123'},
                    {'label':'Hodell et al. (2023) - δ18O_b - IODP U1385', 'value':'Hodell et al. (2023) - δ18O_b - IODP U1385'},
                    {'label':'PROBSTACK TUNED - Hodell et al. (2023) - δ18O_b - IODP U1385', 'value':'PROBSTACK TUNED - Hodell et al. (2023) - δ18O_b - IODP U1385'},
                    {'label':'Barker et al. (2022) - IODP U1476', 'value':'Barker et al. (2022) - IODP U1476'},
                    {'label':'PROBSTACK TUNED - Barker et al. (2022) - IODP U1476', 'value':'PROBSTACK TUNED - Barker et al. (2022) - IODP U1476'},
                    {'label':'Elderfield et al. (2012) - δ18O_sw - ODP 1123', 'value':'Elderfield et al. (2012) - δ18O_sw - ODP 1123'}, 
                    {'label':'Ford & Raymo (2019) - δ18O_sw - Stack (DSDP 607 + ODP 1123 + ODP 1208A)', 'value':'Ford & Raymo (2019) - δ18O_sw - Stack (DSDP 607 + ODP 1123 + ODP 1208A)'},
                    {'label':'PROBSTACK TUNED - Ford & Raymo (2019) - δ18O_sw - Stack (DSDP 607 + ODP 1123 + ODP 1208A)', 'value':'PROBSTACK TUNED - Ford & Raymo (2019) - δ18O_sw - Stack (DSDP 607 + ODP 1123 + ODP 1208A)'},
                    {'label':'Clark et al. (2025) - δ18O_sw - New Probstack (/wo trend) deconvolution', 'value':'Clark et al. (2025) - δ18O_sw - New Probstack (/wo trend) deconvolution'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2025) - δ18O_sw - New Probstack (/wo trend) deconvolution', 'value':'PROBSTACK TUNED - Clark et al. (2025) - δ18O_sw - New Probstack (/wo trend) deconvolution'},
                    {'label':'Hodell et al. (2023) - δ18O_p - IODP U1385', 'value':'Hodell et al. (2023) - δ18O_p - IODP U1385'},
                    {'label':'PROBSTACK TUNED - Hodell et al. (2023) - δ18O_p - IODP U1385', 'value':'PROBSTACK TUNED - Hodell et al. (2023) - δ18O_p - IODP U1385'},
                    {'label':'Westerhold et al. (2020) - δ13C_b - CENOGRID Stack', 'value':'Westerhold et al. (2020) - δ13C_b - CENOGRID Stack'},
                    {'label':'PROBSTACK TUNED - Westerhold et al. (2020) - δ13C_b - CENOGRID Stack', 'value':'PROBSTACK TUNED - Westerhold et al. (2020) - δ13C_b - CENOGRID Stack'},
                    {'label':'Elderfield et al. (2012) - δ13C_b - ODP 1123', 'value':'Elderfield et al. (2012) - δ13C_b - ODP 1123'},
                    {'label':'PROBSTACK TUNED - Elderfield et al. (2012) - δ13C_b - ODP 1123', 'value':'PROBSTACK TUNED - Elderfield et al. (2012) - δ13C_b - ODP 1123'},
                    {'label':'Hodell et al. (2023) - δ13C_p - IODP U1385', 'value':'Hodell et al. (2023) - δ13C_p - IODP U1385'},
                    {'label':'PROBSTACK TUNED - Hodell et al. (2023) - δ13C_p - IODP U1385', 'value':'PROBSTACK TUNED - Hodell et al. (2023) - δ13C_p - IODP U1385'},
                    {'label':'Clark et al. (2024) - Global Mean ΔSST stack', 'value':'Clark et al. (2024) - Global Mean ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - Global Mean ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - Global Mean ΔSST stack'},
                    {'label':'Clark et al. (2024) - North Atlantic ΔSST stack', 'value':'Clark et al. (2024) - North Atlantic ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - North Atlantic ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - North Atlantic ΔSST stack'},
                    {'label':'Clark et al. (2024) - Tropical Atlantic ΔSST stack', 'value':'Clark et al. (2024) - Tropical Atlantic ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - Tropical Atlantic ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - Tropical Atlantic ΔSST stack'},
                    {'label':'Clark et al. (2024) - South Atlantic ΔSST stack', 'value':'Clark et al. (2024) - South Atlantic ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - South Atlantic ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - South Atlantic ΔSST stack'},
                    {'label':'Clark et al. (2024) - North Pacific ΔSST stack', 'value':'Clark et al. (2024) - North Pacific ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - North Pacific ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - North Pacific ΔSST stack'},
                    {'label':'Clark et al. (2024) - Tropical Pacific ΔSST stack', 'value':'Clark et al. (2024) - Tropical Pacific ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - Tropical Pacific ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - Tropical Pacific ΔSST stack'},
                    {'label':'Clark et al. (2024) - South Pacific ΔSST stack', 'value':'Clark et al. (2024) - South Pacific ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - South Pacific ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - South Pacific ΔSST stack'},
                    {'label':'Clark et al. (2024) - Tropical ΔSST stack', 'value':'Clark et al. (2024) - Tropical ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2024) - Tropical ΔSST stack', 'value':'PROBSTACK TUNED - Clark et al. (2024) - Tropical ΔSST stack'},
                    {'label':'Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack', 'value':'Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack', 'value':'PROBSTACK TUNED - Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack'},
                    {'label':'Herbert et al. (2010) - Tropical ΔSST stack', 'value':'Herbert et al. (2010) - Tropical ΔSST stack'},
                    {'label':'PROBSTACK TUNED - Herbert et al. (2010) - Tropical ΔSST stack', 'value':'PROBSTACK TUNED - Herbert et al. (2010) - Tropical ΔSST stack'},
                    {'label':'Martínez‐García et al. (2011) - Fe MAR - ODP 1090', 'value':'Martínez‐García et al. (2011) - Fe MAR - ODP 1090'},
                    {'label':'Weber et al. (2022) - Fe MAR - IODP U1537', 'value':'Weber et al. (2022) - Fe MAR - IODP U1537'},
                    {'label':'Lamy et al. (2024) - Antarctic Circumpolar Current (ACC) strength - IODP U1540', 'value':'Lamy et al. (2024) - Antarctic Circumpolar Current (ACC) strength - IODP U1540'},
                    {'label':'Lamy et al. (2024) - Antarctic Circumpolar Current (ACC) strength - IODP U1541', 'value':'Lamy et al. (2024) - Antarctic Circumpolar Current (ACC) strength - IODP U1541'},
                    {'label':'Barker et al. (2022) - Ice Rafted Debris (IRD) - ODP 983', 'value':'Barker et al. (2022) - Ice Rafted Debris (IRD) - ODP 983'},
                    {'label':'Sun et al. (2019) - Magnetic Susceptibility (MS) - Jingyuan Loess', 'value':'Sun et al. (2019) - Magnetic Susceptibility (MS) - Jingyuan Loess'},
                    {'label':'Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess', 'value':'Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess', 'value':'PROBSTACK TUNED - Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess'},
                    {'label':'Sun et al. (2019) - Loess mean size - Jingyuan Loess', 'value':'Sun et al. (2019) - Loess mean size - Jingyuan Loess'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2019) - Loess mean size - Jingyuan Loess', 'value':'PROBSTACK TUNED - Sun et al. (2019) - Loess mean size - Jingyuan Loess'},
                    {'label':'Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess', 'value':'Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess', 'value':'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess'},
                    {'label':'Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess', 'value':'Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess', 'value':'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess'},
                    {'label': 'Ding et al. (2002) - Normalised mean loess size - Chiloparts stack','value': 'Ding et al. (2002) - Normalised mean loess size - Chiloparts stack'},
                    {'label': 'PROBSTACK TUNED - Ding et al. (2002) - Normalised mean loess size - Chiloparts stack','value': 'PROBSTACK TUNED - Ding et al. (2002) - Normalised mean loess size - Chiloparts stack'},
                    {'label': 'Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon', 'value': 'Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon'},
                    {'label': 'PROBSTACK TUNED - Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon', 'value': 'PROBSTACK TUNED - Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon'},
                    {'label':'Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid', 'value':'Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid'},
                    {'label': 'PROBSTACK TUNED - Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid','value': 'PROBSTACK TUNED - Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid'},                    
                    {'label':'Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value':'Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label': 'PROBSTACK TUNED - Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value': 'PROBSTACK TUNED - Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label':'Zhao et al. (2021) - Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value':'Zhao et al. (2021) - Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label': 'Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value': 'Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label': 'PROBSTACK TUNED - Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value': 'PROBSTACK TUNED - Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label':'Zhao et al. (2021) - Mean Temperature Warmest Month (MTWM) - Paleolake at Zoige Basin (Core ZB13-C2)', 'value':'Zhao et al. (2021) - Mean Temperature Warmest Month (MTWM) - Paleolake at Zoige Basin (Core ZB13-C2)'},
                    {'label':'Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)', 'value':'Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)'},
                    {'label':'PROBSTACK TUNED - Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)', 'value':'PROBSTACK TUNED - Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)'},
                    {'label':"Melles et al. (2012) - Magnetic Susceptibility (MS) - Lake El'gygytgyn", 'value':"Melles et al. (2012) - Magnetic Susceptibility (MS) - Lake El'gygytgyn"},
                    {'label':"Melles et al. (2012) - Total organic carbon content (TOC%) - Lake El'gygytgyn", 'value':"Melles et al. (2012) - Total organic carbon content (TOC%) - Lake El'gygytgyn"},
                    {'label':"Melles et al. (2012) - Si/Ti - Lake El'gygytgyn", 'value':"Melles et al. (2012) - Si/Ti - Lake El'gygytgyn"},
                    {'label':'Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal', 'value':'Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal'},
                    {'label':'PROBSTACK TUNED - Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal', 'value':'PROBSTACK TUNED - Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal'},
                    {'label':'Johnson et al. (2016) - Ca abundance - Lake Malawi', 'value':'Johnson et al. (2016) - Ca abundance - Lake Malawi'},
                    {'label':'Johnson et al. (2016) - Leaf wax δ13C in C31 - Lake Malawi', 'value':'Johnson et al. (2016) - Leaf wax δ13C in C31 - Lake Malawi'},
                    {'label': 'Johnson et al. (2016) - 5pt smooth Annual Lake Surface Temperature (ALST) - Lake Malawi', 'value':'Johnson et al. (2016) - 5pt smooth Annual Lake Surface Temperature (ALST) - Lake Malawi'},
                    {'label':'Johnson et al. (2016) - Annual Lake Surface Temperature (ALST) - Lake Malawi', 'value':'Johnson et al. (2016) - Annual Lake Surface Temperature (ALST) - Lake Malawi'},
                    {'label': 'Wang et al. (2025) - Mean Annual Temperature (MAT) - Paleolake Heqing', 'value': 'Wang et al. (2025) - Mean Annual Temperature (MAT) - Paleolake Heqing'},
                    {'label': 'PROBSTACK TUNED - Wang et al. (2025) - Mean Annual Temperature (MAT) - Paleolake Heqing', 'value': 'PROBSTACK TUNED - Wang et al. (2025) - Mean Annual Temperature (MAT) - Paleolake Heqing'},
                    {'label': 'Lu et al. (2022) - Mean Annual Temperature (MAT) - Lingtai Loess', 'value': 'Lu et al. (2022) - Mean Annual Temperature (MAT) - Lingtai Loess'},
                    {'label': 'Lu et al. (2022) - Mean Annual Surface Temperature (MAST) - Lingtai Loess', 'value': 'Lu et al. (2022) - Mean Annual Surface Temperature (MAST) - Lingtai Loess'},
                    {'label': 'PROBSTACK TUNED - Lu et al. (2022) - Mean Annual Surface Temperature (MAST) - Lingtai Loess', 'value': 'PROBSTACK TUNED - Lu et al. (2022) - Mean Annual Surface Temperature (MAST) - Lingtai Loess'},
                    {'label':'Sun et al. (2021) - Si/Sr - IODP U1308', 'value':'Sun et al. (2021) - Si/Sr - IODP U1308'},
                    {'label':'Sun et al. (2021) - Ca/K - Lake Ohrid', 'value':'Sun et al. (2021) - Ca/K - Lake Ohrid'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2021) - Ca/K - Lake Ohrid', 'value':'PROBSTACK TUNED - Sun et al. (2021) - Ca/K - Lake Ohrid'},
                    {'label':'Sun et al. (2021) - Loess mean size - Gulang Loess', 'value':'Sun et al. (2021) - Loess mean size - Gulang Loess'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2021) - Loess mean size - Gulang Loess', 'value':'PROBSTACK TUNED - Sun et al. (2021) - Loess mean size - Gulang Loess'},
                    {'label':'Sun et al. (2021) - Millenial Climate Variability (MCV) - MCV Stack', 'value':'Sun et al. (2021) - Millenial Climate Variability (MCV) - MCV Stack'},
                    {'label':'PROBSTACK TUNED - Sun et al. (2021) - Millenial Climate Variability (MCV) - MCV Stack', 'value':'PROBSTACK TUNED - Sun et al. (2021) - Millenial Climate Variability (MCV) - MCV Stack'},
                    {'label':'Jouzel et al. (2007) - EDC δD (AICC2023)', 'value':'Jouzel et al. (2007) - EDC δD (AICC2023)'},
                    {'label':'PROBSTACK TUNED - Jouzel et al. (2007) - EDC δD (AICC2023)', 'value':'PROBSTACK TUNED - Jouzel et al. (2007) - EDC δD (AICC2023)'},
                    {'label':'Bereiter et al. (2014) - Atmospheric CO2 - Composite Antarctic record', 'value':'Bereiter et al. (2014) - Atmospheric CO2 - Composite Antarctic record'},
                    {'label':'PROBSTACK TUNED - Bereiter et al. (2014) - Atmospheric CO2 - Composite Antarctic record', 'value':'PROBSTACK TUNED - Bereiter et al. (2014) - Atmospheric CO2 - Composite Antarctic record'},
                    {'label':'Yamamoto et al. (2022) - Atmospheric CO2 (δ13C leaf wax reconstr.) - IODP U1446', 'value':'Yamamoto et al. (2022) - Atmospheric CO2 (δ13C leaf wax reconstr.) - IODP U1446'},
                    {'label':'PROBSTACK TUNED - Yamamoto et al. (2022) - Atmospheric CO2 (δ13C leaf wax reconstr.) - IODP U1446', 'value':'PROBSTACK TUNED - Yamamoto et al. (2022) - Atmospheric CO2 (δ13C leaf wax reconstr.) - IODP U1446'},
                    {'label':'Clark et al. (2025) - Global Mean sea level (GMSL)', 'value':'Clark et al. (2025) - Global Mean sea level (GMSL)'},
                    {'label':'PROBSTACK TUNED - Clark et al. (2025) - Global Mean sea level (GMSL)', 'value':'PROBSTACK TUNED - Clark et al. (2025) - Global Mean sea level (GMSL)'},
                    # {'label':'', 'value':''},
                    # {'label':'', 'value':''},
                ], 
                value='LR04',           # default selection
                style={'width':'75%', 'margin-bottom':'1em'}
            ),
        ], width=8),
        dbc.Col([
            html.Label("Choose MIS boundaries: "),
            dcc.RadioItems( [
                                {'label': 'Lisiecki & Raymo (2005)', 'value': 'LR04'},
                                {'label': 'Tzedakis et al. (2017) method applied to Prob-stack', 'value': 'Prob-stack'},
                                {'label': 'Tzedakis et al. (2017) method applied to Prob-stack (only terminations = no glacial onsets)', 'value': 'Prob-stack2'}
                            ],
                            'Prob-stack',
                            id='mis-bounds-radio-items', inline=True, style={'margin-bottom':'1em'})
                ], width=12, className='bounds-dropdown'
            ),
        dbc.Col([
            dbc.Checkbox( 
                id="smooth-checkbox", 
                label="Smooth data (Whittaker-Eilers)", 
                value=False, # default unchecked 
                style={'margin-bottom':'1em'}
            ),
        ], width=4, className="dropdown"),
        dbc.Col([
            dcc.Input(id='range', type='number', min=0, max=2e4, step=0.1, placeholder=r"Input ƛ value", style={'width': '25%', 'margin-bottom':'1em'})
        ], width=4, className="range"),
        dbc.Col([
            html.Div(id='lambda-insights', className='lambda-insights', style={'margin-bottom':'2em'}),
        ]),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='single-plots'), style={'width':'95%'})  # width=12, 
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='data-insights', className='data-insights'),
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.Iframe(id='ig-table', style={"width": "100%", "height": "600px", "border": "none"})  # , "height": "600px", 
        ])
    ]),
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id='extrema-plots'), style={'width':'90%'}),  # width=12
    # ]),
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id='freq-plots'), style={'width':'90%'}),  # width=12,
    #     # dbc.Col(dcc.Graph(id='pyleo-plot'), style={'width':'30%'})  # width=12, 
    # ]),
    # # dbc.Row([
    # #     dbc.Col(dcc.Graph(id='pyleo-plot'), style={'width':'60%'})  # width=12, 
    # # ]),
    # dbc.Row([
    #     html.Img(id='pyleo-plot', alt='My Image', style={'width=':'20%', 'zoom':'30%'})
    #     ])
], fluid=True)

# Create Callbacks (Flask Route)
# Single Plot Callback -> Dropdown Input -> Show Plot Results  
@app.callback(
    Output('single-plots', 'figure'),
    Input('metric-dropdown', 'value'),
    Input('smooth-checkbox', 'value'),
    Input('range', 'value'),
    Input('mis-bounds-radio-items', 'value')
)
def update_plot(selected_metric, smooth, lam, bounds):
    print('lam=',lam)
    if selected_metric is None:
        return go.Figure()
        

    # Extract selected data
    age = df[(selected_metric, 'age')].to_numpy()
    data = df[(selected_metric, 'data')].to_numpy()
    y_invert = df2.loc[0, (selected_metric, 'y_invert')]
    # length = df.loc[0, (selected_metric, 'len')]

    age_probstack = df[('Probstack', 'age')].to_numpy()
    data_probstack = df[('Probstack', 'data')].to_numpy()
    y_invert_probstack = df2.loc[0, ('Probstack', 'y_invert')]
    
    if smooth:
        # store raw data
        age_raw = age
        data_raw = data

        # apply smoothing 
        age, data = plotting.smoothing(age_raw, data_raw, lam)

    # Calculate extrema
    data_input = np.array([
          [age, data, y_invert], 
       ], dtype=object)
    
    if bounds=='LR04':
        extrema = plotting.calc_extrema(data_input, plotting.mis_bounds)
    elif bounds=='Prob-stack':
        extrema = plotting.calc_extrema(data_input, np.hstack([0,plotting.bounds_probstack[:,1]]))
    elif bounds=='Prob-stack2':
        extrema = plotting.calc_extrema_only_terminations(data_input, plotting.bounds_probstack2)

    # Initialize figure
    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
            x=age_probstack,
            y=data_probstack,
            mode='lines',
            name="Probstack",
            line=dict(color='red', width=2)
        ), secondary_y=True)

    if smooth:
        # Add base line plot
        fig.add_trace(go.Scatter(
            x=age_raw,
            y=data_raw,
            mode='lines',
            name="Raw data",
            line=dict(color='blue', width=2)
        ), secondary_y=False)
        # Smoothed lines
        fig.add_trace(go.Scatter(
            x=age,
            y=data,
            mode='lines',
            name=selected_metric,
            line=dict(color='green', width=3)
        ), secondary_y=False)

    else:
        # Add base line plot
        fig.add_trace(go.Scatter(
            x=age,
            y=data,
            mode='lines',
            name=selected_metric,
            line=dict(color='blue', width=2)
        ), secondary_y=False)

    # Add extrema points
    if extrema[0].size > 0:
        fig.add_trace(go.Scatter(
            x=extrema[0][:, 0],
            y=extrema[0][:, 1],
            mode='markers',
            name='Extrema',
            marker=dict(size=10, color='purple', symbol='circle')
        ), secondary_y=False)

    # Add shaded MIS bounds (Not for bounds_probstack2!)
    # for start, end, label in plotting.bounds:
    if bounds=='LR04':
        mis_bounds = plotting.bounds
    elif bounds=='Prob-stack':
        mis_bounds = plotting.bounds_probstack
    elif bounds=='Prob-stack2':
        mis_bounds = plotting.bounds_probstack2

    if bounds=='LR04' or bounds=='Prob-stack':
        for start, end, label, state in mis_bounds:
            if state % 2 != 0:
                color = 'lightcoral' 

                if ((start+end)/2)<=1500:
                    if y_invert:
                        fig.add_trace(go.Scatter(
                            x=[(end+start)/2],
                            y=[0.95*np.nanmax(extrema[0][:,1])],
                            text=label,
                            mode="text",
                            showlegend=False,
                            textfont=dict(
                                size=14,         # Adjust font size here
                                # family="Arial",  # Optional: choose a font
                                # color="black"    # Optional: choose a color
                            )
                        ), secondary_y=False)
                    else:
                        fig.add_trace(go.Scatter(
                            x=[(end+start)/2],
                            y=[np.nanmax([0.95*np.nanmin(extrema[0][:,1]),1.05*np.nanmin(extrema[0][:,1])])],
                            text=label,
                            mode="text",
                            showlegend=False,
                            textfont=dict(
                                size=14,         # Adjust font size here
                                # family="Arial",  # Optional: choose a font
                                # color="black"    # Optional: choose a color
                            )
                        ), secondary_y=False)
            else:
                color = 'cornflowerblue'

                if ((start+end)/2)<=1500:
                    if y_invert:
                        fig.add_trace(go.Scatter(
                            x=[(end+start)/2],
                            y=[0.95*np.nanmin(extrema[0][:,1])],
                            text=label,
                            mode="text",
                            showlegend=False,
                            textfont=dict(
                                size=14,         # Adjust font size here
                                # family="Arial",  # Optional: choose a font
                                # color="black"    # Optional: choose a color
                            )
                        ), secondary_y=False)
                    else:
                        fig.add_trace(go.Scatter(
                            x=[(end+start)/2],
                            y=[np.nanmin([0.95*np.nanmax(extrema[0][:,1]),1.05*np.nanmax(extrema[0][:,1])])],
                            text=label,
                            mode="text",
                            showlegend=False,
                            textfont=dict(
                                size=14,         # Adjust font size here
                                # family="Arial",  # Optional: choose a font
                                # color="black"    # Optional: choose a color
                            )
                        ), secondary_y=False)

            fig.add_shape(
                type='rect',
                x0=start,
                x1=end,
                y0=0,
                y1=1,
                xref='x',
                yref='paper',
                fillcolor=color,
                opacity=0.5,
                layer='below',
                line_width=0
            )
    # Prob-stack2 bounds -. only draw vertial lines at glacial terminations
    else:
        terminations = np.hstack([0, plotting.bounds_probstack2[::2,1]])
        # Add vlines for each termination
        for t in terminations:
            fig.add_vline(x=t, line_color='black', line_dash='solid', line_width=2)


    # Apply layout
    fig.update_layout(
        margin=dict(r=0, t=40, l=0, b=40),
        title=dict(
            text=df2.loc[0, (selected_metric, 'name')],
            x=0.5,
            xanchor='center',
            font=dict(
                size=26,  # Set the font size for the title
                # color='blue',  # Optional: Set the font color
                # family='Arial' # Optional: Set the font family
            ) 
        ),
        xaxis=dict(title='Age (ka)', range=[0, 1500], showgrid=False),
        yaxis=dict(title=df2.loc[0, (selected_metric, 'variable')], showgrid=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="left",
            x=0.01
        )
    )

    # Reverse y-axis if needed
    fig.update_yaxes(title_text=df2.loc[0, ('Probstack', 'variable')], secondary_y=True)
    if df2.loc[0, (selected_metric, 'y_invert')]:
        fig.update_yaxes(autorange='reversed', secondary_y=False)

    # Secondary y-axis inverted (Probstack)
    if y_invert_probstack:
        fig.update_yaxes(autorange='reversed', secondary_y=True)

    return fig
    

# Average Resolution Callback -> Dropdown Input -> Show Average Resoltion
@app.callback(
    Output('data-insights', 'children'),
    Input('metric-dropdown', 'value')
)
def update_average_resolution(selected_metric):
    if selected_metric is None:
        return None

    # Extract selected data
    age = df[(selected_metric, 'age')].to_numpy()
    data = df[(selected_metric, 'data')].to_numpy()

    # Only use time interval 0 <=t <= 1.5 Ma
    mask = np.where(np.logical_and(0<=age,age<=1500))
    age = age[mask]

    # average resolution
    age_diff = np.diff(age, 1)
    age_av_res = np.mean(age_diff)
    age_max_res = np.max(age_diff)
    age_min_res = np.min(age_diff)

    insights = [
        html.Div([
            "For the time interval ",
            html.Span("0 - 1.5 Ma: ", style={"fontWeight": "bold"}),
            "Average resolution: ",
            html.Span(f"{age_av_res:.1f} kyr", style={"fontWeight": "bold"}),
            " | Max time step: ",
            html.Span(f"{age_max_res:.1f} kyr", style={"fontWeight": "bold"}),
            " | Min time step: ",
            html.Span(f"{age_min_res:.1f} kyr", style={"fontWeight": "bold"})
        ])
    ]

    # insights = [
    #     html.Div([
    #         "For the time interval: ",
    #         html.Span("0 - 1.5 Ma: ", style={"fontWeight": "bold"})
    #     ]),
    #     html.Ul([
    #         html.Li([
    #             "Average resolution: ",
    #             html.Span(f"{age_av_res:.1f} kyr", style={"fontWeight": "bold"})
    #     ]),
    #         html.Li([
    #             "Max time step: ",
    #             html.Span(f"{age_max_res:.1f} kyr", style={"fontWeight": "bold"})
    #     ]),
    #         html.Li([
    #             "Min time step: ",
    #             html.Span(f"{age_min_res:.1f} kyr", style={"fontWeight": "bold"})
    #     ]),

    #     ])
    # ]

    return insights

# update optimal lambda Callback -> Smoothing input -> Print optimal lambda
@app.callback(
    Output('lambda-insights', 'children'),
    Input('metric-dropdown', 'value'),
    Input('smooth-checkbox', 'value'),
    Input('range', 'value')
)
def update_optimal_lambda(selected_metric, smooth, lam):
    if selected_metric is None:
        return None
    if smooth is False:
        return None

    # Extract selected data
    age = df[(selected_metric, 'age')].to_numpy()
    data = df[(selected_metric, 'data')].to_numpy()
    
    if smooth:
        # apply smoothing 
        optimal_lambda = plotting.smoothing(age, data, lam, output=True)

    insights = [
        html.Div([
            "Optimal ƛ (or selected one): ",
            html.Span(f"{optimal_lambda:.3f}", style={"fontWeight": "bold"})
        ])
    ]

    return insights


# IG Table Callback -> Dropdown Input -> Show IG Strength Table
@app.callback(
    Output('ig-table', 'srcDoc'),
    Input('metric-dropdown', 'value'),
    Input('smooth-checkbox', 'value'),
    Input('range', 'value'),
    Input('mis-bounds-radio-items', 'value')
)
def update_IG_table(selected_metric, smooth, lam, bounds):
    if selected_metric is None:
        return None

    # Extract selected data
    age = df[(selected_metric, 'age')].to_numpy()
    data = df[(selected_metric, 'data')].to_numpy()
    y_invert = df2.loc[0, (selected_metric, 'y_invert')]

    if smooth:
        # apply smoothing 
        age, data = plotting.smoothing(age, data, lam)

    # Calculate extrema
    data_input = np.array([
          [age, data, y_invert], 
       ], dtype=object)
    

    if bounds=='LR04':
        extrema = plotting.calc_extrema(data_input, plotting.mis_bounds)
    elif bounds=='Prob-stack':
        extrema = plotting.calc_extrema(data_input, np.hstack([0,plotting.bounds_probstack[:,1]]))
    elif bounds=='Prob-stack2':
        extrema = plotting.calc_extrema_only_terminations(data_input, plotting.bounds_probstack2)

    df_IG, df_G, df_amplitude = plotting.create_dfs(df2, selected_metric, extrema, y_invert, bounds)

    # Create and style DataFrame
    html_string = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    margin: 0;
                    padding: 20px;
                    box-sizing: border-box;
                    width: 100%;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;  /* Full screen width */
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 4px 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #f0f0f0;
                }}
            </style>
        </head>
        <body>
            <h3 style="text-align: center;">Interglacial Strengths</h3>
            {df_IG.to_html(index=True)}
        </body>
        <body>
            <h3 style="text-align: center;">Glacial Strengths</h3>
            {df_G.to_html(index=True)}
        </body>
        <body>
            <h3 style="text-align: center;">Termination Strengths</h3>
            {df_amplitude.to_html(index=True)}
        </body>
        </html>
    """
    
    return html_string


# # Extrema Plots Callback
# @app.callback(
#     Output('extrema-plots', 'figure'),
#     Input('metric-dropdown', 'value'),
#     Input('smooth-checkbox', 'value'),
#     Input('range', 'value'),
#     Input('mis-bounds-radio-items', 'value')
# )
# def update_extrema_plot(selected_metric, smooth, lam, bounds):
#     if selected_metric is None:
#         return go.Figure()

#     # Extract selected data
#     age = df[(selected_metric, 'age')].to_numpy()
#     data = df[(selected_metric, 'data')].to_numpy()
#     y_invert = df2.loc[0, (selected_metric, 'y_invert')]
    
#     if smooth:
#         # store raw data
#         age_raw = age
#         data_raw = data

#         # apply smoothing 
#         age, data = plotting.smoothing(age_raw, data_raw, lam)

#     # Calculate extrema
#     data_input = np.array([
#           [age, data, y_invert], 
#        ], dtype=object)

#     # calculate extrema    
#     if bounds=='LR04':
#         extrema = plotting.calc_extrema(data_input, plotting.mis_bounds)
#     elif bounds=='Prob-stack':
#         extrema = plotting.calc_extrema(data_input, np.hstack([0,plotting.bounds_probstack[:,1]]))
#     elif bounds=='Prob-stack2':
#         extrema = plotting.calc_extrema_only_terminations(data_input, plotting.bounds_probstack2)

#     # get ids of IGs and Gs
#     extrema_IGs_id = np.where(extrema[0,:,2]==1)[0]
#     extrema_Gs_id = np.where(extrema[0,:,2]==0)[0]

#     # get IG and G extrema seperately
#     extrema_IGs = extrema[0][extrema_IGs_id,:2]
#     extrema_Gs = extrema[0][extrema_Gs_id,:2]

#     if np.nanmax(age) < 1000:
#         return go.Figure()

#     # Initialize figure
#     fig = make_subplots(rows=1, cols=3, subplot_titles=[f'Interglacial extrema', 'Glacial extrema', 'Termination amplitude'])

#     fig.add_trace(go.Scatter(
#         # x=extrema[0][0::2, 0],
#         # y=extrema[0][0::2, 1],
#         x=extrema_IGs[:,0], 
#         y=extrema_IGs[:,1], 
#         mode='markers',
#         name='Interglacial extrema',
#         marker=dict(size=10, color='red', symbol='circle')
#         ), row=1, col=1
#     )

#     fig.add_trace(go.Scatter(
#         # x=extrema[0][1::2, 0],
#         # y=extrema[0][1::2, 1],
#         x=extrema_Gs[:,0], 
#         y=extrema_Gs[:,1], 
#         mode='markers',
#         name='Glacial extrema',
#         marker=dict(size=10, color='blue', symbol='circle')
#         ), row=1, col=2
#     )

#     fig.add_trace(go.Scatter(
#         x=(np.absolute(extrema_Gs[:,0]+extrema_IGs[:-1,0]))/2, 
#         y=np.absolute(extrema_Gs[:,1]-extrema_IGs[:-1,1]), 
#         mode='markers',
#         name='Termination amplitude',
#         marker=dict(size=10, color='purple', symbol='circle')
#         ), row=1, col=3
#     )

#     # Apply layout
#     fig.update_layout(
#         margin=dict(r=0, t=40, l=0, b=40),
#         title=dict(
#             text=df2.loc[0, (selected_metric, 'name')],
#             x=0.5,
#             xanchor='center',
#             font=dict(
#                 size=26,  # Set the font size for the title
#                 # color='blue',  # Optional: Set the font color
#                 # family='Arial' # Optional: Set the font family
#             )
#         ),
#         # xaxis=dict(title='Period (kyr)', showgrid=True),
#         # yaxis=dict(title=df2.loc[0, (selected_metric, 'variable')], showgrid=False),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=-0.2,
#             xanchor="left",
#             x=0
#         )
#     )
#     # Update x/y labels 
#     fig.update_xaxes(title_text="Age (ka)")
#     fig.update_yaxes(title_text=df2.loc[0, (selected_metric, 'variable')])

#     # Reverse y-axis if needed
#     if df2.loc[0, (selected_metric, 'y_invert')]:
#         fig.update_yaxes(autorange='reversed', row=1, col=1)
#     else:
#         fig.update_yaxes(autorange='reversed', row=1, col=2)


#     return fig

# # LombScargle Plots Callback
# @app.callback(
#     Output('freq-plots', 'figure'),
#     Input('metric-dropdown', 'value'),
#     Input('smooth-checkbox', 'value'),
#     Input('range', 'value')
# )
# def update_freq_plot(selected_metric, smooth, lam):
#     if selected_metric is None:
#         return go.Figure()

#     # Extract selected data
#     age = df[(selected_metric, 'age')].to_numpy()
#     data = df[(selected_metric, 'data')].to_numpy()

#     if smooth:
#         # apply smoothing 
#         age, data = plotting.smoothing(age, data, lam)

#     if np.nanmax(age) < 1000:
#         return go.Figure()

#     # LombScargle 
#     (f_LombScargle_postMPT, P_LombScargle_postMPT), (f_LombScargle_preMPT, P_LombScargle_preMPT) = plotting.calc_lombscargle(age, data)

#     # Initialize figure
#     fig = make_subplots(rows=1, cols=2, subplot_titles=[f'Pre MPT: 1 Ma - {np.min([np.nanmax(age),1500])*1e-3:.1f} Ma', 'Post MPT: 800 ka - 0 ka'])

#     if selected_metric!='LR04':
#         (f_LombScargle_postMPT_LR04, P_LombScargle_postMPT_LR04), (f_LombScargle_preMPT_LR04, P_LombScargle_preMPT_LR04) = plotting.calc_lombscargle(df[('LR04','age')], df[('LR04','data')])

#         fig.add_trace(go.Scatter(
#             x=1/f_LombScargle_preMPT_LR04,
#             y=P_LombScargle_preMPT_LR04,
#             mode='lines',
#             showlegend=False,
#             line=dict(color='blue', width=2)
#             ), row=1, col=1
#         )

#         fig.add_trace(go.Scatter(
#             x=1/f_LombScargle_postMPT_LR04,
#             y=P_LombScargle_postMPT_LR04,
#             mode='lines',
#             name='LR04',
#             line=dict(color='blue', width=2),
#             ), row=1, col=2
#         )

#     # Pre MPT Plot
#     fig.add_trace(go.Scatter(
#         x=1/f_LombScargle_preMPT,
#         y=P_LombScargle_preMPT,
#         mode='lines',
#         showlegend=False,
#         line=dict(color='orange', width=2)
#         ), row=1, col=1
#     )
#     for orb_freq in [100, 41, 23]:
#         fig.add_vline(x=orb_freq, line_dash="dash", line_color="grey")

#     # Post MPT Plot
#     fig.add_trace(go.Scatter(
#         x=1/f_LombScargle_postMPT,
#         y=P_LombScargle_postMPT,
#         mode='lines',
#         name=selected_metric,
#         line=dict(color='orange', width=2),
#         ), row=1, col=2
#     )
#     for orb_freq in [100, 41, 23]:
#         fig.add_vline(x=orb_freq, line_dash="dash", line_color="grey")

#     # Apply layout
#     fig.update_layout(
#         margin=dict(r=0, t=40, l=0, b=40),
#         title=dict(
#             text=df2.loc[0, (selected_metric, 'name')],
#             x=0.5,
#             xanchor='center',
#             font=dict(
#                 size=26,  # Set the font size for the title
#                 # color='blue',  # Optional: Set the font color
#                 # family='Arial' # Optional: Set the font family
#             ) 
#         ),
#         # xaxis=dict(title='Period (kyr)', showgrid=True),
#         # yaxis=dict(title=df2.loc[0, (selected_metric, 'variable')], showgrid=False),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=-0.2,
#             xanchor="left",
#             x=0
#         )
#     )
#     # Update x/y labels 
#     fig.update_xaxes(title_text="Period (kyr)")
#     fig.update_yaxes(title_text="Spectral power (a.u.)")

#     return fig


# # PyleoCLim Plot Callback
# @app.callback(
#     Output('pyleo-plot', 'src'),
#     Input('metric-dropdown', 'value'),
#     Input('smooth-checkbox', 'value'),
#     Input('range', 'value')
# )
# def update_pyleo_plot(selected_metric, smooth, lam):
#     if selected_metric is None:
#         return ''

#     # Extract selected data
#     age = df[(selected_metric, 'age')].to_numpy()
#     data = df[(selected_metric, 'data')].to_numpy()
#     y_invert = df2.loc[0, (selected_metric, 'y_invert')]
#     name = df2.loc[0,(selected_metric, 'name')]
#     variable = df2.loc[0,(selected_metric, 'variable')]

#     if smooth:
#         # apply smoothing 
#         age, data = plotting.smoothing(age, data, lam)

#     # only use past 1.5 Ma
#     mask = age <= 1500
#     age = age[mask]
#     data = data[mask]

#     # create figure with pyleoclim
#     file_path = plotting.pyleo_plot(age, data, y_invert, variable, name)

#     return file_path


# # Delete old scalograms
# @app.callback(
#     Input('metric-dropdown', 'value')
# )
# def delete_old_plots(selected_metric):
    print('Delte function called...')
    for fname in os.listdir('assets/'):
        if fname.startswith("pyleo_plot"):
            print(f'... deltes followig file: assets/{fname}')
            os.remove(os.path.join('assets/', fname))


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=False) #, dev_tools_hot_reload=False
