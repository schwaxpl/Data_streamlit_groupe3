import streamlit as st
import pandas as pd
import Utils.Utils as u
from pylab import *

from sklearn.decomposition import PCA
from sklearn import preprocessing 
import seaborn as sns
from sklearn import neighbors
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import model_selection
from sklearn.linear_model import LogisticRegressionCV
u.init_page("Extras")
with st.expander("Traitement pré configuré ""Vin"" "):
    bt_explo = st.button("Exploration des données pour classification")
    bt_vin = st.button("Générer un modèle KNearest Neighbours",key="vin")
    bt_vin2 = st.button("Générer un modèle de regression linéaire",key="vin2")

    if bt_explo or bt_vin or bt_vin2:
        st.subheader("Resultats")
        if bt_explo:
            if("data" in st.session_state):
                data = st.session_state["data"]
                X=data[data.columns[:-1]]
                Y=data["target"]
                st.title("Exploration des données")
                st.text("Valeurs uniques dans la target :")
                st.dataframe(np.unique(data.iloc[:,-1]))
                st.text("Equilibre du jeu de données :")
                st.dataframe(data.iloc[:,-1].value_counts())
                st.text("Matrice de correlation : ")
                correlation_matrix = pd.DataFrame(X).corr()
                correlation_matrix=correlation_matrix[correlation_matrix>0.5]
                mask = np.triu(correlation_matrix.select_dtypes("number").corr())
                correlation_matrix.index=data.columns[:-1]
                correlation_matrix.columns=data.columns[:-1]
                # Tracé de la heatmap
                fig, ax = plt.subplots()
                sns.heatmap(correlation_matrix, mask=mask,annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5,ax=ax)
                st.write(fig)
                #st.pyplot(plt.barh(width=data.iloc[:,-1].value_counts(),y=data.iloc[:,-1].value_counts().index))
                with st.spinner("Veuillez patienter pendant la génération du graphique"):
                    st.pyplot(sns.pairplot(data,hue="target"))
            else:
                st.text("Veuillez importer un dataset")
        if bt_vin:
            if("data" in st.session_state):
                data = st.session_state["data"]
                X=data[data.columns[:-1]]
                Y=data["target"]

                
                X = preprocessing.scale(X)
                features_train, features_test, activity_train, activity_test = model_selection.train_test_split(X,Y,train_size=0.7)
                st.text("Pourcentage jeu d'entrainement : " + str(len(activity_train)/ float(len(X))))
                st.text("Pourcentage jeu de test : " + str(len(activity_test)/ float(len(X))))

                st.title("Génération du modèle KNeighborsClassifier")
                with st.spinner("Veuillez patienter pendant l'entrainement du modèle"):
                    nn2 = neighbors.KNeighborsClassifier(n_neighbors=5)
                    nn2.fit(features_train,activity_train)
                    st.text("Le taux de bon classement pour NN2 sur l'échantillon test est " + str(nn2.score(features_test,activity_test)))
                    st.text("Le taux de bon classement pour NN2 sur l'échantillon test est " + str(nn2.score(features_train,activity_train)))
                with st.spinner("Veuillez patienter pendant la validation croisée"):
                    my_kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state = 0)
                    nn_val_croisee = neighbors.KNeighborsClassifier(n_neighbors = 10)

                    scores = model_selection.cross_val_score(estimator=nn_val_croisee,
                                            X=X,
                                            y=Y,
                                            cv=my_kfold,
                                            n_jobs=-1) # permet de répartir les calculs sur plusieurs coeurs
                    st.text("Scores : " + str(scores))
                    st.text("Moyenne du score : " + str(mean(scores)))
                    from sklearn.model_selection import cross_val_score, KFold
                with st.spinner("Veuillez patienter pendant le GridSearchCV"):
                    features_all_train, features_all_test, activity_all_train, activity_all_test = model_selection.train_test_split(X,Y,train_size=0.7,random_state=42)
                    from sklearn.model_selection import GridSearchCV
                    st.text("On va tester un nombre de voisins compris entre 2 et 20")
                    # la grille de parametres a regler sont definis dans un dictionnaire (dict)
                    tuned_parameters = {'n_neighbors': range(2,20)}

                    my_kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state=0)
                    nnGrid = GridSearchCV(neighbors.KNeighborsClassifier(),
                                        tuned_parameters,
                                        cv=5)
                    nnGrid.fit(features_all_train, activity_all_train)

                    # le meilleur modele 
                    st.text('On choisit de conserver ' + str( nnGrid.best_params_['n_neighbors'])+ ' voisins.')
                    st.text("On a obtenu le meilleur score de " + str( nnGrid.best_score_) + " avec ce paramètres")
                st.text("Matrice de confusion : ")
                predictions = nnGrid.predict(features_all_test)
                cm = confusion_matrix(activity_all_test, predictions)
                disp = ConfusionMatrixDisplay(confusion_matrix=cm)
                fig, ax = plt.subplots()
                sns.set_theme(font_scale=1.2)  # Adjust font size
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                plt.title('Confusion Matrix')
                st.write(fig)
                st.session_state["Data"] = data
                st.session_state["model"] = nnGrid.best_estimator_
                st.text("Modèle sauvegardé !")
            else:
                st.text("Vous devez d'abord importer un fichier")
        if bt_vin2:
            if("data" in st.session_state):
                data = st.session_state["data"]
                X=data[data.columns[:-1]]
                Y=data["target"]

                X = preprocessing.scale(X)
                features_train, features_test, activity_train, activity_test = model_selection.train_test_split(X,Y,train_size=0.7)
                st.text("Pourcentage jeu d'entrainement : " + str(len(activity_train)/ float(len(X))))
                st.text("Pourcentage jeu de test : " + str(len(activity_test)/ float(len(X))))

                st.title("Génération du modèle Regression Logistique")
                with st.spinner("Veuillez patienter pendant l'entrainement du modèle"):
                    clf = LogisticRegressionCV(cv=5, random_state=0)

                    #--------------------------------------
                    my_kfold =    model_selection.KFold(n_splits=10, shuffle=True, random_state=0)
                    scores = model_selection.cross_val_score(estimator=clf,
                                            X=X,
                                            y=Y,
                                            cv=my_kfold,
                                            n_jobs=-1) 
                    st.text("Moyenne du score : " + str(mean(scores)))
                    from sklearn.model_selection import cross_val_score, KFold
                st.text("Matrice de confusion : ")
                features_all_train, features_all_test, activity_all_train, activity_all_test = model_selection.train_test_split(X,Y,train_size=0.7,random_state=42)
                clf.fit(features_all_train, activity_all_train)
                predictions_log=clf.predict(features_all_test)
                cm = confusion_matrix(activity_all_test, predictions_log)
                fig, ax = plt.subplots()
                sns.set_theme(font_scale=1.2)  # Adjust font size
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                plt.title('Confusion Matrix')
                st.write(fig)
                st.session_state["Data"] = data
                st.session_state["model"] = clf
                st.text("Modèle sauvegardé !")
            else:
                st.text("Vous devez d'abord importer un fichier")


with st.expander("Traitement pré configuré ""Diabète"" "):
    bt_diab = st.button("Lancer le traitement",key="diabete")
    if bt_diab:
        if("data" in st.session_state):
            data = st.session_state["data"]

        else:
            st.text("Vous devez d'abord importer un fichier")