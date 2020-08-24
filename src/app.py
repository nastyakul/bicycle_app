import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objs as go

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import sys
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.

PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
DATA_DIR = os.path.join(PARENT_DIR, 'data')

df_train = pd.read_csv(os.path.join(DATA_DIR, 'train.csv')).set_index('datetime')
df_train.index = pd.to_datetime(df_train.index)

def get_time_features(df):
    # time-derived features
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day_of_year'] = df.index.dayofyear
    return(df)
df_train = get_time_features(df_train)
columns_to_group = ['season', 'holiday', 'hour', 'day_of_week', 'month', 'year']

st.title('Bicycle demand checker')

# plotly figure setup
fig = go.Figure()

# one trace for each df column
for col in columns_to_group:
    fig.add_trace(go.Bar(
        x=df_train.groupby(col)['count'].mean().index,
        y=df_train.groupby(col)['count'].mean().values,
    name = col))

# one button for each df column
updatemenu= []
buttons=[]
for col in columns_to_group:
    visible_arr = np.zeros(len(columns_to_group), dtype=bool)
    visible_arr[columns_to_group.index(col)] = True
    buttons.append(dict(method='restyle',
                        label=col,
                        args=[{'x': [df_train.groupby(col)['count'].mean().index],
                               'y':[df_train.groupby(col)['count'].mean().values],
                              'visible': visible_arr}])
                  )

# some adjustments to the updatemenu
updatemenu=[]
your_menu=dict()
updatemenu.append(your_menu)
updatemenu[0]['buttons']=buttons
updatemenu[0]['direction']='down'
updatemenu[0]['showactive']=True

# update layout and show figure
fig.update_layout(updatemenus=updatemenu, title="Demand for bicycles depends on a number of factors:")
st.plotly_chart(fig)

date = st.sidebar.date_input(label = "Pick a date")
# st.write(type(date))
# st.write(df_preprocessed.head())

time_of_day = st.sidebar.selectbox(
    'Choose time',
    ('Morning', 'Day', 'Evening', 'Night')
)

weather = st.sidebar.selectbox(
    'What is the weather like?',
    ('Clear', 'Cloudy', 'Rainy', 'Snowy')
)

st.write(f'We suggest, the demand for bicycles on {date} will be above average:')
df_train['count'].hist(bins = 20, density = True)
plt.axvline(100, c='b')

############
# Processing input
############
input_columns = ["season", "holiday",	"workingday", "weather", "temp", "atemp", "humidity",
           "windspeed", "casual", "registered", "count"]
df_input = pd.DataFrame(columns = input_columns)

# def construct_datetime():
#     """
#     parse datetime input
#     :return:
#     """
# def get_season():
#     """
#     infer season from datetime
#     :return:
#     """
#
# def get_holiday():
#     """
#     infer if the day is a holiday or not
#     :return:
#     """
#
# def get_workingday():
#     """
#     infer if the day is a working day or not
#     :return:
#     """
#
# def get_weather():
#     """
#     encode provided weather
#     :return:
#     """




