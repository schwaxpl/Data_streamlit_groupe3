import streamlit as st
import pandas as pd
import numpy as np
import Pages as p
st.title('Projet streamlit groupe 3')

if("data" in st.session_state):
    data = st.session_state["data"]
    st.dataframe(data)
else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")