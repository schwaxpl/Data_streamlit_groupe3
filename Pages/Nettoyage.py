import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import missingno as msno
import matplotlib.pyplot as plt

def Nettoyage():

    st.title('Nettoyage des données')

    if("data" in st.session_state):
        data = st.session_state["data"]

        # Affichage des colonnes
        with st.expander('Information des colonnes'):
            st.markdown('## Information des colonnes')
            display_option = st.radio('Choisissez une option', ['Afficher toutes les colonnes', 'Sélectionner des colonnes'])

            if display_option == 'Afficher toutes les colonnes':
                st.subheader('Dataframe complet')
                st.write(data)
            else:
                selected_columns = st.multiselect('Sélectionnez les colonnes à afficher', data.columns)

                if selected_columns:
                    st.subheader('Dataframe avec les colonnes sélectionnées')
                    st.write(data[selected_columns])
                else:
                    st.warning('Veuillez sélectionner au moins une colonne.')

            # Onglet Info de la colonne
            list_columns = list(data.columns)
            onglet_info = st.tabs(list_columns)

            for idx, col_name in enumerate(list_columns):
                with onglet_info[idx]:
                    st.text(f'Nombre de valeurs non nulles : {data[col_name].count()}')
                    st.text(f'Type de données : {data[col_name].dtype}')
                    st.text(f'Nombre de valeurs uniques : {data[col_name].nunique()}')

        # Choix des colonnes
        with st.expander('Choix des colonnes'):
            st.markdown('## Choix des colonnes')
            columns_to_drop = st.multiselect('Sélectionnez les colonnes inutiles à supprimer', data.columns)

            if st.button('Supprimer les colonnes sélectionnées'):
                if columns_to_drop:
                    data = data.drop(columns=columns_to_drop, axis=1)
                    st.success('Colonnes supprimées avec succès.')
                else:
                    st.warning('Veuillez sélectionner au moins une colonne à supprimer.')

                # Bouton pour revenir en arrière
            if st.button('Revenir en arrière'):
                data = pd.DataFrame(data)
                st.success('Opération annulée. Dataframe réinitialisé.')

            st.subheader('Dataframe mis à jour')
            st.write(data)

        # Imputation / Remplacement des NaN
        with st.expander('Imputation et remplacement des valeurs manquantes'):
            st.markdown('## Imputation des valeurs manquantes')
            missing_values = data.isnull().sum()
            st.table(missing_values.reset_index().rename(columns={0: 'Nombre de valeurs manquantes'}).style.highlight_null()) # Affichage des Nan
            st.set_option('deprecation.showPyplotGlobalUse', False)
            msno.matrix(data)
            # fig, ax = plt.subplots()
            # ax.scatter([1, 2, 3], [1, 2, 3])
            st.pyplot()


    else:
        st.text("Bienvenue, allez dans file upload pour charger un CSV")

Nettoyage()