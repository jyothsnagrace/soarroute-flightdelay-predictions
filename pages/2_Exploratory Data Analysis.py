from lib.functions import load_data, page_config, get_correlation_matrix, plot_heatmap, plot_bar_chart
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import streamlit as st
import altair as alt, os

# Streamlit app
def main():

    ### Page Config
    page_config()

    ### css
    with open('lib/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

    ### Data Source
    st.markdown('''
        * :gray[**Data Source:** Bureau of Transportation Statistics bts.gov]
        * :gray[**Date Range:** 06/01/2024 to 06/30/2024]
        ''')
    
    ### Load Data and Preprocess Data
    
    data = load_data()


    tab1, tab2, tab3 = st.tabs(["Dataset Preview", "Correlation Map", "Top 10 U.S. Airports"])

    with tab1:
        st.subheader("Dataset Preview:")
        st.write("Dataset Shape: ", data.shape)
        st.write(data.head())

        st.write("Dataset Describe:")
        st.write(data.describe())
        

    with tab2:
        st.subheader("Correlation Heatmap:")
        correlation_matrix = get_correlation_matrix(data)
        st.altair_chart(plot_heatmap(correlation_matrix), use_container_width=True)

    with tab3:
        st.subheader("Top 10 Airports with Highest Average Arrival Delay")
        st.plotly_chart(plot_bar_chart(data), use_container_width=True)
            
 

if __name__ == "__main__":
    main()
