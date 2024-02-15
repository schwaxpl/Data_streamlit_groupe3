import streamlit as st
import pandas as pd


file = st.file_uploader(label="Mettez votre CSV",type="csv",accept_multiple_files=False)

if file:
    data = pd.read_csv(file)
    st.text("Coucou, " + str(file) + " uploadé" )
    st.dataframe(data)
    st.session_state["data"] = data
