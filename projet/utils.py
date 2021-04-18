from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    plt.figure(figsize = (16,12))
    sns.heatmap(df, annot=True,cmap="Blues")
