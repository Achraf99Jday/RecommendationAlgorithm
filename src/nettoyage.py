import os
import unicodedata
import string
 

def supprimeAccent(string):
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode("utf-8")

def minusculeString(string):
    return string.lower()

def supprimePonctuation(string):
    for ponctuation in string.punctuation:
        string = string.replace(ponctuation, "")
    return string

def extractionDonnerSeries(chemin_sous_repertoire_racine) :
    """
    Fonction qui va extraire les titres des différents episodes des differentes saison d'une series.
    
    param : chemin_sous_repertoire_racine (string) -> chemin vers l'un des sous repertoires du dossier racine qui contient 
    un ensemble de sous repertoires et fichier texte qui correspond a une serie avec le titre de ces episodes.
    return : liste[string] -> liste de tous les titres des épisodes d'une série
    """
    mot = []
   
    for root, directories, files in os.walk(chemin_sous_repertoire_racine):  

        #Parcours l'ensemble des fichiers
        for file in files:
            mot.append(file)

        #Parcours l'ensemble des répertoires
        for directorie in directories:
            mot.append(directorie)
    
    return mot

def traduitDonner(string):
    """
    Fonction qui va traduire les titres des séries et épisodes en une seule langue.
    
    param : string -> chaine de caractere qui corresponds a un titres d'une serie ou d'un épisode.
    return : string -> chaine de caractere traduit en une unique langue.
    """
    return string

def normaliseDonner(string):
    """
    Fonction qui va normaliser une donner.
    Cette fonction va mettre en minuscule la string, retirer les caracteres spécifiques.
    
    param : string -> chaine de caractere a normaliser
    return : string -> chaine de caractere normaliser.
    """
    string = minusculeString(string) #mettre tous les mots en minuscules
    string = supprimePonctuation(string) #remplace accent 
    string = supprimePonctuation(string) #supprime la ponctuation
    return string

def filtreDonner(liste) :
    """
    Fonction qui va filtrer les donner.
    Cette fonction va filtrer les donners inutiles mot trop frequent ...
    
    param : liste[string] -> liste chaine de caractere a filtrer
    return : liste[string] -> liste chaine de caractere filtrer.
    """
    return liste

def extractionSeries(chemin_racine):
    """
    Fonction qui va extraire les titres des différents séries.
    
    param : chemin_sous_repertoire_racine (string) -> chemin vers l'un des sous repertoires du dossier racine qui contient 
    un ensemble de sous repertoires et fichier texte qui correspond a une serie avec le titre de ces episodes.
    return : liste1[liste2[string]]  -> une liste1 ou chaque element de la liste1 correspond a une serie.
    La serie est une liste2[string] ou chaque element de cette liste correspond a un titre d'un episode de cette serie.
    """

    liste = []
    for serie in os.listdir() :
        liste.append(extractionDonnerSeries(serie))
    
    return serie
