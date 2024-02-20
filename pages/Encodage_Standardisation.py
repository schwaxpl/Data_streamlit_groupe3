import streamlit as st
import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import streamlit_extras
import Utils.Utils as u

u.init_page("Encodage_Standardisation")

def Encodage_Standardisation():

    st.title('Encodage et Standardisation des données')

    if("data" in st.session_state):
        data = st.session_state["data"]

        # Encodage des données
        with st.expander('Encodage'):
            def replace_values_widget(data, column):
                st.subheader('Remplacement de valeurs dans une colonne')

                # Sélectionner une colonne pour le remplacement
                selected_column = st.selectbox('Sélectionnez une colonne:', data.columns)

                # Afficher les valeurs uniques de la colonne sélectionnée
                unique_values = data[selected_column].unique()
                st.write(f"Valeurs uniques dans la colonne '{selected_column}':")
                st.write(unique_values)

                # Ajouter un widget pour spécifier la valeur à remplacer
                value_to_replace = st.text_input('Valeur à remplacer:', '')

                # Ajouter un widget pour spécifier la nouvelle valeur
                new_value = st.text_input('Nouvelle valeur:', '')

                # Bouton pour effectuer le remplacement
                if st.button('Remplacer les valeurs'):
                    if value_to_replace != '' and new_value != '':
                        # Remplacer les valeurs dans la colonne sélectionnée
                        data[column] = data[column].replace(value_to_replace, new_value)
                        st.success(f'Valeurs dans la colonne "{selected_column}" remplacées avec succès.')
                    else:
                        st.warning('Veuillez entrer une valeur à remplacer et une nouvelle valeur.')

                    # Afficher le DataFrame mis à jour
                    st.subheader('Dataframe mis à jour')
                    st.write(data)





    else:
        st.text("Bienvenue, allez dans file upload pour charger un CSV")

Encodage_Standardisation()