import streamlit as st
import pandas as pd
import Utils.Utils as u
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings

u.init_page("Entrainement")
if("data" in st.session_state):
    data = st.session_state["data"]
    if "target" in data.columns:
        with st.expander("Données",True):
            st.text("La colonne target contient "+str(data["target"].value_counts().count())+" valeurs différentes, voici le top 5:")
            st.dataframe(data["target"].value_counts().head())
            st.text("Le jeu de données contient "+str(data["target"].count()) + " lignes")
            split = st.slider("Split Train / Test",0,100,33,1)
            generer_split = st.button("Découper")
            y = data["target"]
            X = data.drop("target",axis=1)
            if(generer_split):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split/100.0, random_state=42)
                st.text(str(len(X_train)) + " lignes d'entrainement")
                st.text(str(len(X_test)) + " lignes de test")

    with st.expander("Modèle"):
        tab_reg,tab_clas,tab_clus,tab_dim = st.tabs(["Regression","Classification","Clustering","Réduction des dimensions"])
        with tab_reg:
            st.selectbox("Choisissez un modèle",("Régression","SVR","pouet"))
            warnings.filterwarnings("ignore")

        with tab_clas:
            algo = st.selectbox("Choisissez un modèle",("Régression Logistique","K Nearest Neighbours","SVC"))
            clf = LogisticRegression()
            clf.fit(X_train, y_train)
        with tab_clus:
            st.text("WIP : Cette fonctionnalité sera disponible prochainement")
        with tab_dim:
            st.text("WIP : Cette fonctionnalité sera disponible prochainement")

else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")