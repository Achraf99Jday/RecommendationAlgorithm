import numpy as np

def prediction_n_meilleur_genre(data_genre):
    data = data_genre.groupby(['reviewer','genre']).count()
    dico = dict()
    for i in range(len(data)):
        temps = data.iloc[i]
        if temps.name[0] not in dico :
            dico[temps.name[0]] = [(temps.values[0],temps.name[1])]
        else:
            dico[temps.name[0]].append((temps.values[0],temps.name[1]))

    for i in dico :
        dico[i].sort(reverse=True)
    return dico

def recommandation_user(dico,user,limite=10,verbose=True):
    temps =  dico[user]
    resultat = []
    if verbose :
        print('Top Genre')
    for i in range(len(temps)) :
        if i >= limite :
            break
        resultat.append(temps[i][1])
        if verbose :
            print((i+1), ' :', temps[i][1])
    return resultat

