import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import missingno as msno
import matplotlib.pyplot as plt
import streamlit_extras
import Utils.Utils as u

u.init_page("Nettoyage")

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
            undo_columns_button_id = 'undo_columns_button'
            if st.button('Revenir en arrière', key=undo_columns_button_id):
                data = pd.DataFrame(data)
                st.success('Opération annulée. Dataframe réinitialisé.')

            st.subheader('Dataframe mis à jour')
            st.write(data)

       # Imputation / Remplacement des NaN
        with st.expander('Imputation et remplacement des valeurs manquantes'):
            st.markdown('## Imputation des valeurs manquantes')
            st.markdown('### Information des valeurs manquantes :')
            missing_values = data.isnull().sum()
            st.table(missing_values.reset_index().rename(columns={0: 'Nombre de valeurs manquantes'}).style.highlight_null()) # Affichage des Nan
            st.set_option('deprecation.showPyplotGlobalUse', False) 
            msno.matrix(data)
            st.pyplot()

            st.markdown('### Remplacer / supprimer des valeurs manquantes :')
            selected_column = st.selectbox('Sélectionnez une colonne:', data.select_dtypes('number').columns)
            replace_button_id_median = f'replace_button_median_{selected_column}'
            replace_button_id_specific = f'replace_button_specific_{selected_column}'
            return_button_id = f'return_button_{selected_column}'
            replace_button_id_dropna = f'replace_button_dropna_{selected_column}'

            old_value = st.text_input('Valeur à remplacer:', type='default')
            new_value = st.text_input('Nouvelle valeur:', type='default')

            if st.button(f'Remplacer les valeurs ({selected_column})', key=replace_button_id_specific):
                try:
                    old_value = eval(old_value) 
                    data[selected_column].replace(old_value, new_value, inplace=True)
                    st.success(f'Valeurs "{old_value}" dans la colonne "{selected_column}" remplacées par "{new_value}" avec succès.')
                except:
                    st.error('Erreur : Veuillez entrer une valeur valide.')

            if st.button('Remplacer les valeurs manquantes par la médiane', key=replace_button_id_median):
                median_value = data[selected_column].median()
                data[selected_column].fillna(median_value, inplace=True)
                st.success(f'Valeurs manquantes dans la colonne "{selected_column}" remplacées avec succès.')

            if st.button('Supprimer les valeurs manquantes restantes',key=replace_button_id_dropna):
                data.dropna(inplace=True)
                st.success('Valeurs manquantes restantes supprimées avec succès.')

            if st.button('Revenir en arrière', key=return_button_id):
                data = pd.DataFrame(data)
                st.success('Opération annulée. Dataframe réinitialisé.')

            st.subheader('Dataframe mis à jour')
            st.write(data)


            missing_values = data.isnull().sum()
            st.table(missing_values.reset_index().rename(columns={0: 'Nombre de valeurs manquantes'}).style.highlight_null())

        # Transformation des données
        with st.expander('Transformation des données'):
            st.markdown('## Transformation des données')

            # sur une colonne
            st.subheader('Dataframe original')
            st.write(data)

            selected_column = st.selectbox('Sélectionnez une colonne:', data.columns)
            separator_pattern = st.text_input('Motif de séparation (ex: espace, V, -, etc.)', '')
            transformation_code = st.text_area('Code de transformation (utilisez "x" comme variable pour la valeur courante)', '')

            def custom_transform(value, separator_pattern, transformation_code):
                try:
                    if isinstance(value, (str, int, float)):
                        value = str(value)

                        transformed_value = eval(transformation_code.replace('x', 'value'))
                        return transformed_value
                except:
                    pass
                
                return value

            data[selected_column + '_transformed'] = data[selected_column].apply(custom_transform, args=(separator_pattern, transformation_code))



            st.subheader('Dataframe mis à jour')
            st.write(data)



    else:
        st.text("Bienvenue, allez dans file upload pour charger un CSV")

Nettoyage()