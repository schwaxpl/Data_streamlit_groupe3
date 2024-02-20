import streamlit as st
import pandas as pd
import numpy as np
import missingno as msno
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
            display_option = st.radio('Choisissez une option', ['Afficher toutes les colonnes', 'Sélectionner des colonnes'],key='display_option')

            if display_option == 'Afficher toutes les colonnes':
                st.subheader('Dataframe complet')
                st.dataframe(data)
                st.session_state["data"] = data
            else:
                selected_columns = st.multiselect('Sélectionnez les colonnes à afficher', data.columns,key='selected_columns')

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
            columns_to_drop = st.multiselect('Sélectionnez les colonnes inutiles à supprimer', data.columns,key='columns_to_drop')

            if st.button('Supprimer les colonnes sélectionnées',key='button_drop_columns'):
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
            st.dataframe(data)
            st.session_state["data"] = data

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
            selected_column = st.selectbox('Sélectionnez une colonne:', data.select_dtypes('number').columns,key='key_drop_replace_nan')
            replace_button_id_median = f'replace_button_median_{selected_column}'
            replace_button_id_specific = f'replace_button_specific_{selected_column}'
            return_button_id = f'return_button_{selected_column}'
            replace_button_id_dropna = f'replace_button_dropna_{selected_column}'

            old_value = st.text_input('Valeur à remplacer:', type='default',key='old_value_drop_replace_nan')
            new_value = st.text_input('Nouvelle valeur:', type='default',key='new_value_drop_replace_nan')

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
            st.dataframe(data)
            st.session_state["data"] = data


            missing_values = data.isnull().sum()
            st.table(missing_values.reset_index().rename(columns={0: 'Nombre de valeurs manquantes'}).style.highlight_null())

        # Transformation des données
        with st.expander('Transformation des données'):
            st.markdown('## Transformation des données')

            # Garder des motifs dans les valeurs
            st.markdown('### Garder des motifs dans les valeurs')
            st.subheader('Dataframe original')
            st.dataframe(data)
            st.session_state["data"] = data

            selected_column = st.selectbox('Sélectionnez une colonne:', data.columns,key='key_gader_motifs')
 
            pattern_options = list(set([word.lower() for item in data[selected_column] for word in str(item).split()]))
            selected_pattern = st.selectbox('Sélectionnez un motif dans les valeurs:', pattern_options)
            keep_option = st.radio('Choisissez ce qui sera gardé:', ['Avant le motif', 'Après le motif'])
            apply_to_same_column = st.checkbox('Appliquer la transformation à la même colonne')
            new_column_name = st.text_input('Nom de la nouvelle colonne (si différent de la colonne d\'origine):', key='text_input_new_column_transform_data')
            button_id_motifs = f'button_motifs_{selected_column}'

            def custom_transform(value, selected_pattern, keep_option):
                if isinstance(value, (str, int, float)):
                    words = str(value).split()
                    if selected_pattern.lower() in [word.lower() for word in words]:
                        pattern_index = [word.lower() for word in words].index(selected_pattern.lower())
                        if keep_option == 'Avant le motif':
                            return ' '.join(words[:pattern_index])
                        elif keep_option == 'Après le motif':
                            return ' '.join(words[pattern_index + 1:])
                return value

            if st.button('Valider la transformation',key=button_id_motifs):
                        if apply_to_same_column:
                            data[selected_column] = data[selected_column].apply(custom_transform, args=(selected_pattern, keep_option))
                        else:
                            new_column_name = new_column_name if new_column_name else selected_column + '_transformed'
                            data[new_column_name] = data[selected_column].apply(custom_transform, args=(selected_pattern, keep_option))

            st.subheader('Dataframe mis à jour')
            st.dataframe(data)
            st.session_state["data"] = data

            # Remplacer des valeurs
            st.markdown('### Remplacement de valeurs')
            selected_column = st.selectbox('Sélectionnez une colonne:', data.columns,key='key_replace_val')

            unique_values = data[selected_column].unique()
            st.write(f"Valeurs uniques dans la colonne '{selected_column}':")
            st.write(unique_values)

            value_to_replace = st.text_input('Valeur à remplacer:', '')
            new_value = st.text_input('Nouvelle valeur:', '')

            if st.button('Remplacer les valeurs',key='button_validate_transform_data'):
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

Nettoyage()