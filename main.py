import streamlit as st

from knmy import knmy
import pandas as pd
import datetime

station = 260

st.title("Temperature and precipitation")
st.sidebar.title("Selections")

possible_stations = [209, 210, 215, 225, 235, 240,
                     242, 248, 249, 251, 257, 258, 260, 265,
                     267, 269, 270, 273, 275, 277, 278, 279,
                     280, 283, 285, 286, 290, 308, 310, 311,
                     312, 313, 315, 316, 319, 323, 324, 330,
                     331, 340, 343, 344, 348, 350, 356, 370,
                     375, 377, 380, 391]

station = st.sidebar.selectbox("Station", possible_stations,
                               index = 12,
                                format_func=int)  

startdate = st.sidebar.date_input('Start date', datetime.date(2015,11,1))
start = datetime.datetime.combine(startdate,datetime.datetime.min.time())

enddate = st.sidebar.date_input('End date', datetime.datetime(2020,12,1,0,0))
end = datetime.datetime.combine(enddate,datetime.datetime.max.time())

def plot_t_and_rh(station):
    disclaimer, stations, variables, data = knmy.get_knmi_data('hourly',
                            stations=[station],
                            start = start.strftime('%Y%m%d%H'),
                            end = end.strftime('%Y%m%d%H'),
                            parse=True) 
    
    
    
    data = data.iloc[1:]
    
    data['YYYYMMDD'] = pd.to_datetime(data['YYYYMMDD'], format = '%Y%m%d', errors='ignore')
    
    data.index = data['YYYYMMDD']+pd.to_timedelta(data['HH'].astype(int), unit='h',
                                                  errors='ignore')
    #data.index = pd.to_datetime(data.index, errors='ignore')
    #data.index = data.index.tz_localize('Europe/Amsterdam', ambiguous = 'NaT')
    droprows = ['2016-03-27 02:00:00',
                '2016-10-30 02:00:00',
                '2017-03-26 02:00:00',
                '2017-10-29 02:00:00',
                '2018-03-25 02:00:00',
                '2018-10-28 02:00:00',
                '2019-03-31 02:00:00',
                '2019-10-27 02:00:00',
                '2020-03-29 02:00:00',
                '2020-10-25 02:00:00']
    for row in droprows:
        try:
            data = data.drop(datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S'), axis=0)
        except:
            pass
    
    
    data = data[[ 'DD', 'FH', 'FF', 'FX', 'T', 'T10N', 'TD',
           'SQ', 'Q', 'DR', 'RH', 'P', 'VV', 'N', 'U', 'WW', 'IX', 'M', 'R', 'S',
           'O', 'Y']].astype(float)
    
    # RH filter
    data['RH'][data['RH'] < 0 ] = 0
    data['RH'] = data['RH']/10
    data['T'] = data['T']/10
    
    st.write(f"""
             ## Temperature at station {station} ({stations.name.values[0]})
             in degrees Celcius
             """)
             
    st.line_chart(data['T'])
    st.write(f"""
             ## Precipitation at station {station} ({stations.name.values[0]})
             in mm
             """)
    st.line_chart(data['RH'])


if __name__ == "__main__":
    plot_t_and_rh(station=station)