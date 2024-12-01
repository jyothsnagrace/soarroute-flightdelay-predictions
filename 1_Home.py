import streamlit as st
from lib.functions import page_config

APP_TITLE = 'Soarroute Inc: Flight Delay Predictions'
APP_SUB_TITLE = 'Authors: Sammie Srabani, Neha Korrapati, Leela Josna Kona, Devangi Samal'



def main():

    ### Page Config
    page_config()
    
    ### css
    with open('lib/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    ### Data Source
    st.markdown('''
        :gray[A Streamlit App to analyze and predict the expected Flight Delays based on weather, airlines and flight origin-destination]
        * :gray[**Libraries Used:** Streamlit, Pandas, Scikit-Learn, Plotly, Altair]
        * :gray[**Data Source:** Bureau of Transportation Statistics bts.gov]
        ''')
    ### Banner
    with st.container():
        st.image('data/banner1.jpg', use_column_width="always", caption="Example Image")
        # st.markdown(f"<img style='max-width: 100%;max-height: 100%;'/>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()