
# # import stuff
# import streamlit as st
# import numpy as np
# import pandas as pd
# import time
# import datetime
# #####################################
# @st.cache_data()
# def load_file(file):
#     time.sleep(3)
#     if file is not None:
#         df = pd.read_csv(file)
#     else:
#         df = pd.read_csv(file)
#     return(df)
# #######################################
# # load flight schedule
# # load model
# # load look up table
# # input box
# delay = "MODEL OUTPUT"
# flight_schedule = load_file('data/flight_schedule.csv')
# airport_cities = load_file('data/airport_cities.csv')
# airport_list = airport_cities[["AIRPORT"]].sort_values("AIRPORT")
# airlines = load_file('data/airline_list.csv')
# airline_list = airlines[['Description']].sort_values("Description")

# ############################################
# st.write("Enter Flight Information")
# d = st.date_input("When is your flight", value = None)
# t = st.time_input("What time is your flight", value = None)
# origin = st.selectbox("Origin Airport", airport_list, index = None, placeholder = "Select Origin airport")
# destination = st.selectbox("Destination Airport", airport_list, index = None, placeholder= "Select Destination Airport")
# airline = st.selectbox("Airline", airline_list, index = None, placeholder= "Select Airline")

# #############################

# ## All the Logic and stuff

# ###########################

# st.write("Your flight is delayed " + delay + " minutes on average.")

# st.write("Other Flight Options:")
# st.write("PLACEHOLDER FOR OPTIONS LOGIC")
# # avg delay
# # other options
