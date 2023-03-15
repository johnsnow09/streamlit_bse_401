import streamlit as st


############### Custom Functions      ###############


# from: https://discuss.streamlit.io/t/how-to-add-extra-lines-space/2220/7
def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

############### Custom Functions Ends ###############


st.set_page_config(
    page_title="BSE Stocks App",
    page_icon="💰",
)

st.title("Welcome to the BSE Stock Analysis App")
# st.header("This is Home Page")
# st.sidebar.success('Page Navigation')


# calling Vertical space function
v_spacer(height=6)


box_left,_1 = st.columns([3,1],gap = "large")

with box_left:
    st.write("This **App** contains Data about **Indian Stocks** from **BSE**. \
               \n It uses **'Polars'** to handle **large data** processing  \n \
               \n Data downloaded from R library -  \n \
             https://github.com/ilangurudev/IndianStocksR.  \n \
             \n  Data was further saved into **RDS** & **Parquet** file formats which is further read using **polars**.")
    

# calling Vertical space function
v_spacer(height=6)

_2,box_right = st.columns([2,2],gap = "large")

with box_right:
    st.write('<p style="color:grey;"><i>Caption:</i></p>', 
            unsafe_allow_html=True)
    st.write("Created by - **Vineet**  \n \
             using **Python** and data downloaded using:  \n **R** library", 
             unsafe_allow_html=True)
    

