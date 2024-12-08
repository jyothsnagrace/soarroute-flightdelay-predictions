from lib.functions import load_data, page_config, preprocess_data, train_models, plot_results
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, log_loss
import streamlit as st
import altair as alt, os
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt



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
    X, y, le = preprocess_data(data)

    dt_model, knn_model, y_test, dt_pred, knn_pred, dt_acc, knn_acc, chart, results = train_models(X, y)
    

    tab1, tab2, tab3, tab4 = st.tabs(["Decision Tree Classification", "KNN Classification", "Delay Reasons Chart", "Log-Loss Comparision"])

    with tab1:
        st.subheader("Decision Tree Classification Report:")
        st.write(f"Decision Tree Accuracy: {dt_acc:.2f}")
        st.dataframe(pd.DataFrame(classification_report(y_test, dt_pred, target_names=le.classes_, output_dict=True)).transpose())

    with tab2:
        st.subheader("KNN Classification Report:")
        st.write(f"KNN Accuracy: {knn_acc:.2f}")
        st.dataframe(pd.DataFrame(classification_report(y_test, knn_pred, target_names=le.classes_, output_dict=True)).transpose())


    with tab3:
        st.subheader("Flight Delay Reasons Distribution")
        delay_reason_counts = pd.Series(le.inverse_transform(y)).value_counts().reset_index()
        delay_reason_counts.columns = ['Reason', 'Count']
        delay_reason_counts = delay_reason_counts[delay_reason_counts['Reason'] != 'NO_DELAY']
        delay_reason_counts['Percentage (%)'] = ((delay_reason_counts['Count'] / delay_reason_counts['Count'].sum()) * 100).round(2)

        with st.container(border=True):
            col1, col2 = st.columns(2)

        with col1:
            st.write(delay_reason_counts.head())

        with col2:
            plot_results(delay_reason_counts)

    with tab4:
        st.subheader("Log-Loss Comparision")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
   
        with col1:
            st.write(results.head())

        with col2:
            st.altair_chart(chart, theme="streamlit")


if __name__ == "__main__":
    main()
