import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt, os
import matplotlib.pyplot as plt
# from vega_datasets import data
from datetime import date, timedelta
import plotly.graph_objects as go



def page_config():
    APP_TITLE = ':green[Soarroute Inc] Predictions Of Flight Delays'
    APP_SUB_TITLE = 'Authors: Sammie Srabani, Neha Korrapati, Leela Josna Kona, Devangi Samal'

    st.set_page_config(page_title=APP_TITLE, page_icon=":airplane_departure", layout="wide")
    st.title(f":satellite: {APP_TITLE} :airplane_departure:")
    st.caption(APP_SUB_TITLE)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

@st.cache_resource
def load_data():
    df = pd.read_csv("data/T_ONTIME_REPORTING.csv")

    # main_table = pd.read_csv("data/T_ONTIME_REPORTING.csv")
    # lookup_table = pd.read_csv("data/lookup_tables/L_AIRLINE_ID.csv")
    # df = pd.merge(main_table, lookup_table, left_on='OP_CARRIER_AIRLINE_ID', right_on='Code', how='inner')
    df = df.rename(columns={'OP_CARRIER_AIRLINE_ID': 'CARRIER'})


    return df