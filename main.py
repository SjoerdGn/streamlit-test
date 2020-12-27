import streamlit as st

from knmy import knmy
import pandas as pd

station = 260

st.title("Temperature and precipitation")
st.sidebar.title("Selections")

possible_stations = [209,
                     210, 215, 225, 235, 240,
                     242, 248, 249, 251, 257, 258, 260, 265,
                     267, 269, 270, 273, 275, 277, 278, 279,
                     280, 283, 285, 286, 290, 308, 310, 311,
                     312, 313, 315, 316, 319, 323, 324, 330,
                     331, 340, 343, 344, 348, 350, 356, 370,
                     375, 377, 380, 391]

station = st.sidebar.selectbox("Station", possible_stations,
                               index = 12,
                                format_func=int)  

def plot_t_and_rh(station):
    disclaimer, stations, variables, data = knmy.get_knmi_data('hourly',
                            stations=[station],
                            parse=True) 
    
    
    
    data = data.iloc[1:]
    
    data['YYYYMMDD'] = pd.to_datetime(data['YYYYMMDD'], format = '%Y%m%d')
    data.index = data['YYYYMMDD']+pd.to_timedelta(data['HH'].astype(int), unit='h')
    
    data = data[[ 'DD', 'FH', 'FF', 'FX', 'T', 'T10N', 'TD',
           'SQ', 'Q', 'DR', 'RH', 'P', 'VV', 'N', 'U', 'WW', 'IX', 'M', 'R', 'S',
           'O', 'Y']].astype(float)
    
    # RH filter
    data['RH'][data['RH'] < 0 ] = 0
    
    st.write(f"""
             # Temperature at station {station}
             """)
             
    st.line_chart(data['T'])
    st.write(f"""
             # Precipitation at station {station}
             """)
    st.line_chart(data['RH'])


if __name__ == "__main__":
    plot_t_and_rh(station=station)