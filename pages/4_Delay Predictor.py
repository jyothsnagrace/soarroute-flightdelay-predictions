# import stuff
from lib.functions import page_config
import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime

import keras
from joblib import Parallel, delayed 
import joblib


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
    #####################################
    @st.cache_data()
    def load_file(file):
        time.sleep(3)
        if file is not None:
            df = pd.read_csv(file)
        else:
            df = pd.read_csv(file)
        return(df)

        
    def add_colon (string):
      return string [:-2] + ":" + string[-2:]


    
    #######################################
    # load flight schedule
    # load model
    # load look up table
    # input box
    delay = "MODEL OUTPUT"
    delay_reason = "KNN model output"
    delay_dict = {0:"the carrier", 1: 'a late aircraft', 2: 'the National Aviation System', 3: "No Delay", 4: 'security reasons', 5: 'weather' }
    flight_schedule = load_file('data/flight_schedule.csv')
    airport_cities = load_file('data/airport_cities.csv')
    airlines = load_file('data/airline_list.csv')
    flight_info = load_file('data/flight_info.csv')
    ############################################
    st.subheader("Enter Flight Information")
    
    col1, col2 = st.columns(2)

    with col1:
      d = st.date_input("When is your flight", value = None)
      if not d: 
        st.stop()
      day_of_week = d.strftime('%A')

    with col2:
      st.empty()

    col1, col2 = st.columns(2)

    with col1:
      origin_list = flight_schedule.loc[flight_schedule['day_of_week'] == day_of_week, 'ORIGIN'].unique()
      origin_list.sort()
      origin = st.selectbox("Origin Airport", origin_list, index = None, placeholder = "Select Origin airport")
      if not origin:
        st.stop()
    
    with col2:
      dest_list = flight_schedule[(flight_schedule['day_of_week'] == day_of_week) & (flight_schedule['ORIGIN'] == origin)][["DEST"]]
      dest_list.drop_duplicates(inplace=True)
      dest_list.sort_values('DEST', inplace=True)
      destination = st.selectbox("Destination Airport", dest_list, index = None, placeholder= "Select Destination Airport")
      if not destination:
        st.stop()

    col1, col2 = st.columns(2)
    
    with col1:
      airlines_list = flight_schedule[(flight_schedule['day_of_week'] == day_of_week) & (flight_schedule['ORIGIN'] == origin) & (flight_schedule['DEST'] == destination)][['OP_CARRIER_AIRLINE_ID']]
      temp_list = airlines_list.merge(airlines,how = 'left', on = 'OP_CARRIER_AIRLINE_ID')
      air_list = temp_list['Description']
      air_list=air_list.drop_duplicates()
      air_list.sort_values(inplace=True)
      airline = st.selectbox("Airline", air_list, index=None, placeholder= "Select Airline")
      if not airline:
        st.stop()
    airline_id = airlines[airlines['Description'] == airline]['OP_CARRIER_AIRLINE_ID'].item()

    flight_start = flight_schedule[(flight_schedule['day_of_week'] == day_of_week) & (flight_schedule['OP_CARRIER_AIRLINE_ID'] == airline_id) & (flight_schedule['ORIGIN'] == origin) & (flight_schedule['DEST'] == destination)][["CRS_DEP_TIME"]].sort_values("CRS_DEP_TIME")

    with col2:
      t = st.selectbox("What time is your flight", flight_start, index = None, placeholder = "Select departure time")
      if not t:
        st.stop()


    city_origin = airport_cities.loc[airport_cities['AIRPORT'] == origin, 'CITY_MARKET'].item()
    city_dest = airport_cities.loc[airport_cities['AIRPORT'] == destination]['CITY_MARKET'].item()

    nn_model_input = flight_info[(flight_info['DAY_OF_WEEK'] == day_of_week) & (flight_info['ORIGIN'] == origin) & (flight_info['DEST'] == destination) & (flight_info['CRS_DEP_TIME'] == t)][["AIR_TIME","DISTANCE","CRS_ELAPSED_TIME"]]

    knn_model_input = flight_info[(flight_info['DAY_OF_WEEK'] == day_of_week) & (flight_info['ORIGIN'] == origin) & (flight_info['DEST'] == destination) & (flight_info['CRS_DEP_TIME'] == t)][['DEP_DELAY', 'ARR_DELAY', 'TAXI_OUT', 'TAXI_IN']]

    #############################

    ## get similar flights
    flight_schedule = flight_schedule.merge(airlines, on = "OP_CARRIER_AIRLINE_ID", how = 'left')
    flight_schedule['CRS_ARR_TIME']= flight_schedule['CRS_ARR_TIME'].astype(str)
    flight_schedule['CRS_ARR_TIME'] = flight_schedule['CRS_ARR_TIME'].apply(add_colon)
    flight_schedule['CRS_DEP_TIME']= flight_schedule['CRS_DEP_TIME'].astype(str)
    flight_schedule['CRS_DEP_TIME'] = flight_schedule['CRS_DEP_TIME'].apply(add_colon)

    similar_flights = flight_schedule[(flight_schedule['day_of_week'] == day_of_week) & (flight_schedule['ORIGIN_CITY_MARKET_ID'] == city_origin) & (flight_schedule['DEST_CITY_MARKET_ID'] == city_dest)][["Description","ORIGIN","DEST","CRS_DEP_TIME","CRS_ARR_TIME"]]


    if similar_flights.empty:
        similar_flights = "No other flight options"
    else:
        similar_flights.reset_index(drop = True, inplace=True)
        similar_flights.rename(columns = { "Description" : "Airline", "ORIGIN" : "Origin", "DEST" : "Destination", "CRS_DEP_TIME": "Departure Time", "CRS_ARR_TIME": "Arrival Time"}, inplace = True)

    ##### get NN model output

    user_input = nn_model_input.to_numpy()
    model = keras.models.load_model('nn_model.keras')
    delay = model.predict(user_input)

    knn_user_input = knn_model_input.to_numpy()
    knn_model = joblib.load('knn_model.pkl')
    delay_reason = knn_model.predict(knn_user_input)
    delay_reason = round(np.average(delay_reason))
    ###########################
    if delay[0][1]>= 0.5:
      delay_length = round(delay[0][0])
      reason = delay_dict.get(delay_reason)
      if delay_reason != 3:
        st.write("Your flight is usually delayed by " + reason + ".")
      st.write("Your flight is delayed " + str(delay_length) + " minutes on average.")
      st.write("Other Flight Options:")
      st.write(similar_flights)
    else:
      st.write("Your flight is usually on time.")




if __name__ == "__main__":
    main()
