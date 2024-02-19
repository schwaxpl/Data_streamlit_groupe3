import streamlit as st
import pandas as pd
import numpy as np
import Pages as p
from Utils import Utils as u

u.init_page("Export_Data")

if("data" in st.session_state):
    data = st.session_state["data"]
    @st.cache
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(data)

    st.download_button(
    "Télécharger les données",
    csv,
    "export.csv",
    "text/csv",
    key='download-csv'
    )
    st.dataframe(data)
else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")