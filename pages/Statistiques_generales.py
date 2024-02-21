import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

nb_catcolumn=0
nb_numcolumn=0

if("data" in st.session_state):
    data = st.session_state["data"]

    with st.expander("Column Type"):    
        st.subheader("Column Data Types:") # Iterate over each column and display if it's categorical or numerical
        for column_name in data.columns:
            if data[column_name].dtype == 'object':
                nb_catcolumn+=1
            else:
                nb_numcolumn+=1
        st.write(f"The dataset contains {nb_catcolumn} categorical columns and " f"{nb_numcolumn} numerical columns")

        st.subheader("Data types of each column:") # Check data types of each column
        st.write(data.dtypes)
    
    if nb_catcolumn !=0:    
        with st.expander("Matrice de correlation"):
            data_numeric = data.apply(pd.to_numeric, errors='coerce')
            st.dataframe(data_numeric.corr())
            fig, ax = plt.subplots()
            sns.heatmap(data_numeric.corr(), ax=ax,)
            st.write(fig)
    else:
        with st.expander("Matrice de correlation"):
            st.dataframe(data.corr())
            fig, ax = plt.subplots()
            sns.heatmap(data.corr(), ax=ax,)
            st.write(fig)

    with st.expander("Pairplot visualization"):
        st.pyplot(sns.pairplot(data,hue="target"))
    
    with st.expander("Représentation des données par histogramme"):
        fig, ax = plt.subplots()
        data.hist(figsize=(20, 20))
        st.write(fig)
      
    
    with st.expander("Description des données"):
        st.dataframe(data.describe())

    with st.expander("Informations"):
        st.dataframe(data.info())

    with st.expander("Usage mémoire"):
        st.dataframe(data.memory_usage())

    
else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")

