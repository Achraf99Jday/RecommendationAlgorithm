from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def TFIDF(liste):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(liste)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    return pd.DataFrame(denselist, columns=feature_names),feature_names