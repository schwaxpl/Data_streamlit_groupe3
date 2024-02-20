import streamlit as st
import pandas as pd
import Utils.Utils as u
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings

from pylab import *

from sklearn.decomposition import PCA
from sklearn import preprocessing 
import seaborn as sns
from sklearn import neighbors
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import model_selection
from sklearn.linear_model import LogisticRegressionCV
from sklearn.svm import SVC 
u.init_page("Entrainement")
if("data" in st.session_state):
    data = st.session_state["data"]
    y = data["target"]
    X = data.drop("target",axis=1)
    if("train_test" in st.session_state):
        X_train, X_test, y_train, y_test = st.session_state["train_test"][0],st.session_state["train_test"][1],st.session_state["train_test"][2],st.session_state["train_test"][3]
    if "target" in data.columns:
        with st.expander("Données",True):
            st.text("La colonne target contient "+str(data["target"].value_counts().count())+" valeurs différentes, voici le top 5:")
            st.dataframe(data["target"].value_counts().head())
            st.text("Le jeu de données contient "+str(data["target"].count()) + " lignes")
            split = st.slider("Split Train / Test",0,100,33,1)
            generer_split = st.button("Découper")

            if(generer_split):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split/100.0, random_state=42)
                st.text(str(len(X_train)) + " lignes d'entrainement")
                st.text(str(len(X_test)) + " lignes de test")
                st.session_state["train_test"] = (X_train, X_test, y_train, y_test) 

    with st.expander("Modèle"):
        try:
            __test = X_train
            init_train = False
        except NameError:
            init_train = True
        tab_reg,tab_clas,tab_clus,tab_dim = st.tabs(["Regression","Classification","Clustering","Réduction des dimensions"])
        with tab_reg:
            algo = st.selectbox("Choisissez un modèle",("","Régression","SVR","pouet"))
            warnings.filterwarnings("ignore")
            if algo != "":
                if init_train:
                        st.text("Aucun jeu de test créé, initialisé avec des paramètres par défaut")
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
                        st.text(str(len(X_train)) + " lignes d'entrainement")
                        st.text(str(len(X_test)) + " lignes de test")
                else:
                    st.text("Le jeu de données de test personnalisé a été utilisé")

                bt_trainr = st.button("Entrainer le modèle",key="bt_trainr")

        with tab_clas:
            algo = st.selectbox("Choisissez un modèle",("","Régression Logistique","K Nearest Neighbours","SVC"))
            if algo != "":
                
                
                if init_train:
                    st.text("Aucun jeu de test créé, initialisé avec des paramètres par défaut")
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
                    st.text(str(len(X_train)) + " lignes d'entrainement")
                    st.text(str(len(X_test)) + " lignes de test")
                else:
                    st.text("Le jeu de données de test personnalisé a été utilisé")
                if(algo == "K Nearest Neighbours"):
                    txt_voisins = st.text_input("Nombre de voisins")
                bt_trainc = st.button("Entrainer le modèle",key="bt_trainc")
                if bt_trainc:
                    if algo == "Régression Logistique":
                        st.title("Génération du modèle Regression Logistique")
                        model = LogisticRegressionCV(cv=5, random_state=0)
                    if algo == "K Nearest Neighbours":
                        if str(txt_voisins).isdigit():
                            nb_voisins = int(txt_voisins)
                        else:
                            nb_voisins = 10
                        if nb_voisins>len(X_train):
                            nb_voisins = int(np.floor(len(X_train)/2))
                            st.text("nombre de nb_voisins ajusté à " + str(nb_voisins))
                        if nb_voisins>len(X_test):
                            nb_voisins = int(np.floor(len(X_test)/2))
                            st.text("nombre de nb_voisins ajusté à " + str(nb_voisins))
                        model = neighbors.KNeighborsClassifier(n_neighbors = nb_voisins)
                    if algo == "SVC":
                        model = SVC(kernel='linear')
                    with st.spinner("Veuillez patienter pendant l'entrainement du modèle"):
                        

                        #--------------------------------------
                        my_kfold =    model_selection.KFold(n_splits=10, shuffle=True, random_state=0)
                        scores = model_selection.cross_val_score(estimator=model,
                                                X=X,
                                                y=y,
                                                cv=my_kfold,
                                                n_jobs=-1) 
                        st.text("Moyenne du score du modèle: " + str(mean(scores)))
                        from sklearn.model_selection import cross_val_score, KFold
                    st.text("Matrice de confusion : ")
                    model.fit(X_train, y_train)
                    predictions_log=model.predict(X_test)
                    cm = confusion_matrix(y_test, predictions_log)
                    fig, ax = plt.subplots()
                    sns.set_theme(font_scale=1.2)  # Adjust font size
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                    plt.title('Confusion Matrix')
                    st.write(fig)
                    st.session_state["Data"] = data
                    st.session_state["model"] = model
                    st.text("Modèle sauvegardé !")
        with tab_clus:
            st.text("WIP : Cette fonctionnalité sera disponible prochainement")
        with tab_dim:
            st.text("WIP : Cette fonctionnalité sera disponible prochainement")

else:
    st.text("Bienvenue, allez dans file upload pour charger un CSV")