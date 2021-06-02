import numpy as np

def recommandation_globale(data):
    dico_best = dict()
    for i in list(set(data['genre'])):
        dico_best[i] = []
    bd = data.groupby(['movie','genre']).mean()
    taille = len(bd)
    for i in range(taille):
        temps = bd.iloc[i]
        dico_best[temps.name[1]].append((temps.values[0],temps.name[0]))
    for serie in dico_best :
        dico_best[serie].sort(reverse=True)
    return dico_best

def affiche_liste_genre(dico):
    k = 1
    for i in dico.keys():
        print(k,' ' ,i)


def recommande_film(dico,genre,n=5,verbose=True):
    try :
        lists = dico[genre][:n]
        lists2 = []
        for i in range(len(lists)) :
            lists2.append(lists[i][1])
            if verbose :
                print(i , ' : ',lists[i][1])
        return lists2
    except :
        if verbose :
            print('Veuillez saisir un genre valide :')
            affiche_liste_genre(dico)

def top_film(data,n=20,verbose=True):
    t = data['global rating']
    r = np.argsort(-1*t)[:n]
    arr = data.to_numpy()
    res = []
    if verbose :
        print('Top Film')
    for i in range(len(arr[r]))  :
        res.append(arr[r][i][0])
        if verbose :
            print((i+1), ' :', arr[r][i][0])
    return res


def serie_similaire(matrice_distance,list_serie,n=10,seuil=0.5) :
    res = []
    res2 = []
    list_serie_ind = np.array(range(0,len(list_serie)))
    for i in matrice_distance:
        list_ind = np.argsort(i)[1:n+1]
        res.append(list_serie[list_ind])
        res2.append(list_serie_ind[list_ind])
    return res,res2

