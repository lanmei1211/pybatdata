# -*- coding: utf-8 -*-
# System and Standard Libraries
import base64
import datetime
import io
import re
from copy import deepcopy

# Dash Python - HTML Interface Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import pandas as pd

# Dash Python - My HTML Interface
from src.dashsetup.header import Header
from src.dashsetup.body import *
from src.dashsetup.footpage import FootPage
# Functions and Plots
from src.dashsetup.plot2D import plot2D
from src import *
# IO code
from src.iobat.test_file import get_csv

# Dash External Style Import
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Global variables
file = []
last_n_clicks = 0
last_radio = 'Differential Voltage Analysis (DVA)'

# Main Layout
app.layout = html.Div(
    style={'width': '100%', 'height': '100%',
        'backgroundColor': colors['background'],
        'backgroundImage': 'url(https://i.redd.it/ev89ehtc0o2x.png)'
    }, 
    children=[
        # Header Layout
        Header(),

        # Body Layout
        BodyIntro(),
        Body(),
        
        # Footpage Layout
        FootPage(),
    ]
)

# Callbacks (interactive parts of the interface)
###################
# Load a file
###################
@app.callback(Output(component_id='output-data-upload', component_property='children'),
                  [Input(component_id='upload-data', component_property='contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
def file_callback(list_of_contents, list_of_names, list_of_dates):
    print(len(list_of_dates))
    print(type(list_of_contents))
#    print('names=',list_of_names)
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        global file
        file = get_csv(list_of_contents[0], list_of_names[0], list_of_dates[0])

        return children 

########################
# Selection of analysis
########################
@app.callback(Output(component_id='analysis-radio',component_property='children'),
                [Input(component_id='analysis-dropdown',component_property='value')],
                [State('type-radioitems','value')],
                [Event('type-radioitems','change')])
def dropdown_callback(value,radio):
    global last_radio
    if last_radio != value:
        last_radio = value
        print('dropdown select:', value, '\n')

    if value == 'Coulombic Efficiency (CE)':
        return Select_Analysis_Radio(False,'A')
    elif value == 'Differential Voltage Analysis (DVA)':
        return Select_Analysis_Radio(False,'A')
    else:
        return Select_Analysis_Radio(True,radio)
    
###################
# Cycle selection
###################
# Function used to interpret the input
def regex_format(text):
    formated = ''
    for c in text:
        if c == '-' and len(formated) > 0 and formated[-1].isdigit():
            formated += c
        elif c == ',' and len(formated) > 0 and formated[-1].isdigit():
            formated += c
        elif re.match('\d',c) != None:
            formated += c
    print(formated)
    return formated

@app.callback(Output(component_id='cycles-select',component_property='children'),
                [Input(component_id='cycles-input',component_property='value')],
                [],
                [])
def cycles_callback(input_):
    formated = regex_format(deepcopy(input_))

    if re.match("^\s*$",input_) != None:
        return 'Selected Cycles = Empty'
    if re.match("^([\d]+\s*[\,\-]{0,1}\s*)+$",input_) != None:
        return 'Selected Cycles = ',formated
    else:
        return 'Selected Cycles = Invalid Format'

###################
# Plot
###################
def plot_callback(dropdown,title,xlabel,ylabel,cycles,mode):
    global file
    if dropdown == 'Coulombic Efficiency (CE)':
        print('Coulombic Efficiency (CE)')
        return src.coulombic_efficiency(file,title,xlabel,ylabel)
    elif dropdown == 'Differential Voltage Analysis (DVA)':
        print('Differential Voltage Analysis (DVA)')
        return src.DVA(file,title,xlabel,ylabel,cycles)
    elif dropdown != '':
        print(dropdown)
        if mode == 'D':
            mode = -1
        elif mode == 'C':
            mode = 1
        else:
            mode = 0
        return src.dashsetup.plot2D(dropdown,file,title,xlabel,ylabel,cycles,mode)

def cycletolist(formated):
    # 0. Variables
    i = 0
    number = ''
    cycles = []

    while i < len(formated):
        # 1. Reading the number
        while i < len(formated) \
        and re.match('\d',formated[i]) != None:
            number += formated[i]
            i += 1

        # 2. Appending
        if len(number) != 0:
            number = int(number)
            cycles.append(number)
            number = ''

        if i == len(formated):
            break

        # 3. Checking format
        # a. single
        if formated[i] == ',':
            i += 1
        # b. range
        elif formated[i] == '-':
            i += 1
            number = cycles[-1]

            range_number = ''
            while i < len(formated)\
            and re.match('\d',formated[i]) != None:
                range_number += formated[i]
                i += 1
            range_number = int(range_number)

            if range_number < number:
                for n in range(range_number,number):
                    cycles.append(n)
            else:
                for n in range(number+1,range_number+1):
                    cycles.append(n)
            number = ''

    return cycles

@app.callback(   
    Output(component_id='plot_click', component_property='children'),
    [Input('plot_button','n_clicks'),
     Input('analysis-dropdown','value'),
     Input('title-input','value'),
     Input('xlabel-input','value'),
     Input('ylabel-input','value'),
     Input('cycles-input','value')],
    [State('type-radioitems','value')],
    [Event('type-radioitems','change')])
def refresh_callback(n_clicks,value,title,xlabel,ylabel,cycles,mode):
    global last_n_clicks
    if n_clicks == last_n_clicks:
        return None
    elif last_n_clicks != n_clicks:
        last_n_clicks = n_clicks
        formated = regex_format(deepcopy(cycles))
        if len(formated) > 0:
            cycle_list = cycletolist(formated)
            cycle_list.sort()
        else:
            cycle_list = []
        print('cycles: ',cycle_list)
        return plot_callback(str(value),title,xlabel,ylabel,cycle_list,mode)

if __name__ == '__main__':
    app.run_server(debug=True)
