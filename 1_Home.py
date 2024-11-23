import streamlit as st

APP_TITLE = 'PROPOSING PREDICTION OF FLIGHT DELAYS'
APP_SUB_TITLE = 'Source: Bureau of Transportation Statistics bts.gov'



def main():

    ### Page Config
    st.set_page_config(page_title=APP_TITLE, page_icon=":airplane_departure", layout="wide")
    st.markdown("""
        <style>
            .st-emotion-cache-zt5igj {
                color: teal;
                padding-top: 15px;
                padding-bottom: 15px;
            }
        </style>""", unsafe_allow_html=True)
    st.title(f":satellite: {APP_TITLE} :airplane_departure:")
    # st.caption(APP_SUB_TITLE)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    
    with open('lib/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        :gray[A Streamlit App to analyze and predict the expected Flight Delays based on weather, airlines and flight origin-destination]
        * :gray[**Libraries Used:** Streamlit, Pandas, Plotly]
        * :gray[**Data Source:** bts.gov]
        ''')


    with col2:
        # st.caption("Authors: Sammie Srabani, Neha Korrapati, Leela Josna Kona, Devangi Samal")
        st.markdown('<div style="text-align: right;color:gray";>Author: Sammie Srabani, Neha Korrapati, Leela Josna Kona, Devangi Samal</div>', unsafe_allow_html=True)
        


    with st.container():
        st.image('data/banner.jpg', caption="Image by DSBA 6156 Group1")



if __name__ == "__main__":
    main()