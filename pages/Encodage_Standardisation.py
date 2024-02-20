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
                st.markdown('## Encodage')
                st.markdown('### Remplacement de valeurs')

                selected_column = st.selectbox('Sélectionnez une colonne:', data.columns)

                unique_values = data[selected_column].unique()
                st.write(f"Valeurs uniques dans la colonne '{selected_column}':")
                st.write(unique_values)

                value_to_replace = st.text_input('Valeur à remplacer:', '')
                new_value = st.text_input('Nouvelle valeur:', '')

                if st.button('Remplacer les valeurs'):
                    if value_to_replace != '' and new_value != '':
                        data[selected_column] = data[selected_column].replace(value_to_replace, new_value)
                        st.success(f'Valeurs dans la colonne "{selected_column}" remplacées avec succès.')
                    else:
                        st.warning('Veuillez entrer une valeur à remplacer et une nouvelle valeur.')

                    st.subheader('Dataframe mis à jour')
                    st.dataframe(data)
                    st.session_state["data"] = data

            


    else:
        st.text("Bienvenue, allez dans file upload pour charger un CSV")

Encodage_Standardisation()