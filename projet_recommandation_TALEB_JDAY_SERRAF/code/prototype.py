import sys
sys.path.append('./')   

#importation de la librairie projet
import projet 
# importation des fonctions de serialisation de fichier
from projet import save as sv

from projet import filtrage_collaborative as fc

from projet import prediction_genre_preferer as fcg

from projet import recommandation_globales as rg

import pandas as pd
import numpy as np

from surprise import SVD
from surprise import Reader

def creer_un_compte(base_de_donner_user):
    user_name = input('Veuillez saisir un user_name .\n')
    while fc.user_exist(base_de_donner_user,user_name) :
        print('user_name existant')
        user_name = input('Veuillez saisir un user_name .\n')
    base_de_donner_user.append(user_name)
    sv.sauvegardeFichier("./fichierSerialiser/base_de_donner_user",base_de_donner_user)
    return base_de_donner_user

def note_film_user(base_de_donner_user,base_de_donner_film,filtre_collab):
    user_name = input('Veuillez saisir votre user_name .\n')
    while not fc.user_exist(base_de_donner_user,user_name) :
        print('user_name inexistant')
        user_name = input('Veuillez saisir votre user_name .\n')
    
    serie_name = input('Veuillez saisir une serie .\n')
    serie_name = fc.liste_nom_serie_filtre([serie_name])[0]
    while not fc.user_exist(base_de_donner_film,serie_name) :
        print('serie inexistante\n')
        serie_name = input('Veuillez saisir une serie .\n')
        serie_name = fc.liste_nom_serie_filtre([serie_name])[0]
    
    note = -1
    while note < 0 or note > 5:
        try :
            note = float(input('Veuillez saisir une note entre 0 et 5 .\n'))
        except :
            note = float(input('Veuillez saisir une note entre 0 et 5 .\n'))

    filtre_collab = filtre_collab.append({'reviewer':user_name,'movie':serie_name,'rating':note},ignore_index=True)
    sv.sauvegardeFichier("./fichierSerialiser/base_de_donner_prediction_genre",filtre_collab)
    return filtre_collab


def note_film_critique(base_de_donner_film,base_de_donner_genre,reco_glob):
    
    serie_name = input('Veuillez saisir une serie .\n')
    while not fc.user_exist(base_de_donner_film,serie_name) :
        print('serie existante\n')
        serie_name = input('Veuillez saisir une serie .\n')
    
    genre_name = input('Veuillez saisir le genre de la serie .\n')
    while not fc.user_exist(base_de_donner_genre,genre_name) :
        print('genre inexistant')
        genre_name = input('Veuillez saisir le genre de la serie .\n')

    note = -1
    while note < 0 or note > 5:
        note = float(input('Veuillez saisir une note entre 0 et 5 .\n'))

    reco_glob = reco_glob.append({'movie':serie_name,'genre':genre_name,'global rating':note},ignore_index=True)
    sv.sauvegardeFichier('./fichierSerialiser/base_de_donnees_recommendation_global',reco_glob)

def recommande_user(selectionne_profil,filtre_collab_genre,reco_glob,filtre_collab,base_de_donner_genre,base_de_donner_user):
    res_compte = input('Possédez-vous un compte ? [o/n]\n')
    if res_compte == 'n' :
        res_genre_pref = input('Souteriez-vous séléctionner vos genres de série préférez ? [o/n]\n')
        if res_genre_pref == 'n' :
            res = rg.top_film(reco_glob)
        else : 
            for i in range(len(base_de_donner_genre)):
                print((i),' :' ,base_de_donner_genre[i])
            
            res_genre_pref = int(input('Veuillez sélectionner un genre . [0,1,...,11]\n'))
            resultat = rg.recommandation_globale(reco_glob)
            liste_resultat = rg.recommande_film(resultat,base_de_donner_genre[res_genre_pref],n=10)
    else :
        user_name = input('Veuillez saisir votre user_name .\n')
        if fc.user_exist(base_de_donner_user,user_name) :
            algo = SVD()
            lecteur = Reader()                        
            reco, acc_rmse, acc_mse, acc_mae, predi = fc.filtrage_collaboratif2(selectionne_profil,filtre_collab,filtre_collab_genre,user_name,algo,lecteur,nb_seuil=1000,verbose=False)
            res = fc.recommandation_user(reco,user_name,n=10)
        else :
            print("Votre compte n'existe pas.\n")


def affiche_menu():
    print('Systeme de recommandation\n')
    print('1/ Créer un compte')
    print('2/ Noté un film (user)')
    print('3/ Noté un film (critique)')
    print('4/ Avoir une recommandation de film')
    print('5/ Quitter')


def saisie_controler_menu():
    menu = -1 
    while menu <=0 or menu >=6 :
        try :
            menu = int(input('Veuillez sélétionnez une action . 1/2/3/4/5\n'))
        except :
            menu = int(input('Veuillez sélétionnez une action . 1/2/3/4/5\n'))
    return menu

def object_global(user,film,genre,collab,collab_genre,reco_global,selectionne_profil):
    dico = dict()
    dico['base_de_donner_user'] = sv.lectureFichier(user)  
    dico['base_de_donner_serie'] = sv.lectureFichier(film)
    dico['base_de_donner_genre'] = sv.lectureFichier(genre)
    dico['filtre_collab'] = sv.lectureFichier(collab) 
    dico['filtre_collab_genre'] = sv.lectureFichier(collab_genre)
    dico['reco_glob'] = sv.lectureFichier(reco_global)
    dico['selectionne_profil'] = sv.lectureFichier(selectionne_profil)  
    return dico

def main():
    dirname = "./fichierSerialiser/"
    chemin_user = dirname + "base_de_donner_user"
    chemin_film = dirname + "base_de_donner_serie"
    chemin_genre = dirname +  "base_de_donner_genre"
    chemin_collab = dirname + "base_de_donner_filtrage_collaboratif"
    chemin_collab_genre = dirname + "base_de_donner_prediction_genre"
    chemin_reco_global = dirname + 'base_de_donnees_recommendation_global'
    chemin_selectionne_profil = dirname + 'base_de_donnees_selectionne_profil'

    dico = object_global(chemin_user,chemin_film,chemin_genre,chemin_collab,chemin_collab_genre,chemin_reco_global,chemin_selectionne_profil)

    bool = True

    while bool :
        affiche_menu()
        menu = saisie_controler_menu()

        print()
        if menu == 1 :
            creer_un_compte(dico['base_de_donner_user'])
        if menu == 2 :
            note_film_user(dico['base_de_donner_user'],dico['base_de_donner_serie'],dico['filtre_collab'])
        if menu == 3 :
            note_film_critique(dico['base_de_donner_serie'],dico['base_de_donner_genre'],dico['reco_glob'])
        if menu == 4 :
            recommande_user( dico['selectionne_profil'],dico['filtre_collab_genre'],dico['reco_glob'],dico['filtre_collab'],dico['base_de_donner_genre'],dico['base_de_donner_user'])
        if menu == 5 :
            bool = False



if __name__ == '__main__':
    main()