import pickle


################### PICKLE ######################
def sauvegardeFichier(nomFichier,liste):
    """
    nomFichier : nom du fichier qu'on souhaite sauvegarder
    """
    with open(nomFichier,'wb') as fichier :
        enregistre = pickle.Pickler(fichier)
        enregistre.dump(liste)

def lectureFichier(nomFichier):
    with open(nomFichier,'rb') as fichier :
        recupere = pickle.Unpickler(fichier)
        return recupere.load()
    