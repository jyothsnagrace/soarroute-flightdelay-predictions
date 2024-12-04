import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import altair as alt
import plotly.express as px

def page_config():
    APP_TITLE = ':green[Soarroute Inc] Flight Delay Predictions'
    APP_SUB_TITLE = 'Authors: Neha Korrapati, Leela Josna Kona, Sammie Srabani, Devangi Samal'

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_page_config(page_title=APP_TITLE, page_icon=":airplane_departure", layout="wide")
    st.title(f":satellite: {APP_TITLE} :airplane_departure:")
    st.caption(APP_SUB_TITLE)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    

# Load the dataset
@st.cache_resource
def load_data():
    df = pd.read_csv("data/T_ONTIME_REPORTING.csv")
    df = df.rename(columns={'OP_CARRIER_AIRLINE_ID': 'CARRIER'})
    return df

def get_correlation_matrix(data):
    delay_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 
                     'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
    delay_data = data[delay_columns].dropna()
    correlation_matrix = delay_data.corr().reset_index().melt('index')
    correlation_matrix.columns = ['Variable 1', 'Variable 2', 'Correlation']
    return correlation_matrix


def plot_heatmap(correlation_matrix):
    heatmap = alt.Chart(correlation_matrix).mark_rect().encode(
        x='Variable 1:O',
        y='Variable 2:O',
        color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='yellowgreenblue', domainMid=0)),
        tooltip=['Variable 1', 'Variable 2', 'Correlation']
    ).properties(
        width=500,
        height=500
    )
    return heatmap

def plot_bar_chart(data):
    avg_delay_by_origin = data.groupby('ORIGIN')['ARR_DELAY'].mean().reset_index()
    top_10_avg_delay = avg_delay_by_origin.nlargest(10, 'ARR_DELAY')
    bar_plot = px.bar(top_10_avg_delay, x='ORIGIN', y='ARR_DELAY', color='ARR_DELAY',  color_continuous_scale='tealgrn'
                      )
    bar_plot.update_layout(xaxis_title='Origin Airport', yaxis_title='Average Arrival Delay')
    return bar_plot

#################################################

# Preprocess the data
def preprocess_data(data):
    data = data.rename(columns={'CARRIER_DELAY': 'CARRIER DELAY', 'WEATHER_DELAY': 'WEATHER DELAY', 'NAS_DELAY': 'NAS DELAY', 
                                'SECURITY_DELAY': 'SECURITY DELAY', 'LATE_AIRCRAFT_DELAY':'LATE AIRCRAFT DELAY'})
   
    delay_columns = [
        'CARRIER DELAY', 'WEATHER DELAY', 'NAS DELAY', 'SECURITY DELAY', 'LATE AIRCRAFT DELAY'
    ]

    data['DELAY_REASON'] = data[delay_columns].idxmax(axis=1)
    data['DELAY_REASON'] = data['DELAY_REASON'].fillna('NO_DELAY')
    X = data[['DEP_DELAY', 'ARR_DELAY', 'TAXI_OUT', 'TAXI_IN']].fillna(0)
    y = data['DELAY_REASON']
    le = LabelEncoder()
    y = le.fit_transform(y)
    return X, y, le


# Train DT and KNN Classifier models
def train_models(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_pred)

    # KNN
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    knn_pred = knn_model.predict(X_test)
    knn_acc = accuracy_score(y_test, knn_pred)
    
    return dt_model, knn_model, dt_acc, knn_acc, y_test, dt_pred, knn_pred

def plot_results(df):
    base = alt.Chart(df).encode(
         theta=alt.Theta(field='Percentage (%)', type='quantitative'),
         color=alt.Color(field='Reason', type='nominal').scale(scheme="yellowgreenblue"),
         tooltip=['Reason', 'Count', 
         alt.Tooltip('Percentage (%):Q', title='Percentage', format='.2f')]
         )
    pie = base.mark_arc(outerRadius=120)

    # text = base.mark_text(radius=90, size=12).encode(
    #         text=alt.Text('Percentage (%):Q', format=".2f"),
    #         theta=alt.Theta(field='Percentage (%)', type='quantitative'),
    #         color=alt.value('black')  # Ensures text is readable
    #         )
            
    st.altair_chart(pie, use_container_width=True, theme="streamlit")