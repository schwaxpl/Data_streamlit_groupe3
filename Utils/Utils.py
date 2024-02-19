import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

def init_page(page):
    st.set_page_config(layout="wide")
    st.write('''<style>[data-testid="stHorizontalBlock"] [data-testid="column"]:has(div.page_actuelle) p {color: #bbff00;font-weight:bold;}</style>''', unsafe_allow_html=True)
    bandeau(page)

    
    if("data" in st.session_state and "nom_dataset" in st.session_state):
        nom_dataset = st.session_state["nom_dataset"]
        st.text("Vous travaillez sur le dataset " + str(nom_dataset) )
    if("model" in st.session_state):
        st.text("Vous avez un modèle en cours d'utilisation")


def reset_select():
    st.session_state.selection1 = ""
    st.session_state.selection2 = ""
    st.session_state.selection3 = ""
    st.session_state.selection4 = ""
    st.session_state.selection5 = ""
    st.session_state.reset_select = False

    

def bandeau(page):
    col1,col2,col3,col4,col5 = st.columns(5)
    choix = ""
    if("reset_select" in st.session_state):
        if(st.session_state.reset_select==True):
            reset_select()
    with col1:
        choix_col = st.selectbox("Import / Export données",("","Import","Export"),key="selection1")
        if(page in ("File_upload","Export_Data")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col

    with col2:
        choix_col = st.selectbox("Data Management",("","Statistiques", "Nettoyage"),key="selection2")
        if(page in ("Statistiques","Nettoyage")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col

    with col3:
        choix_col = st.selectbox("Preparation",("", "Encoding & Standardisation"),key="selection3")
        if(page in ("Encoding & Standardisation")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col

    with col4:
        choix_col = st.selectbox("Model Creation",("","Model Training","Model Evaluation","Model Tuning"),key="selection4")
        if(page in ("Model Training","Model Evaluation","Model Tuning")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col
    with col5:
        choix_col = st.selectbox("Output",("","Predict", "Import/export modèle"),key="selection5")
        if(page in ("Predict", "Import/export modèle")):
            st.write("""<div class='page_actuelle'/>""", unsafe_allow_html=True)
        if(choix_col != ""):
            choix = choix_col

    if(choix != ""):
        st.session_state.reset_select = True

        MATCH = {
            'Import': "File_upload",
            'Export': "Export_Data",
            "Statistiques":"Statistiques_generales",
            "Nettoyage":"Nettoyage",
            "Import/export modèle":"Model_IO"

        }
        try:
            switch_page(MATCH[choix])
        except KeyError:
            st.text("Page " + choix + " non trouvée")