import streamlit as st
import pandas as pd
import Utils.Utils as u

u.init_page("File_upload")

file = st.file_uploader(label="Mettez votre CSV",type="csv",accept_multiple_files=False)
txt_sep = st.text_input("Séparateur",",",max_chars=3)
if file:
    sep = ","
    if (txt_sep != ""):
        sep = txt_sep 
    data = pd.read_csv(file,sep=sep)
    st.success("✅ Votre fichier " + str(file.name) + " a été correctement importé. Voici un aperçu des données :" )
    st.dataframe(data.head())
    st.session_state["data"] = data
    st.session_state["nom_dataset"] = str(file.name).split('.')[-2]


