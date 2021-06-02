import sys
sys.path.append('../') 
import projet   
from projet import filtrage_collaborative as fc

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import timeit

def constitue_serie_tdidf(liste) :
    res = []
    for i in liste:
        res.append(reconstitue_serie_tdidf(i))
    return res

def reconstitue_serie_tdidf(serie):
    temps = ""
    for saison in serie :
        for episode in saison :
            
            temps = temps + " ".join(episode) + " "
            
            
    return temps

#################### AUTRE ####################

def calcule_frequence_serie(liste):
    dic = dict()
    
    for i in liste :
        if i in dic :
            dic[i] += 1
        else :
            dic[i] = 1
    
    return dic



#################### GRAPHE ####################

def graphe(liste):
    freq = Counter(liste)
    max = dict(freq.most_common(20))
    fig, ax = plt.subplots()
    ax = fig.add_axes(rect=[0,0,2,2])

    plt.bar(list(max.keys()), max.values(), color='g')
    plt.show()


def affiche2dScatter(X,Y):
    plt.scatter(X[:,0],X[:,1],c=Y)
    plt.colorbar()

def affiche3dScatter(X,Y):
    ax = plt.axes(projection='3d')
    ax.scatter(X[:,0],X[:,1],X[:,2],c=Y)

def afficheHeatmap(matrice_distance,liste_nom):
    """
    matrice_distance -> ndarray : matrice carrer des distances des series 
    """
    df = pd.DataFrame(matrice_distance)
    df["serie"] = liste_nom
    df.set_index("serie",inplace=True)
    df.columns = liste_nom
    plt.figure(figsize=(len(liste_nom), int(len(liste_nom)*0.66)))
    sns.heatmap(df, annot=True,cmap="Blues")

def affiche_distribution_genre(filtre_collab,reco_glob):
    filtre_reco = filtre_collab.merge(reco_glob, how='inner', on='movie')
    filtre_reco = filtre_reco.drop_duplicates(subset='movie')
    count = Counter(filtre_reco['genre'])
    list_genre = []
    list_valeur = []
    for i in  count:
        list_genre.append(i)
        list_valeur.append(count[i])
    plt.figure(figsize=(25,25))
    plt.pie(list_valeur, labels=list_genre, 
            autopct='%1.1f%%', shadow=True, startangle=90)
    print('Distribution Genre')


def evaluation_algo_accuracy(filtre_collab,nb_user,algo,lecteur):
    l1 = [];l2 = [];l4 = [];l5 = []

    for i in nb_user:
        tic = timeit.default_timer() # heure de départ
        reco,acc_rmse,acc_mse,acc_mae,predi = fc.filtrage_collaboratif(filtre_collab.iloc[:i,:],algo,lecteur,verbose=False)
        toc = timeit.default_timer() # heure de départ
        l1.append(acc_rmse);l2.append(acc_mse);l4.append(acc_mae);l5.append((toc-tic))
    return l1,l2,l4,l5

def affiche_evaluation_accuracy(nb_user,svd_rmse,svd_mse,svd_mae,svdpp_rmse,svdpp_mse,svdpp_mae):
    plt.figure(figsize=(10,5))
    plt.title('Svd VS Svdpp')
    plt.xlabel('Nombre Utilisateur')
    plt.ylabel('Accuracy')
    plt.plot(nb_user,svd_rmse,label='svd_rmse')
    plt.plot(nb_user,svd_mse,label='svd_mse')
    plt.plot(nb_user,svd_mae,label='svd_mae')
    plt.plot(nb_user,svdpp_rmse,label='svdpp_rmse')
    plt.plot(nb_user,svdpp_mse,label='svdpp_mse')
    plt.plot(nb_user,svdpp_mae,label='svdpp_mae')
    plt.legend()

def affiche_evaluation_time(nb_user,svd_time,svdpp_time):
    plt.figure(figsize=(10,5))
    plt.title('Svd VS Svdpp')
    plt.xlabel('Nombre Utilisateur')
    plt.ylabel('Times')
    plt.plot(nb_user,svd_time,label='svd_time')
    plt.plot(nb_user,svdpp_time,label='svdpp_time')
    plt.legend()