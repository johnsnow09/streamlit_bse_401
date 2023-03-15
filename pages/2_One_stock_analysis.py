import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
from numerize.numerize import numerize

import plotly.express as px

# https://stackoverflow.com/questions/40996175/loading-a-rds-file-in-pandas
# import pyreadr


# from: https://youtu.be/lWxN-n6L7Zc
# StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.
st.set_page_config(page_title="Streamlit_101",
                    layout='wide',
                    initial_sidebar_state="expanded")


# @st.cache
# @st.cache_data
def get_data():
    df = pl.scan_parquet('df_bse_compiled_3.parquet')
    # df = pl.scan_parquet('V:/1. R & Python work/Python/2.AnalytixLabs Practice/Streamlit 102 Stocks/df_bse_compiled_3.parquet')
    
    # polars automatically took it as date so need for casting
    # df['date'] = pd.to_datetime(df['date'])
    
    return df

df = get_data()


header_left,header_mid,header_right = st.columns([1,3,1],gap = "large")

with header_mid:
    # https://docs.streamlit.io/library/get-started/create-an-app
    st.title("Streamlit app in Polars")
    
    # Create a text element and let the reader know the data is loading.
    # data_load_state = st.text('Loading data...')

with st.sidebar:
    Security_Type = st.multiselect(label="Select Security type",
                                     options=df.lazy().select(pl.col('SC_TYPE')).unique().collect().to_series().to_list() ,
                                     
                                     default= "Q")
    

    ########## Security Group Filteration & List Below ########## 

    Security_Group_List = df.lazy().filter(pl.col('SC_TYPE').is_in(Security_Type)).select(
                                                pl.col('SC_GROUP')).unique().collect().to_series().to_list()

    Security_Group = st.multiselect(label="Select Security type",
                                     options=Security_Group_List,
                                     default=Security_Group_List)
    

    ########## Security Name Filteration & List Below ##########

    Security_Name_List = df.lazy().filter((pl.col('SC_TYPE').is_in(Security_Type)) & 
                                                (pl.col('SC_GROUP').is_in(Security_Group))
                                                ).select(
                                                pl.col('SC_NAME')).unique().collect().to_series().to_list()
    
    Security_Name = st.multiselect(label="Security Name",
                                    options=Security_Name_List,
                                   default="ADANI POWER",
                                   max_selections=1)
    


df_selected = df.lazy().filter((pl.col('SC_TYPE').is_in(Security_Type)) &
                       (pl.col('SC_GROUP').is_in(Security_Group)) & 
                       (pl.col('SC_NAME').is_in(Security_Name))).collect()

Sector_Name = df_selected.select(pl.col('Sector Name')).unique().item()
Industry_Name = df_selected.select(pl.col('Industry')).unique().item()
Industry_Name_New = df_selected.select(pl.col('Industry New Name')).unique().item()
lifetime_high = float(df_selected['CLOSE'].max())
lifetime_low = float(df_selected['CLOSE'].min())

no_1,no_2,no_3,no_4,no_5 = st.columns(5, gap="large")

with no_1:
    st.image('Icons/kick-me.png', use_column_width='Auto')
    st.metric(label='Sector',value=Sector_Name)

with no_2:
    st.image('Icons/banana.png', use_column_width='Auto')
    st.metric(label='Industry',value=Industry_Name)

with no_3:
    st.image('Icons/ninja.png', use_column_width='Auto')
    st.metric(label='Industry New',value=Industry_Name_New)

with no_4:
    st.image('Icons/weight.png', use_column_width='Auto')
    st.metric(label='Highest Price',value=numerize(lifetime_high)) 

with no_5:
    st.image('Icons/glasses.png', use_column_width='Auto')
    st.metric(label='Lowest Price',value=numerize(lifetime_low))



############## Below code is same as above but in 1 column & 2 Rows instead ##############

fig_price_journey = px.line(df_selected.to_pandas(),x='date',y='CLOSE',
                            title=f'<b>{Security_Name} Price Journey</b>')
fig_price_journey.update_xaxes(rangeslider_visible = True)
fig_price_journey.update_layout(xaxis_range = ['2020-01-01','2023-03-10'],
                                showlegend = False,
                                title = {'x':0.5},
                                plot_bgcolor = "rgba(0,0,0,0)",
                                xaxis = (dict(showgrid = False)),
                                yaxis = (dict(showgrid = False)),)

st.plotly_chart(fig_price_journey,use_container_width=True)



df_selected2 = df_selected.clone()
df_selected2 = df_selected2.with_columns((pl.col('CLOSE').pct_change()*100).alias("pct_change"))

# st.table(df_selected2.head().to_pandas())

fig_price_pct = px.line(df_selected2.to_pandas(),x='date',y='pct_change',title=f'<b>{Security_Name} % Price Change</b>')
fig_price_pct.update_xaxes(rangeslider_visible = True)
fig_price_pct.update_layout(xaxis_range = ['2020-01-01','2023-03-10'],
                                showlegend = False,
                                title = {'x':0.5},
                                plot_bgcolor = "rgba(0,0,0,0)",
                                xaxis = (dict(showgrid = False)),
                                yaxis = (dict(showgrid = False)),)

st.plotly_chart(fig_price_pct,use_container_width=True)


