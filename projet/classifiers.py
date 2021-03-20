# Import de packages externes
import numpy as np
import pandas as pd 
import copy
from sklearn.feature_extraction.text import TfidfVectorizer

def TFIDF(liste):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(liste)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    return pd.DataFrame(denselist, columns=feature_names),feature_names



# ---------------------------
class Classifier:
    """ Classe pour représenter un classifieur
        Attention: cette classe est une classe abstraite, elle ne peut pas être
        instanciée.
    """
    #TODO: Classe à Compléter
    def __init__(self, input_dimension):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
            Hypothèse : input_dimension > 0
        """
        self.input_dimension = input_dimension
        
    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """        
        raise NotImplementedError("Please Implement this method")
    
    def score(self,x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")
    
    def predict(self, x):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")

    def accuracy(self, desc_set, label_set):
        """ Permet de calculer la qualité du système sur un dataset donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        if len(desc_set) > 0 :
            qualiter =  0 
            for i in range(len(desc_set)) :
                prediction = self.predict(desc_set[i])
                vrai_valeur = label_set[i]
                if prediction == vrai_valeur :
                    qualiter += 1
            return qualiter / len(desc_set)
        return 0


# ---------------------------
class ClassifierKNN(Classifier):
    """ Classe pour représenter un classifieur par K plus proches voisins.
        Cette classe hérite de la classe Classifier
    """
    #TODO: Classe à Compléter
    def __init__(self, input_dimension, k):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension d'entrée des exemples
                - k (int) : nombre de voisins à considérer
            Hypothèse : input_dimension > 0
        """
        self.dim = input_dimension
        self.k = k 
        self.desc_set = []
        self.label_set = []

    def score(self,x):
        """ rend la proportion de +1 parmi les k ppv de x (valeur réelle)
            x: une description : un ndarray
        """
        #euclidienne : sqrt( somme(xi - x)**2 )
        distance = []
      
        for xi in self.desc_set  :
            temps = 0
            for i in range(len(xi)) :
                temps += (xi[i] - x[i]) ** 2
            distance.append(np.sqrt(temps))

        liste_index = np.argsort(distance)
     
        nombre_de_1 = 0
        for i in range(self.k) :
            index = liste_index[i]
            if self.label_set[index] == 1 :
                nombre_de_1 += 1
            
        return nombre_de_1 / self.k

    def predict(self, x):
        """ rend la prediction sur x (-1 ou +1)
            x: une description : un ndarray
        """
        if self.score(x) >= 0.5 :
            return 1
        return -1

    def train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """        
        self.desc_set = desc_set
        self.label_set = label_set


# classifieur Perceptron (moindre carrer)
class ClassifierADALINE(classif.Classifier):
    def train(self,desc_set, label_set):
        
        self.w = np.linalg.solve(np.matmul(np.transpose(desc_set), desc_set), np.matmul(np.transpose(desc_set), label_set))
        
    def score(self,x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """

        return np.vdot(x, self.w)
    def predict(self, x):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        if self.score(x) > 0:
            return 1
        return -1


# MultiClass
class ClassifierMultiOAA():
    def __init__(self, classifier):
        self.c = copy.deepcopy(classifier)
        self.classifiers = []
        self.ind_label = dict() # Dictionnaire {Classe : indice associé dans la liste du classifier}

    def train(self, data_set, label_set):
        # Tout d'abord on crée nos nCl classifiers et on leur assigne un indice
        i=0
        for l in label_set:
            if l not in self.ind_label :
                self.ind_label[l] = i
                i += 1
                self.classifiers.append(copy.deepcopy(self.c))

        # Pour chaque classe, on transforme le label_set en 1 et -1 et on entraine le classifier        
        for classe in self.ind_label:
            ytmp = [1 if k == classe else -1 for k in label_set]
            self.classifiers[self.ind_label[classe]].train(data_set, ytmp)

    def score(self, x):
        res = []
        for c in self.classifiers:
            res.append(c.score(x))
        return res
    
    def predict(self, x):
        ind = np.argsort(self.score(x))[-1] 
        for k in self.ind_label :
            if self.ind_label[k] == ind:
                return k 
    
    def accuracy(self, desc_set, label_set):
        yhat = np.array([self.predict(x) for x in desc_set])
        return np.where(label_set == yhat, 1., 0.).mean()
    