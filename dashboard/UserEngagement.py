import streamlit as st
import numpy as np
import pandas as pd
import sys
import os
import plotly.express as px

@st.cache()
def load_data():
    clean_data_df = pd.read_csv("./data/cleaned_telco_data.csv")
    return clean_data_df

@st.cache()
def load_eng_data():
    eng_data_df = pd.read_csv("./data/telco_user_engagement_data.csv")
    return eng_data_df

clean_data_df = load_data()
eng_data_df = load_eng_data()

def app():
    st.title("User Engagement Analysis")
    st.header('Here is sample data from the cleaned table')
    clean_data_df = load_data()
    st.dataframe(clean_data_df.head(1000))
    app_clean_data_df = clean_data_df[['MSISDN/Number', 'Social Media Data Volume (Bytes)', 'Google Data Volume (Bytes)',
                                   'Email Data Volume (Bytes)', 'Youtube Data Volume (Bytes)', 'Netflix Data Volume (Bytes)',
                                   'Gaming Data Volume (Bytes)', 'Other Data Volume (Bytes)']]
    app_clean_data_df = app_clean_data_df.groupby(
        'MSISDN/Number').agg({
            'Social Media Data Volume (Bytes)': 'sum',
            'Google Data Volume (Bytes)': 'sum',
            'Email Data Volume (Bytes)': 'sum',
            'Youtube Data Volume (Bytes)': 'sum',
            'Netflix Data Volume (Bytes)': 'sum',
            'Gaming Data Volume (Bytes)': 'sum',
            'Other Data Volume (Bytes)': 'sum',
        })

    clean_data_df = clean_data_df[['MSISDN/Number', 'Bearer Id', 'Dur (ms)', 'Total Data Volume (Bytes)']]
    
    clean_data_df = clean_data_df.groupby(
        'MSISDN/Number').agg({
            'Bearer Id': 'count', 
            'Dur (ms)': 'sum', 
            'Total Data Volume (Bytes)': 'sum'
        })
    clean_data_df = clean_data_df.rename(
        columns={'Bearer Id': 'number of xDR Sessions'})

    st.write("")
    st.header('Top 10 Numbers (Users) with highest')
    option = st.selectbox(
        'Top 10 Numbers (Users) with highest',
        ('Number of xDR Sessions', 'Number of Duration', 'Total Data Volume'))

    if option == 'Number of xDR Sessions':
        data = clean_data_df.sort_values(
            'number of xDR Sessions', ascending=False).head(10)
        name = 'number of xDR Sessions'
    elif option == 'Number of Duration':
        data = clean_data_df.sort_values('Dur (ms)', ascending=False).head(10)
        name = 'Dur (ms)'
    elif option == 'Total Data Volume':
        data = clean_data_df.sort_values(
            'Total Data Volume (Bytes)', ascending=False).head(10)
        name = 'Total Data Volume (Bytes)'
    data = data.reset_index('MSISDN/Number')
    fig = px.pie(data, names='MSISDN/Number', values=name)
    st.plotly_chart(fig)

    # st.write('You selected:', option)

    st.dataframe(data)

    st.write("")
    st.header('Top 10 Engaged Users Per App')
    app_option = st.selectbox(
        'Top 10 Engaged Users Per App',
        ('Social Media', 'Youtube','Google', 'Email', 'Netflix', 'Gaming', 'Other')
    )

    if app_option == 'Social Media':
        app_data = app_clean_data_df.sort_values(
            'Social Media Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Social Media Data Volume (Bytes)'
    elif app_option == 'Youtube':
        app_data = app_clean_data_df.sort_values(
            'Youtube Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Youtube Data Volume (Bytes)'
    elif app_option == 'Google':
        app_data = app_clean_data_df.sort_values(
            'Google Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Google Data Volume (Bytes)'
    elif app_option == 'Email':
        app_data = app_clean_data_df.sort_values(
            'Email Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Email Data Volume (Bytes)'
    elif app_option == 'Netflix':
        app_data = app_clean_data_df.sort_values(
            'Netflix Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Netflix Data Volume (Bytes)'
    elif app_option == 'Gaming':
        app_data = app_clean_data_df.sort_values(
            'Gaming Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Gaming Data Volume (Bytes)'
    else:
        app_data = app_clean_data_df.sort_values(
            'Other Data Volume (Bytes)',ascending=False
        ).head(10)
        app_name = 'Other Data Volume (Bytes)'
    
    app_data = app_data.reset_index('MSISDN/Number')
    app_fig = px.pie(app_data, names='MSISDN/Number', values=app_name)
    st.plotly_chart(app_fig)
    st.dataframe(app_data)

    st.title("User Clusters")
    st.write("")
    eng_data_df = load_eng_data()
    st.dataframe(eng_data_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 6 clusters based on their engagement(i.e. number of xDR sessions, duration and total data used).**")
    plotly_plot_scatter(eng_data_df, 'Total Data Volume (Bytes)', 'Dur (ms)',
            'cluster', 'xDR Sessions')








def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)
