import streamlit as st

from knmy import knmy
import pandas as pd

disclaimer, stations, variables, data = knmy.get_knmi_data('hourly',
                        stations=[260],
                        parse=True) 



data = data.iloc[1:]

data['YYYYMMDD'] = pd.to_datetime(data['YYYYMMDD'], format = '%Y%m%d')
data.index = data['YYYYMMDD']+pd.to_timedelta(data['HH'].astype(int), unit='h')

#%%
data = data[[ 'DD', 'FH', 'FF', 'FX', 'T', 'T10N', 'TD',
       'SQ', 'Q', 'DR', 'RH', 'P', 'VV', 'N', 'U', 'WW', 'IX', 'M', 'R', 'S',
       'O', 'Y']].astype(float)


#%%