from pysolar.solar import *
import datetime
import numpy as np
import pandas as pd 
import plotly.express as px
import serial
from time import sleep
import sys
import glob

# Find serial ports
def serial_ports():
    """ Lists serial port names

        @raises 
            EnvironmentError: On unsupported or unknown platforms
        @returns
            A list of the serial ports available on the system.
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Calibration parameters
altitude_calibr = 2048/180
altitude_offset = 0
azimuth_calibr = 7260/180
azimuth_offset = 90

# Serial connection
def connect(port="/dev/ttyACM0", baud=9600):
    ''' Serial connection

        @params 
            port: port device
            baud: baudrate (default=9600)
        @returns
            Device connected and opened.
    '''
    dev = serial.Serial(port, baud, timeout=0)
    return dev

# Move system
def move(dev, latitude, altitude, azimuth, timeinterval=2):
    ''' Function to move the mechanical system

        @params
            dev: serial connection
            latitude: location latitude
            altitude: sun altitude (deg)
            azimuth: sun azimuth (deg)
            timeinterval: sleep period, in seconds, after final position is reached

    '''

    dt = timeinterval * 1000

    alt = np.round((altitude - altitude_offset)*altitude_calibr)
    if latitude < 0 and azimuth > 180 : # move in the same direction 
        azimuth = azimuth - 360
    az = np.round((azimuth - azimuth_offset)*azimuth_calibr)

    dev.flushInput()

    while dev.inWaiting() < 10 :
        sleep(0.2)    
    
    stepper_status = dev.readline()[-1]
        
    if stepper_status == 0 :
        print("pos: " + str(alt) + "; " + str(az) + "\n") 
        msg = "movesun;" + str(alt) + ";" + str(az) + ";" + str(dt) + "\n"
        dev.write(bytes(msg,'utf-8'))
    else :
        print("ERRO")
    
    return

# Initial position DF
def nulldf(altitude, azimuth):
    ''' Create a dataframe with the initial position

        @params
            altitude: sun altitude (deg)
            azimuth: sun azimuth (deg)
        @returns
            Dataframe with initial position.
    '''
    df = pd.DataFrame({'altitude':[altitude], 'azimuth':[azimuth]})
    return df

# One point sun position
def onepoint_sim(latitude, longitude, year, month, day, hour, utcdiff=0):
    ''' Find the sun position 
    
        @params
            latitude, longitude: geographic coordinates
            year, month, day: date (integer values)
            hour: hour (integer)
            utcdiff: timeozone (eg. -3, default=0)
        @returns
            Dataframe with the sun position (altitude and azimuth).
    '''
    tz = datetime.timezone(datetime.timedelta(hours=utcdiff)) # acertando fuso horário
    localdate = datetime.datetime(year, month, day, hour, 0, tzinfo=tz) # criando datetime 
    alt = get_altitude(latitude, longitude, localdate)
    az = get_azimuth(latitude, longitude, localdate)
    df = pd.DataFrame({'datetime':[localdate],'latitude':[str(latitude)],'longitude':[str(longitude)],
        'altitude':[alt],'azimuth':[az]})
    return df

# One day sun position
def oneday_sim(latitude, longitude, year, month, day, utcdiff=0):
    ''' Find the sun position for each hour in a specific day

        @params
            latitude, longitude: geographic coordinates
            year, month, day: date (integer values)
            utcdiff: timezone (eg. -3, default=0)
        @returns
            Dataframe with sun positions (altitude and azimuth) for each hour (00:00 to 23:00).
    '''

    day_hours = np.arange(0,24)
    alt = []
    az = []
    localdate = []
    for h in day_hours:
        tz = datetime.timezone(datetime.timedelta(hours=utcdiff))
        localdate.append(datetime.datetime(year, month, day, h, 0, tzinfo=tz))
        alt.append(get_altitude(latitude, longitude, localdate[-1]))
        az.append(get_azimuth(latitude, longitude, localdate[-1]))
    n = len(alt)
    df = pd.DataFrame({'datetime':localdate,'latitude':np.repeat(str(latitude),n),'longitude':np.repeat(str(longitude),n),
        'altitude':alt,'azimuth':az})
    return df

# One year (monthly) sun position
def month_sim(latitude, longitude, year, day, hour, utcdiff=0):
    ''' Find sun position for each month in a whole year, for the same day and hour

        @params
            latitude, longitude: geographic coordinates
            year, day: date (integer values)
            hour: hour (integer)
            utcdiff: timezone (eg. -3, default = 0)
        @returns
            Dataframe with sun positions (altitude and azimuth) for each month.
    '''

    if day > 28:
        if day == 31:
            months = np.array([1,3,5,7,8,10,12])
        else:
            months = np.array([1,3,4,5,6,7,8,9,10,11,12])
    else:
        months = np.arange(1,13)
    alt = []
    az = []
    localdate = []
    for m in months:
        tz = datetime.timezone(datetime.timedelta(hours=utcdiff))
        localdate.append(datetime.datetime(year, m, day, hour, 0, tzinfo=tz))
        alt.append(get_altitude(latitude, longitude, localdate[-1]))
        az.append(get_azimuth(latitude, longitude, localdate[-1]))
    n = len(alt)
    df = pd.DataFrame({'datetime':localdate,'latitude':np.repeat(str(latitude),n),'longitude':np.repeat(str(longitude),n),
        'altitude':alt,'azimuth':az})
    return df

# Generate sun map for single sun position
def sun_position(valid_data):
    ''' Generate plotly graph with a sun position

        @params
            valid_data: dataframe with single sun position and altitude >= 0
        @returns
            Plotly polar graph
    '''
    figure = px.scatter_polar(valid_data,r='altitude', theta='azimuth', symbol_sequence=['circle'], size=[0.3],
        range_r=[90,0], range_theta=[0,360], start_angle=90, direction="clockwise", color_discrete_sequence=['orange'])
    return figure

# Add reference lines
def add_path(figure, lat, lon, y, m, d, h, tz, pathtype=["sp_day"]):
    ''' Add reference lines to existing plotly graph

        @params
            figure: sun polar graph with a sun position
            lat, lon: geographic coordinates
            y, m, d: date (integer values)
            h, tz: hour and timezone
            pathtype: "sp_day"     ->  sun path for the chosen day
                      "sp_month"   ->  sun path during the year for the same day and hour
                      "sol_summer" ->  summer solstice
                      "sol_winter" ->  winter solstice
                      "equinox"    ->  equinox
        @returns
            Updated figure.
    '''
        
    for i in pathtype:

        if i == "sp_day":
            ldf = oneday_sim(lat, lon, y, m, d, tz)
            ldf = ldf.query('altitude >= 0')
            figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                start_angle=90, direction='clockwise', color_discrete_sequence=['orange']).select_traces()))
    
        elif i == "sp_month":    
            ldf = month_sim(lat, lon, y, d, h, tz)
            ldf = ldf.query('altitude >= 0')
            figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                start_angle=90, direction='clockwise', color_discrete_sequence=['orange']).select_traces()))
        
        elif i ==  "sol_summer":
            if lat > 0:
                ldf = oneday_sim(lat, lon, y, 6, 21, tz)
                ldf = ldf.query('altitude >= 0')
                figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                    start_angle=90, direction='clockwise', line_dash_sequence=['dash'], 
                    color_discrete_sequence=['red']).select_traces()))
            else:
                ldf = oneday_sim(lat, lon, y, 12, 21, tz)
                ldf = ldf.query('altitude >= 0')
                figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                    start_angle=90, direction='clockwise', line_dash_sequence=['dash'], 
                    color_discrete_sequence=['red']).select_traces()))

        elif i ==  "sol_winter":
            if lat > 0:
                ldf = oneday_sim(lat, lon, y, 12, 21, tz)
                ldf = ldf.query('altitude >= 0')
                figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                    start_angle=90, direction='clockwise', line_dash_sequence=['dash'], 
                    color_discrete_sequence=['blue']).select_traces()))
            else:
                ldf = oneday_sim(lat, lon, y, 6, 21, tz)
                ldf = ldf.query('altitude >= 0')
                figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                    start_angle=90, direction='clockwise', line_dash_sequence=['dash'], 
                    color_discrete_sequence=['blue']).select_traces()))

        elif i == "equinox":
            ldf = oneday_sim(lat, lon, y, 3, 20, tz)
            ldf = ldf.query('altitude >= 0')
            figure.add_traces(list(px.line_polar(ldf, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
                start_angle=90, direction='clockwise', line_dash_sequence=['dot'], 
                color_discrete_sequence=['green']).select_traces()))
            # ldf_b = oneday_sim(lat, lon, y, 9, 22, tz)
            # ldf_b = ldf_a.query('altitude >= 0')
            # figure.add_traces(list(px.line_polar(ldf_b, r='altitude', theta='azimuth', range_r=[90,0], range_theta=[0,360], 
            #     start_angle=90, direction='clockwise', line_dash_sequence=['dot'], 
            #     color_discrete_sequence=['green']).select_traces()))

    return figure


#def concat_simulation():

# def sunpath_plot(sim, col='latitude', pos=None):
#     Encontrando alturas maiores do que zero
#     valid_data = sim.query('altitude >= 0')
#     n = len(valid_data)
#     if n == 0:
#         fig = "No valid data"
#     elif n == 1:
#         fig = px.scatter_polar(valid_data,r='altitude', theta='azimuth', symbol_sequence=['circle'], size=[0.3],
#         range_r=[90,0], range_theta=[0,360], start_angle=90, direction="clockwise")
#     else:
#         valid_data.insert(5,'status', np.repeat(1,n))
#         if pos is not None:
#             valid_data.iloc[pos,5] = 2
#         fig = px.scatter_polar(valid_data,r='altitude', theta='azimuth', color=col, 
#             symbol=valid_data['status'], symbol_sequence=['circle-open','circle'], size=np.repeat(0.3,n),
#             range_r=[90,0], range_theta=[0,360], start_angle=90, direction="clockwise")
    
#     return fig

