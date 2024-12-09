# Soarroute Flight Delay Predictions
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://soarroute-flightdelay-predictions.streamlit.app/)

An Interactive Streamlit App Dashboard to analyze and predict the expected Flight Delays based on weather, airlines and flight origin-destination [Streamlit](https://www.streamlit.io) module to improve the travel experience. These models help stakeholders make data-driven decisions, like optimizing schedules or managing airport resources.
You can try [here](https://soarroute-flightdelay-predictions.streamlit.app/).

Data from the Bureau of Transportation Statistics (bts.gov) collected during 01 June 2024 to 30 June 2024, were analyzed to assess Flight Delay Predictions


## Results:
* Decision Tree and KNN models built, trained to predict flight delays
* Neural Network to predict the Flight delay

## Authors
Neha Korrapati, Leela Josna Kona, Devangi Samal, Sammie Srabani

## Objectives
* Identify potential delay flights

* Building a strategies to predict most common reason for delay 

## Dataset and model
* Bureau of Transportation Statistics (bts.gov)

## Libraries Used
* [Streamlit](https://www.streamlit.io)
* [Plotly](https://plotly.com/): (`streamlit.plotly_chart`)
* Keras and TensorFlow

## Snapshots
### 1. Landing Page
![Home](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/home_page.jpg)

### 2. Exploratory Data Analysis
![CH](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/correlation_heatmap.jpg)
![Top10](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/top10_us_airports_avg_arr_delay.jpg)

### 3. Flight Delay Predictions
![DT](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/decision_tree_report.jpg)
![KNN](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/knn_report.jpg)
![pie](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/delay_reasons_chart.jpg)
![bar](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/log_loss_comparision_chart.jpg)

### 4. Delay Predictor
![demo](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/delay_predictor.jpg)
![demo](https://github.com/jyothsnagrace/soarroute-flightdelay-predictions/blob/main/data/img/delay_predictor_demo.jpg)

## Future work
* Predict avg duration of delay – Regression
* Suggest alternative flights
