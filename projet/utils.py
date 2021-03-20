from collections import Counter
import matplotlib.pyplot as plt

def reconstitue_serie_tdidf(serie):
    temps = []
    for saison in serie :
        for episode in saison :
            temps.append(" ".join(episode))
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

