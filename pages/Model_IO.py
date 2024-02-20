import streamlit as st
import pandas as pd
import Utils.Utils as u
import joblib
import io

u.init_page("Import/export modèle")
@st.cache_data
def convert_mod(_model_to_dump):
    joblib.dump(_model_to_dump,"model.pkl")
    
file = st.file_uploader(label="Mettez votre modèle",type="pkl",accept_multiple_files=False)

if file:
    model = joblib.load(file)
    st.text("Modele chargé avec succès !")
    st.session_state["model"] = model

if "model" in st.session_state:
    model = st.session_state["model"]

    convert_mod(model)

    with open("model.pkl", "rb") as file:
        model_bytes = file.read()
        st.download_button(
        "Télécharger le modèle",
        model_bytes,
        "Model.pkl",
        mime="application/octet-stream",
        key='download-pkl'
        )
