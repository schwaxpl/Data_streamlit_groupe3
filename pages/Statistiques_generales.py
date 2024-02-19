import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if("data" in st.session_state):
    data = st.session_state["data"]

    with st.expander("Matrice de correlation"):
        st.dataframe(data.corr())
        fig, ax = plt.subplots()
        sns.heatmap(data.corr(), ax=ax,)
        st.write(fig)

    with st.expander("Description des données"):
        st.dataframe(data.describe())

    with st.expander("Informations"):
        st.dataframe(data.info())

    with st.expander("Usage mémoire"):
        st.dataframe(data.memory_usage())

    
else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")

