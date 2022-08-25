import streamlit as st
import numpy as np
import pandas as pd
import sys
import os
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

@st.cache()
def load_data():
    clean_data_df = pd.read_csv("./data/cleaned_telco_data.csv")
    return clean_data_df

@st.cache()
def load_exp_data():
    exp_data_df = pd.read_csv("./data/telco_user_experience_data.csv")
    return exp_data_df

def app():
    st.title("User Experience Analysis")
    clean_data_df = load_data()
    tellco_exprience_df = clean_data_df[['MSISDN/Number', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)',
                                         'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'Handset Type']]
    tellco_exprience_df['Total Avg RTT (ms)'] = tellco_exprience_df['Avg RTT DL (ms)'] + \
        tellco_exprience_df['Avg RTT UL (ms)']
    tellco_exprience_df['Total Avg Bearer TP (kbps)'] = tellco_exprience_df['Avg Bearer TP DL (kbps)'] + \
        tellco_exprience_df['Avg Bearer TP UL (kbps)']
    tellco_exprience_df['Total TCP Retrans. Vol (Bytes)'] = tellco_exprience_df['TCP DL Retrans. Vol (Bytes)'] + \
        tellco_exprience_df['TCP UL Retrans. Vol (Bytes)']
    tellco_exprience_df = tellco_exprience_df[[
        'MSISDN/Number', 'Total Avg RTT (ms)', 'Total Avg Bearer TP (kbps)', 'Total TCP Retrans. Vol (Bytes)', 'Handset Type']]
    tellco_exprience_df1 = tellco_exprience_df.groupby(
        'MSISDN/Number').agg({'Total Avg RTT (ms)': 'sum', 'Total Avg Bearer TP (kbps)': 'sum', 'Total TCP Retrans. Vol (Bytes)': 'sum', 'Handset Type': [lambda x: x.mode()[0]]})  # ' '.join(x)
    tellco_exprience_df = pd.DataFrame(columns=[
        "Total Avg RTT (ms)",
        "Total Avg Bearer TP (kbps)",
        "Total TCP Retrans. Vol (Bytes)",
        "Handset Type"])

    tellco_exprience_df["Total Avg RTT (ms)"] = tellco_exprience_df1["Total Avg RTT (ms)"]['sum']
    tellco_exprience_df["Total Avg Bearer TP (kbps)"] = tellco_exprience_df1["Total Avg Bearer TP (kbps)"]['sum']
    tellco_exprience_df["Total TCP Retrans. Vol (Bytes)"] = tellco_exprience_df1[
        "Total TCP Retrans. Vol (Bytes)"]['sum']
    tellco_exprience_df["Handset Type"] = tellco_exprience_df1["Handset Type"]['<lambda>']
    option = st.selectbox(
        'Top 10 of the top, bottom and most frequent Datas Based on',
        ('Total Avg RTT (ms)', 'Total Avg Bearer TP (kbps)', 'Total TCP Retrans. Vol (Bytes)'))

    data = tellco_exprience_df.sort_values(option, ascending=False)
    highest = data.head(10)[option]
    lowest = data.tail(10)[option]
    most = tellco_exprience_df[option].value_counts().head(10)
    
    st.header("Highest")
    highest = highest.reset_index('MSISDN/Number')
    fig = px.bar(highest, x='MSISDN/Number', y=option)
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)
    
    st.header("Lowest")
    lowest = lowest.reset_index('MSISDN/Number')
    fig = px.bar(lowest, x='MSISDN/Number', y=option)
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)
    
    st.header("Most")
    st.dataframe(most)

    exp_data_df = load_exp_data()
    st.title("User Clusters")
    st.write("")
    st.dataframe(exp_data_df.head(1000))
    st.write("")
    st.write("")
    st.markdown("***Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).***")
    plotly_plot_scatter(exp_data_df, 'Total TCP Retrans. Vol (Bytes)', 'Total Avg Bearer TP (kbps)',
            'cluster', 'Total Avg RTT (ms)')
    



def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)