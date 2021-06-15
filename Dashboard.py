from functools import total_ordering
import streamlit as st 
import pandas as pd 
import numpy as np
from PIL import Image
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit.proto.DataFrame_pb2 import DataFrame


st.title ('Covid-19 Global Data Analysis Dashboard')
st.write ('Following shows the ***global cases and deaths of coronavirus in a weekly trend***')

img = Image.open ('covid-19-globe.jpg')
st.image (img)

@st.cache
def load_data():
    df = pd.read_csv ('World covid 19 stat.csv')
    return df

df = load_data()

st.sidebar.title ('Menu')
st.sidebar.markdown ('### **Recent week cases and deaths**')
cont_select = st.sidebar.selectbox ('Select a country',df['Country'].unique())
selected_cont = df[df['Country']==cont_select]

st.markdown('### **Recent week cases and deaths**')
def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
    'Recent week status':['Cases in the last seven days','Cases in the preceding seven days','Deaths in the last seven days','Deaths in the preceding seven days'],
    'Number of cases and deaths' :(df.iloc[0]['Cases in the last seven days'], df.iloc[0]['Cases in the preceding seven days'],
    df.iloc[0]['Deaths in the last seven days'], df.iloc[0]['Deaths in the preceding seven days'])})
    return total_dataframe

cont_total = get_total_dataframe(selected_cont)
cont_total_graph = px.bar(cont_total, x ='Recent week status',y = 'Number of cases and deaths',
                   labels = {'Number of cases and deaths':'Number of cases and deaths in %s' % (cont_select)},color = 'Recent week status')
st.plotly_chart(cont_total_graph)

st.markdown('### **Weekly cases and deaths (rate of change)**')
st.sidebar.markdown ('### **Weekly cases and deaths (rate of change)**')
chart_select = st.sidebar.selectbox ('Select chart type',('Area Chart','Strip Chart','Pie Chart'))
data_select = st.sidebar.selectbox ('Select a data',('Weekly Cases Change','Weekly Deaths Change'))

if chart_select  == 'Area Chart':
    if data_select == 'Weekly Cases Change':
        p_chart = px.area(df, y = df['Weekly Cases Change'], x = df['Country'],title = 'Weekly Cases Change', color = 'Country')
        st.plotly_chart(p_chart)
    else: 
        p_chart = px.area(df, y = df['Weekly Deaths Change'], x = df['Country'],title = 'Weekly Deaths Change', color = 'Country')
        st.plotly_chart(p_chart)

if chart_select  == 'Strip Chart':
    if data_select == 'Weekly Cases Change':
        p_chart = px.strip(df, y = df['Weekly Cases Change'], x = df['Country'],title = 'Weekly Cases Change', color = 'Country')
        st.plotly_chart(p_chart)
    else: 
        p_chart = px.strip(df, y = df['Weekly Deaths Change'], x = df['Country'],title = 'Weekly Deaths Change', color = 'Country')
        st.plotly_chart(p_chart)

if chart_select  == 'Pie Chart':
    if data_select == 'Weekly Cases Change':
        p_chart = px.pie(df, values  = df['Weekly Cases Change'], names  = df['Country'], title = 'Weekly Cases Change')
        st.plotly_chart(p_chart)
    else: 
        p_chart = px.pie(df, values = df['Weekly Deaths Change'], names = df['Country'], title = 'Weekly Deaths Change',)
        st.plotly_chart(p_chart)

st.markdown('### **Table of the data**')
def get_table():
    datatable = df[['Country', 'Cases in the last seven days', 'Cases in the preceding seven days',
    'Deaths in the last seven days', 'Deaths in the preceding seven days','Weekly Cases Change',
    'Weekly Deaths Change','Population']]
    return datatable

datatable = get_table()
st.dataframe(datatable)
