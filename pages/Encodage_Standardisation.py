import streamlit as st
import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import streamlit_extras
import Utils.Utils as u
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,StandardScaler,MinMaxScaler


u.init_page("Encodage_Standardisation")

def Encodage_Standardisation():

    st.title('Encodage et Standardisation des données')

    if("data" in st.session_state):
        data = st.session_state["data"]

        # Encodage des données
        with st.expander('Encodage'):
                st.markdown('## Encodage des données')
                
                selected_column = st.selectbox('Sélectionnez une colonne:', data.columns, key='key_1_for_selectbox')

                unique_values = data[selected_column].unique()
                st.write(f"Valeurs uniques dans la colonne '{selected_column}':")
                st.write(unique_values)

                # Bouton pour encodage binaire 
                # if st.button('Encodage binaire (One Hot)',key='button_one_hot'):
                #     encoded_data = pd.get_dummies(data[selected_column], prefix=selected_column)
                #     data = pd.concat([data, encoded_data], axis=1)
                #     data = data.drop(selected_column, axis=1)
                #     st.success(f'Encodage One-Hot de la colonne "{selected_column}" effectué avec succès.')

                # Bouton pour encodage de variables catégoriques nominales
                if st.button('Encoder des variables catégoriques nominales',key='button_one_hot_encoder'):
                    one_hot_encoder = OneHotEncoder(sparse=False, drop='first')
                    encoded_data = one_hot_encoder.fit_transform(data[[selected_column]])
                    columns_encoded = [f'{selected_column}_{int(category)}' for category in one_hot_encoder.get_feature_names_out()]
                    encoded_df = pd.DataFrame(encoded_data, columns=columns_encoded)
                    data = pd.concat([data, encoded_df], axis=1)
                    data = data.drop(selected_column, axis=1)
                    st.success(f'One-Hot Encoder appliqué avec succès sur la colonne "{selected_column}".')

                # Bouton pour encodage de variables catégoriques ordinales
                encoder = OrdinalEncoder()
                if st.button('Encoder des variables catégoriques ordinales',key='button_ordinal_encoder'):
                    data[selected_column] = encoder.fit_transform(data[[selected_column]])


                st.subheader('Dataframe mis à jour')
                st.dataframe(data)
                st.session_state["data"] = data

        # Standardisation des données
        with st.expander('Standardisation'):
            st.markdown('## Standardisation des données')

            selected_columns = st.multiselect('Sélectionnez les colonnes à standardiser:', data.select_dtypes(include=['float64', 'int64']).columns)

            # Bouton de standardisation au Z score
            if selected_columns:
                if st.button('Standardiser au Z score', key='button_standard_scaler'):
                    scaler = StandardScaler()
                    data[selected_columns] = scaler.fit_transform(data[selected_columns])
                    st.success(f'Colonnes {selected_columns} standardisées avec StandardScaler.')

            # Bouton de standardisation au min/max
            if selected_columns:
                if st.button('Appliquer Min-Max Scaling aux colonnes sélectionnées', key='button_min_max_scaler'):
                    scaler = MinMaxScaler()
                    data[selected_columns] = scaler.fit_transform(data[selected_columns])
                    st.success(f'Colonnes {selected_columns} appliquées avec succès Min-Max Scaling.')

            st.subheader('Dataframe mis à jour')
            st.dataframe(data)
            st.session_state["data"] = data

    else:
        st.text("Bienvenue, allez dans file upload pour charger un CSV")

Encodage_Standardisation()