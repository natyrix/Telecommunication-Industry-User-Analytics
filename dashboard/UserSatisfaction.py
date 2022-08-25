import streamlit as st
import numpy as np
import pandas as pd
import sys
import os
import plotly.express as px


@st.cache()
def load_sat_only_scores_data():
    sat_only_scores_df = pd.read_csv("./data/telco_user_satisfaction_only_scores_data.csv")
    return sat_only_scores_df

@st.cache()
def load_sat_score_data():
    sat_score_df = pd.read_csv("./data/telco_user_satisfaction_score_data.csv")
    return sat_score_df


def app():
    st.title("User Satisfaction Analysis")
    st.write("")
    st.header("User engagement score table")
    sat_score_df = load_sat_score_data()
    sat_only_scores_df = load_sat_only_scores_data()
    eng_df = sat_score_df[['MSISDN/Number','xDR Sessions', 'Dur (ms)', 'Total Data Volume (Bytes)', 'engagement_score']]
    
    sat_score_df_agg = sat_score_df.groupby(
        'MSISDN/Number').agg({
            'Dur (ms)': 'sum', 
            'Total Data Volume (Bytes)': 'sum',
           'engagement_score':'sum',
           'engagement_cluster':'sum',
           'Total Avg RTT (ms)':'sum',
           'Total Avg Bearer TP (kbps)':'sum',
           'Total TCP Retrans. Vol (Bytes)':'sum',
           'experience_score':'sum',
           'experience_cluster':'sum',
           'satisfaction_score':'sum',
        })
    
    sat_only_score_df_agg = sat_only_scores_df.groupby(
        'MSISDN/Number').agg({
           'engagement_score':'sum',
           'experience_score':'sum',
           'satisfaction_cluster':'sum',
           'satisfaction_score':'sum',
        })

    st.write(eng_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 6 clusters based on their engagement(i.e. number of xDR sessions, duration and total data used).**")
    plotly_plot_scatter(sat_score_df, 'Total Data Volume (Bytes)', 'Dur (ms)',
            'engagement_cluster', 'xDR Sessions')

    
    st.write("")
    st.header("User experience score table")
    exp_df = sat_score_df[['MSISDN/Number', 'Total Avg RTT (ms)',
        'Total Avg Bearer TP (kbps)', 'Total TCP Retrans. Vol (Bytes)', 'experience_score']]
    st.write(exp_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).**")
    plotly_plot_scatter(sat_score_df, 'Total TCP Retrans. Vol (Bytes)', 'Total Avg Bearer TP (kbps)',
            'experience_cluster', 'Total Avg RTT (ms)')

    st.write("")
    st.header("User satisfaction score table")
    sat_df = sat_only_scores_df[['MSISDN/Number', 'engagement_score', 'experience_score', 'satisfaction_score']]
    st.write(sat_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 2 clusters based on their satisfactio(i.e. engagement score and experience score).**")
    plotly_plot_scatter(sat_only_scores_df, 'engagement_score', 'experience_score',
            'satisfaction_cluster', 'satisfaction_score')
    
    st.write("")
    st.header('Top 10 Numbers (Users) with highest')
    option = st.selectbox(
        'Top 10 Numbers (Users) with highest',
        ('Engagement Score', 'Experience Score', 'Satisfaction Score'))

    if option == 'Engagement Score':
        data = sat_score_df_agg.sort_values(
            'engagement_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'engagement_score', ascending=False).head(10)
        name = 'engagement_score'
    elif option == 'Experience Score':
        data = sat_score_df_agg.sort_values(
            'experience_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'experience_score', ascending=False).head(10)
        name = 'experience_score'
    else:
        data = sat_score_df_agg.sort_values(
            'satisfaction_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'satisfaction_score', ascending=False).head(10)
        name = 'satisfaction_score'
    
    data = data.reset_index('MSISDN/Number')
    # fig = px.pie(data, names='MSISDN/Number', values=name)
    # st.plotly_chart(fig)

    st.dataframe(sat_only_data)

    st.write("")
    st.dataframe(data)




def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)