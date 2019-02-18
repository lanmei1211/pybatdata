# Structure for the example text in boxes
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

def InputTextHTML(id_,placeholder_):
    return dcc.Input(
                id= id_,
                inputmode= 'latin-english',
                minlength = 1,
                maxlength = 30,
                placeholder= placeholder_,
                spellCheck = True,
                style={
                    'width': '80%',
                    'marginLeft': '10%', 'marginRight': '10%',
                    'height': '97.5%',
                    'marginBottom': '2.5%',
                    'textAlign': 'left',
                    'color': '#000000',
                    'fontFamily': 'Roboto Condensed',
                    'fontSize': '18',
                    'fontWeight': 'normal',
                    'marginLeft': '35px',
                },
                type='text',
                value=''
            )

def InputPathHTML(id_,placeholder_):
    return dcc.Input(
                id= id_,
                minlength = 1,
                maxlength = 30,
                placeholder= placeholder_,
                spellCheck = True,
                style={
                    'width': '80%',
                    'marginLeft': '10%', 'marginRight': '10%',
                    'height': '97.5%',
                    'marginBottom': '2.5%',
                    'textAlign': 'left',
                    'color': '#000000',
                    'fontFamily': 'Roboto Condensed',
                    'fontSize': '18',
                    'fontWeight': 'normal',
                    'marginLeft': '35px',
                },
                type='text',
                value=''
            )

