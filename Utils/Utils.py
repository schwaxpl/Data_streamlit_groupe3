import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

def init_page(page):
    st.set_page_config(layout="wide")
    st.write('''<style>[data-testid="stHorizontalBlock"] [data-testid="column"]:has(div.page_actuelle) p {color: #bbff00;font-weight:bold;}</style>''', unsafe_allow_html=True)
    bandeau(page)

def bandeau(page):
    col1,col2,col3,col4,col5 = st.columns(5)
    choix = ""
    with col1:
        choix_col = st.selectbox("Import / Export données",("","Import","Export"))
        if(page in ("File_upload","Export_Data")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col

    with col2:
        choix_col = st.selectbox("Data Management",("","Statistiques", "Data Cleaning"))
        if(choix_col != ""):
            choix = choix_col

    with col3:
        choix_col = st.selectbox("Preparation",("", "Encoding & Standardisation"))

    with col4:
        choix_col = st.selectbox("Model Creation",("","Model Training","Model Evaluation","Model Tuning"))

    with col5:
        choix_col = st.selectbox("Output",("","Predict", "Download Model"))

    if(choix != ""):
        match choix:
            case "Import":
                switch_page("File_upload")
            case "Export":
                switch_page("Export_Data")
            case "Statistiques":
                switch_page("Statistiques_generales")