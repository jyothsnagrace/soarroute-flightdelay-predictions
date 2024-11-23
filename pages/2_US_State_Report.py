
from lib.functions import load_data, date_filter, sidebar_filters, county_map, county_rank, ageGender_chart, race_chart, session_assign, page_config

import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt, os
import matplotlib.pyplot as plt
from vega_datasets import data
from datetime import date, timedelta



def main():

    ### Page Config
    page_config()

    with open('lib/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    ### Load Data
    df = load_data()
    df = df.dropna(subset=['res_state', 'res_county'])
    df = df.reset_index(drop=True)

    st.write("Dataset Shape: ", df.shape)

    #Display Filters and Map
    df, date1, date2 = date_filter(df)
    filtered_df, state, county = sidebar_filters(df)

    stateCounty_count = filtered_df.groupby(['res_state', 'state_fips_code', 'res_county', 'county_fips_code'])['count'].sum().reset_index(name='Total')
    state_count = filtered_df.groupby(['res_state', 'state_fips_code'])['count'].sum().reset_index(name='Total')

    # st.write(stateCounty_count.head())
    # st.write(stateCounty_count.shape)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"COVID-19 Vaccination Coverage Across U.S. Counties")
        county_map(stateCounty_count, state_count)
        

    with col2:
        st.subheader(f" Top Ranked States")
        county_rank(stateCounty_count)


    ### session_state

    session_assign(filtered_df, date1, date2, state, county)

    # "st.session_state object:", st.session_state


    tab1, tab2 = st.tabs(["Session State filters", "Session df"])
    
    with tab1:
        st.write("Start Date: ", st.session_state["my_date1"]) 
        st.write("End Date: ", st.session_state["my_date2"]) 
        st.write("State : ", st.session_state["my_state"]) 
        st.write("County: ", st.session_state["my_county"])        
    with tab2:
        st.write("df: ", st.session_state["my_df"]) 


if __name__ == "__main__":
    main()
