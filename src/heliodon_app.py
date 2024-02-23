import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import heliodon as sun
import webbrowser
from threading import Timer
from waitress import serve

# App

app = dash.Dash(__name__)

server = app.server

def open_browser():
    """
    Open browser to localhost
    """

    webbrowser.open_new('http://127.0.0.1:8080/')


# Layout

app.layout = html.Div([

    html.Div(children=[
        
        html.H1(
            children='HELIODON',
            style={
                'textAlign': 'center'
            }
        ),
        
        html.H4('Location'),
        html.Div([
            html.Label("Latitude"),
            html.Br(),
            dcc.Input(id='LAT', value='latitude', type='text')
        ], style={'width':'50%', 'display':'inline-block'}),
        html.Div([
            html.Label("Longitude"),
            html.Br(),
            dcc.Input(id='LON', value='longitude', type='text'),            
        ], style={'width':'50%', 'float':'right'}),

        html.H4('Datetime'),
        html.Label('Year'),
        html.Br(),
        dcc.Input(id='y', value='year', type='text'),
        html.Br(),
        html.Br(),
        html.Label('Month'),
        html.Br(),
        dcc.Slider(1,12,1, value=6, id='m'),
        html.Label('Day'),
        html.Br(),
        dcc.Slider(1,31,1, value=15, id='d'),

        html.Label('Hour'),
        html.Br(),
        dcc.Slider(0,23,1, value=10, id='h'),
        html.Label('Timezone (UTC)'),
        html.Br(),
        dcc.Slider(-12,12,1, value=0, id='utc'),

        html.H4('References'),
        dcc.Checklist(
            options={
                'sp_day': 'Sun path (day)',
                'sp_month': 'Sun path (month)',
                'sol_summer': 'Summer solstice',
                'sol_winter': 'Winter solstice',
                'equinox': 'Equinox'
            },
            value=['sp_day'],
            id='refpath'
        ),

    ], style={'width':'45%', 'display':'inline-block'}),

    html.Div([

        dcc.Graph(
            id = 'sunmap',
            style={'height':500}
        ),
        html.Div([
           html.Button('PLOT AND MOVE', id='move_show', n_clicks=0), 
        ], style={'width':'20%', 'float':'left'}),
        html.Div([
            html.Button('ZERO AND CLOSE CON', id='zero', n_clicks=0),
        ], style={'width':'20%', 'float':'left'})     

    ],style={'width':'40%', 'float':'right'})
    
], style={'display': 'flex', 'flex-direction': 'row'})


# Callback

@app.callback(
    Output('sunmap', 'figure'),
    Input('zero', 'n_clicks'), Input('move_show', 'n_clicks'),
    State('LAT', 'value'), State('LON','value'), State('y','value'), State('m','value'), 
    State('d','value'), State('h','value'), State('utc','value'), State('refpath', 'value')
)
def update_output_div(zero_clicks, moveshow_clicks, 
        lat_s, lon_s, y_s, m_s, d_s, h_s, tz_s, ref_s):

    if zero_clicks == 0 and moveshow_clicks == 0 :
        df = sun.nulldf(0,90)
        fig = sun.sun_position(df)
        return fig

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'zero' in changed_id:
        if not(con.isOpen()):
            con.open()
        df = sun.nulldf(0,90)
        fig = sun.sun_position(df)
        sun.move(con, 0.0, df.altitude.iloc[0], df.azimuth.iloc[0], timeinterval=0)
        con.close()

    if 'move_show' in changed_id:
        if not(con.isOpen()):
            con.open()
        df = sun.onepoint_sim(float(lat_s), float(lon_s), int(y_s), int(m_s), int(d_s), int(h_s), int(tz_s))
        if df.altitude.iloc[0] >= 0:
            fig = sun.sun_position(df) 
            sun.add_path(fig, float(lat_s), float(lon_s), int(y_s), int(m_s), int(d_s), int(h_s), int(tz_s), pathtype=ref_s)
            sun.move(con, float(lat_s), df.altitude.iloc[0], df.azimuth.iloc[0], timeinterval=0)

    return fig
            

if __name__ == '__main__':

    available_ports = sun.serial_ports()
    port_id = range(len(available_ports))
    print("Port list: ")
    for n, v in zip(port_id, available_ports):
        print("{} -> {}".format(n, v))
    print("Port ID: ")
    id = int(input())
    con = sun.connect(available_ports[id])

    Timer(1, open_browser).start()
    serve(server)
    #app.run_server(debug=False)