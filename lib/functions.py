import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt, os
import matplotlib.pyplot as plt
from vega_datasets import data
from datetime import date, timedelta
import plotly.graph_objects as go



def page_config():
    APP_TITLE = 'PROPOSING PREDICTION OF FLIGHT DELAYS'
    APP_SUB_TITLE = 'Source: Bureau of Transportation Statistics bts.gov for Period between 2020/01/01 and 2022/12/01'
    APP_SUB_TITLE2 = 'Date Range: 2020/01/01 to 2022/12/01'

    st.set_page_config(page_title=APP_TITLE, page_icon=":airplane_departure", layout="wide")
    st.title(f":satellite: {APP_TITLE} :airplane_departure:")
    st.caption(APP_SUB_TITLE)
    st.caption(APP_SUB_TITLE2)
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

def session_assign(filtered_df, date1, date2, state, county):
    st.session_state['my_df'] = filtered_df
    st.session_state["my_date1"] = date1
    st.session_state["my_date2"] = date2
    st.session_state["my_state"] = state
    st.session_state["my_county"] = county


def agePeriod_chart(df):
        fig = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("case_month:O").timeUnit("yearmonth").title("Month Year"),
            y="Total:O",
            color=alt.Color("age_group:N", title="Age Group").scale(scheme="tealblues")
        ).transform_window(
            rank="rank()",
            sort=[alt.SortField("Total", order="descending")],
            groupby=["case_month"]
        ).properties(
            # title="Bump Chart for Stock Prices",
            width=600,
            height=700,
        ).configure_point(
        size=150
        )

        fig2 = alt.Chart(df).mark_line(strokeWidth = 2, point=True).encode(
                # x='case_month:T',
                x=alt.X("case_month:T").title("Date"),
                y='Total:Q',
                color=alt.Color("age_group:N", title="Age Group")
            ).configure_point(
                size=150
            )

        st.altair_chart(fig2, use_container_width=True, theme="streamlit")


def ageGender_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Violin(x=df['age_group'][ df['gender'] == 'Male' ],
                        y=df['Total'][ df['gender'] == 'Male' ],
                        legendgroup='M', scalegroup='M', name='M',
                        line_color='teal')
             )
    fig.add_trace(go.Violin(x=df['age_group'][ df['gender'] == 'Female' ],
                        y=df['Total'][ df['gender'] == 'Female' ],
                        legendgroup='F', scalegroup='F', name='F',
                        line_color='pink')
             )
    fig.add_trace(go.Violin(x=df['age_group'][ df['gender'] == 'Other' ],
                        y=df['Total'][ df['gender'] == 'Other' ],
                        legendgroup='Other', scalegroup='Other', name='Other',
                        line_color='lightgrey')
             )

    fig.update_traces(box_visible=True, meanline_visible=True)
    fig.update_layout(violinmode='group',
                      xaxis_title="Age Group",
                      yaxis_title="Vaccination Count",
                      legend_title="Gender"
                     )

    st.plotly_chart(fig, use_container_width=True)

def ethnicity_chart(df):
    base = alt.Chart(df).mark_arc(innerRadius=50).encode(
        theta="Total:Q",
        color=alt.Color("ethnicity:N", title="Ethnicity").scale(scheme="lighttealblue")
    )
    
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=160, size=20).encode(text="Total:Q")

    st.altair_chart(pie + text, use_container_width=True, theme="streamlit")

def race_chart(df):

    fig = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("case_month:O").timeUnit("yearmonth").title("Month Year"),
        y="Total:O",
        color=alt.Color("race:N", title="Race")#.scale(scheme="tealblues")
    ).transform_window(
        rank="rank()",
        sort=[alt.SortField("Total", order="descending")],
        groupby=["case_month"]
    ).properties(
        # title="Bump Chart for Stock Prices",
        width=600,
        height=700,
    ).configure_point(
    size=150
    )

    st.altair_chart(fig, use_container_width=True, theme="streamlit")

def county_rank(df):
    source = df
    plot = alt.Chart(source).transform_aggregate(
            count='sum(Total)',
            groupby=['res_state', 'res_county']
            ).transform_window(
            rank='rank(count)',
            sort=[alt.SortField('count', order='descending')]
            ).transform_filter(
            alt.datum.rank < 55
            ).mark_bar().encode(
            alt.Y('res_state:N').sort('-x').title('State'),
            alt.X('count:Q').title('Count'),
            color=alt.Color('res_county', title='County').scale(scheme="lighttealblue")
            )


    st.altair_chart(plot, use_container_width=True, theme="streamlit")

def county_map(df, df2):
    states = alt.topo_feature(data.us_10m.url, 'states')
    counties = alt.topo_feature(data.us_10m.url+"#", 'counties')
    max = df['Total'].max()
    source = df
    alt.data_transformers.enable("vegafusion")
    alt.data_transformers.disable_max_rows()
    
    foreground = alt.Chart(counties).mark_geoshape().encode(
        color=alt.Color('Total:Q', scale=alt.Scale(domain=[0, max], scheme="lighttealblue"),title='# of Vaccinations'),
        # color=alt.Color('Total:Q', title='# of Vaccinations'),
        # color=alt.value('steelblue'),
        tooltip=['res_state:N', 'res_county:N', 'Total:Q'] 
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(source, 'county_fips_code', ['res_state', 'res_county', 'Total'])
        ).project(
            type='albersUsa'
        ).properties(
            width=700,
            height=400
            ).interactive()  
    
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='steelblue',  fillOpacity=0
        ).encode(
            tooltip=['res_state:N', 'Total:Q'] #,type= "circle"
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(df2, 'state_fips_code', ['res_state','Total'])
        ).project(
            type='albersUsa'
        ).properties(
            width=700,
            height=400
        ).interactive()  
    
    fig = alt.layer(background, foreground)
    # fig =  background + foreground
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.altair_chart(fig, use_container_width=True, theme="streamlit")

def date_filter(df):

    with st.container(border=True):
    ### Date Filter
        col1, col2 = st.columns(2)
        df["case_month"] = pd.to_datetime(df["case_month"])

        # startDate = pd.to_datetime(df["case_month"]).min()
        # endDate = pd.to_datetime(df["case_month"]).max()

        today = date.today()
        # date_1 = today - timedelta(days=1074)
        # date_2 = date_1 + timedelta(days=30)

        if "my_date1" in st.session_state:
            if "my_date2" in st.session_state:
                startDate = st.session_state["my_date1"]
                endDate = st.session_state["my_date2"]

        if "my_date1" not in st.session_state:
            if "my_date2" not in st.session_state:
                startDate = pd.to_datetime('2021/01/01')
                endDate = pd.to_datetime('2021/05/31')

        with col1:
            date1 = pd.to_datetime(st.date_input("**Start Date**", startDate))
        with col2:
            date2 = pd.to_datetime(st.date_input("**End Date**", endDate))

        df = df[(df["case_month"] >= date1) & (df["case_month"] <= date2)].copy()
    return(df, date1, date2)

def sidebar_filters(df):

    st.sidebar.header("Choose your filter:")

    state = st.sidebar.multiselect("**Pick your State**", options=df.sort_values(by="res_state").res_state.unique())

    if not state:
        df2 = df.copy()
    else:
        df2 = df[df["res_state"].isin(state)]

    county = st.sidebar.multiselect("**Pick your County**", options=df2.sort_values(by="res_county").res_county.unique())#, default=st.session_state["my_county"])

    if not county:
        df3 = df2.copy()
    else:
        df3 = df2[df2["res_county"].isin(county)]

    # Filter the data based on State, County, demographics, metrics 

    if not state and not county:
        filtered_df = df
    elif state and county:
        filtered_df = df3[df["res_state"].isin(state) & df3["res_county"].isin(county)]
    elif county:
        filtered_df = df3[df3["res_county"].isin(county)]
    elif state:
        filtered_df = df3[df3["res_state"].isin(state)]
    # else:
    #     filtered_df = df3[df3["Region"].isin(region) & df3["State/Province"].isin(state) & df3["City"].isin(city)]
    return(filtered_df, state, county)

def session_values():

    if "my_state" not in st.session_state:
        st.session_state["my_state"] = ""

    if state:
        st.session_state["my_state"] = state
        st.write("You have entered: ", st.session_state["my_state"])
    
    if "my_county" not in st.session_state:
        st.session_state["my_county"] = ""

    if county:
        st.session_state["my_county"] = county
        st.write("You have entered: ", st.session_state["my_county"])

    if "my_date1" not in st.session_state:
        st.session_state["my_date1"] = ""

    if date1:
        st.session_state["my_date1"] = date1
        st.write("You have entered: ", st.session_state["my_date1"])   

    if "my_date2" not in st.session_state:
        st.session_state["my_date2"] = ""

    if date2:
        st.session_state["my_date2"] = date2
        st.write("You have entered: ", st.session_state["my_date2"])  
    
    # return state, county, date1, date2



def sidebar_filters2(df):

    st.sidebar.header("Choose your filter:")
    state = st.sidebar.multiselect("**Pick your State**", options=df.sort_values(by="res_state").res_state.unique(), default='NC')
    
    if not state:
        df2 = df.copy()
    else:
        df2 = df[df["res_state"].isin(state)]

    county = st.sidebar.multiselect("**Pick your County**", options=df2.sort_values(by="res_county").res_county.unique(), default='MECKLENBURG')

    if not county:
        df3 = df2.copy()
    else:
        df3 = df2[df2["res_county"].isin(county)]

    # Filter the data based on State, County, demographics, metrics 

    if not state and not county:
        filtered_df = df
    elif state and county:
        filtered_df = df3[df["res_state"].isin(state) & df3["res_county"].isin(county)]
    elif county:
        filtered_df = df3[df3["res_county"].isin(county)]
    elif state:
        filtered_df = df3[df3["res_state"].isin(state)]
    # else:
    #     filtered_df = df3[df3["Region"].isin(region) & df3["State/Province"].isin(state) & df3["City"].isin(city)]
    return(filtered_df, state, county)

@st.cache_resource
def load_data():
    df = pd.read_csv("data/COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv")
    # df = pd.read_csv("https://data.cdc.gov/resource/n8mc-b4w4.csv?$query=SELECT%0A%20%20%60res_state%60%2C%0A%20%20%60state_fips_code%60%2C%0A%20%20%60res_county%60%2C%0A%20%20%60county_fips_code%60%2C%0A%20%20%60case_month%60%2C%0A%20%20%60age_group%60%2C%0A%20%20%60sex%60%2C%0A%20%20%60ethnicity%60%2C%0A%20%20%60race%60%2C%0A%20%20count(*)%20AS%20%60count%60%0AWHERE%20%60case_month%60%20BETWEEN%20%222020-01%22%20AND%20%222022-12%22%0AGROUP%20BY%0A%20%20%60res_state%60%2C%0A%20%20%60state_fips_code%60%2C%0A%20%20%60res_county%60%2C%0A%20%20%60county_fips_code%60%2C%0A%20%20%60age_group%60%2C%0A%20%20%60sex%60%2C%0A%20%20%60race%60%2C%0A%20%20%60ethnicity%60%2C%0A%20%20%60case_month%60%0AORDER%20BY%0A%20%20%60res_state%60%20ASC%20NULL%20LAST%2C%0A%20%20%60res_county%60%20ASC%20NULL%20LAST%2C%0A%20%20%60case_month%60%20ASC%20NULL%20LAST%2C%0A%20%20%60age_group%60%20ASC%20NULL%20LAST%2C%0A%20%20%60sex%60%20ASC%20NULL%20LAST%2C%0A%20%20%60ethnicity%60%20ASC%20NULL%20LAST%2C%0A%20%20%60race%60%20ASC%20NULL%20LAST")
    df = df.rename(columns={'sex': 'gender'})
    df = df.apply(lambda x: x.replace({'Missing|Unknown':'No Data'}, regex=True))
    # df = df.fillna('Other')
    df = df.reindex(columns=['res_state', 'state_fips_code', 'res_county', 'county_fips_code', 'case_month', 'age_group', 'gender', 'race', 'ethnicity', 'count'])
    return df

