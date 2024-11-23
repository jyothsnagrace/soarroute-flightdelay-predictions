
from lib.functions import load_data, page_config
import numpy as np
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

    ### css
    with open('lib/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    ### Data Source
    st.markdown('''
        * :gray[**Data Source:** Bureau of Transportation Statistics bts.gov]
        * :gray[**Date Range:** 2020/01/01 to 2022/12/01]
        ''')
    
    ### Load Data
    df = load_data()

    st.write("Dataset Shape: ", df.shape)

    st.write("Sample Charts placeholder")

     ### Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Flight Delay Reasons")
        st.bar_chart(np.random.randn(50, 3))
        

    with col2:
        st.subheader(f" Average length of Flight Delays")
        st.line_chart(np.random.randn(50, 3))
       
    


if __name__ == "__main__":
    main()
