import sys
sys.path.append('../') 
import projet   
from projet import preTraitement as pt
from projet import save as sv
from projet import prediction_genre_preferer as fcg
from projet import recommandation_globales as rg
from projet import classifiers as cl


import pandas as pd
import numpy as np
import copy

from surprise import SVD
from surprise import Dataset
from surprise import Reader
from surprise import SVDpp
from surprise import accuracy
from collections import defaultdict


def filtre_user(data,list_indice):
    arr = data.to_numpy()
    pd2 = pd.DataFrame(arr[list_indice])
    pd2.columns = data.columns
    return pd2

def liste_nom_serie_filtre(nom_serie):
    nom_serie2 = []
    lists = [pt.supprimeAccent,pt.minusculeString,pt.supprimePonctuation,pt.filtreNombre] #
    for serie in nom_serie :
        serie = pt.normaliseMot(lists,serie) 
        serie = serie[:len(serie)-1]   
        nom_serie2.append(serie)
    return nom_serie2

def filtre_serie(nom_serie1,nom_serie2):
    nom_serie4 = []
    for serie in range(len(nom_serie1)) :
        if nom_serie1[serie] in nom_serie2 :
            nom_serie4.append(nom_serie1[serie])       
    return nom_serie4


def list_indice_serie(nom_serie1,nom_serie2) :
    nom_serie4 = []
    for serie in range(len(nom_serie1)) :
        if nom_serie1[serie] in nom_serie2 :
            nom_serie4.append(serie)       
    return nom_serie4


def prediction_user(data_clean,algo,lecteur,verbose=False):
    data = Dataset.load_from_df( data_clean , lecteur )
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    acc_rmse = accuracy.rmse(predictions,verbose=verbose)
    acc_mse = accuracy.mse(predictions,verbose=verbose)
    acc_mae = accuracy.mae(predictions,verbose=verbose)
    return predictions,acc_rmse,acc_mse,acc_mae


def prediction_n_meilleur(prediction, n=10):
    # On commencez par iterer sur les prédictions de chaque utilisateur.
    n_meilleur = defaultdict(list)
    for uid, iid, _, note, _ in prediction:
        n_meilleur[uid].append((iid, note))

    # Ensuite on trie les prédictions pour chaque utilisateur et on récupére les k les plus élevées.
    for uid, note_user in n_meilleur.items():
        #lambda a la forme uid,rating -> on extrait donc l'élément 1 qui correspond au rating
        note_user.sort(key=lambda tuples: tuples[1], reverse=True)
        n_meilleur[uid] = note_user[:n]

    return n_meilleur

#######################################
# FILTRAGE COLLABORATIF 
#######################################

def filtrage_collaboratif(data,algo,lecteur,n=10,verbose=False):
    #matrice_init,dico_film,dico_vf,dico_user,dico_vu = prepare_data(data)
    predi,acc_rmse,acc_mse,acc_mae = prediction_user(data,algo,lecteur,verbose=verbose)
    #matrice_finale = complete_matrice(copy.deepcopy(matrice_init),dico_film,dico_user,predi)
    #matrice_finale, 
    reco = prediction_n_meilleur(predi, n=10)
    return reco, acc_rmse, acc_mse, acc_mae, predi


def recommandation_user(dico,user,n=10,verbose=True):
    temps = dico[user][:n]
    resultat = []
    if verbose :
        print('Top Film')
    for i in range(len(temps)) :
        resultat.append(temps[i][0])
        if verbose : 
            print((i+1), ' :', temps[i][0])
    return resultat

def user_exist(dico,user):
    return user in dico


#######################################
# FILTRAGE COLLABORATIF 2 (avec selection des users)
#######################################

def selectionne_profil_similaire(selectionne_profil,filtre_collab,filtre_collab_genre,user,nb_seuil=1000):
    cpt = 0
    list_film = selectionne_profil[selectionne_profil['reviewer']==user]['movie']
    list_ind = []
    for serie in set(list_film) :
        temps = filtre_collab[filtre_collab['movie']==serie]
        list_ind += [i for i in temps.index]
        cpt = len(list_ind)
        if cpt >= nb_seuil :
            list_ind = list(set(list_ind))
            return filtre_user(filtre_collab,list_ind)

    dico = fcg.prediction_n_meilleur_genre(filtre_collab_genre)
    genre = fcg.recommandation_user(dico,user,limite=4,verbose=False)
    
    for i in genre :
        temps = selectionne_profil[selectionne_profil['genre']==i].index
        for i in temps :
            if cpt >= nb_seuil :
                break
            list_ind.append(i) 
            cpt += 1
    list_ind = list(set(list_ind))
    return filtre_user(filtre_collab,list_ind)

def filtrage_collaboratif2(selectionne_profil,filtre_collab,filtre_collab_genre,user,algo,lecteur,nb_seuil=1000,verbose=False):
    data =  selectionne_profil_similaire(selectionne_profil,filtre_collab,filtre_collab_genre,user,nb_seuil=nb_seuil)
    return filtrage_collaboratif(data,algo,lecteur,verbose=verbose)


#######################################
# HYBRIDATION
#######################################

def recommandation_hybride(selectionne_profil,filtre_collab,filtre_collab_genre,user,algo,lecteur,tfidf,liste_nom_serie,nb_seuil=1000,verbose=False):
    reco, acc_rmse, acc_mse, acc_mae, predi = filtrage_collaboratif2(selectionne_profil,filtre_collab,filtre_collab_genre,user,algo,lecteur,nb_seuil=1000,verbose=False)
    res = recommandation_user(reco,user,n=5,verbose=verbose)
    matrice_distance = cl.distance_cosine(tfidf)
    film_similaire,_ = rg.serie_similaire(matrice_distance,np.array(liste_nom_serie),n=3)
    liste_nom_serie2 = []
    for i in liste_nom_serie:
        liste_nom_serie2.append(i.rstrip())
    res2 = []
    for serie in res : 
        try : 
            ind = liste_nom_serie2.index(serie)
        except :
            continue
        cpt = 0
        for i in film_similaire[ind] :
            if cpt >= 3 :
                break
            res2.append(i)
            cpt += 1
    return res + res2
    