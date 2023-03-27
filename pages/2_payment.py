import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3

st.title("Payment")
st.write("Choose payment method")
choice = st.selectbox("Pick one", [""" Cash""","Mpesa"])
