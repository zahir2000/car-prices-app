# main.py

import streamlit as st
from home import app as home_app
from price_prediction import app as price_prediction_app
from price_changes import app as price_changes_app

st.set_page_config(layout="centered", page_title="Car Prices App", page_icon="🚗")

# Dictionary of pages
PAGES = {
    "Home": home_app,
    "Car Price Prediction": price_prediction_app,
    "Price Changes": price_changes_app
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Call the app function based on the selection
page_function = PAGES[selection]
page_function()
