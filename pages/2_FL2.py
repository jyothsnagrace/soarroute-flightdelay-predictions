from lib.functions import load_data, page_config
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt, os
import streamlit as st

# Preprocess the data
def preprocess_data(data):
    # Example column names, adjust based on your dataset
    columns_to_use = ["ORIGIN", "DEST", "CARRIER", "DEP_DELAY", "ARR_DELAY", "WEATHER_DELAY", "CARRIER_DELAY", "NAS_DELAY"]
    data = data[columns_to_use].dropna()
    # st.write(data.head(500))
    
    # Convert categorical columns to numeric
    data = pd.get_dummies(data, columns=["ORIGIN", "DEST", "CARRIER"], drop_first=True)
    
    # Create target variable
    data['DELAY_REASON'] = np.where(data['WEATHER_DELAY'] > 0, 'Weather', 
                          np.where(data['DEP_DELAY'] > 15, 'Carrier', 'Other'))
    st.write(data.head(500))

    data = data.drop(['WEATHER_DELAY'], axis=1)
    # st.write(data.head(500))
    return data

# Train models
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

# Visualization
def plot_results(y_test, dt_pred, knn_pred):
    sns.countplot(x=y_test, palette="pastel")
    plt.title("Actual Delay Reasons")
    plt.show()

    sns.countplot(x=dt_pred, palette="pastel")
    plt.title("Decision Tree Predictions")
    plt.show()

    sns.countplot(x=knn_pred, palette="pastel")
    plt.title("KNN Predictions")
    plt.show()

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
    
    ### Load Data
    
    data = load_data()
    st.write("Dataset Preview:")
    st.write(data.head())
    
    # cols = data.columns
    # data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')

    data = preprocess_data(data)
    X = data.drop("DELAY_REASON", axis=1)
    y = data["DELAY_REASON"]
    
    dt_model, knn_model, dt_acc, knn_acc, y_test, dt_pred, knn_pred = train_models(X, y)
    
    st.write(f"Decision Tree Accuracy: {dt_acc:.2f}")
    st.write(f"KNN Accuracy: {knn_acc:.2f}")
    
    st.write("Visualizing Results:")
    plot_results(y_test, dt_pred, knn_pred)
    
    st.write("Decision Tree Classification Report:")
    st.text(classification_report(y_test, dt_pred))
    
    st.write("KNN Classification Report:")
    st.text(classification_report(y_test, knn_pred))

if __name__ == "__main__":
    main()
