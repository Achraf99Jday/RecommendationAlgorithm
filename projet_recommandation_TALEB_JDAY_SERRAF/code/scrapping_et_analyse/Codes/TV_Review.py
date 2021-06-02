from pymongo import MongoClient as pm
import requests
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio

#Extracting data from API
json_data = {}
tv_shows_list = []
count = 0
for page in range(1,55):  #take 50 pages from json
    response = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=ea8063946b3a3ebeb79b254eb8540a797&language=en-US&page="+str(page))
    json_data[page] = response.json()
    for b in range(1,20):
        tv_shows_list.append(json_data[page]["results"][b]["id"])

json_data = {}
for show in range(0,len(tv_shows_list)):   #take 1000 tv shows list from api
    response = requests.get("https://api.themoviedb.org/3/tv/"+str(tv_shows_list[show])+"/reviews?api_key=a8063946b3a3ebeb79b254eb8540a797")
    if response.status_code == 200:
       json_data[count] = response.json()
       count = count+1

###########################################MongoDB Connecivity#########################################################################
dbconn = pm("mongodb://dapgrpl:dapgrpl@91.164.112.170/")
tmdb = dbconn["TMDB"]
tv_reviews = tmdb["tv_reviews"]
collname = tmdb.list_collection_names()
if "tv_reviews" in collname:
    tv_reviews.drop()
tv_reviews = tmdb["tv_reviews"]
mongo_id = []
for a in range(0,len(tv_shows_list)):
    mongo_ins = tv_reviews.insert_one(json_data[a])
    mongo_id.append(mongo_ins.inserted_id)
print("Inserted full data of movies into MongoDB database.\n")

tv_list =[]
collection = tmdb['tv_reviews']
cursor = collection.find({})
for document in cursor:
     tv_list.append(document)    
 
json_data = tv_list 

tv_review_list = tv_reviews.find({},{"_id":0, "id":1, "results":1}) #to find data in a collection
tv_show_id = []
Review_author = []
Review_Content = []
Review_url = [] 
   
for a in range(0,len(tv_shows_list)):  #To move the data into list and converted it to structure
    for b in range(0, len(tv_review_list[a]["results"])):
        tv_show_id.append(tv_review_list[a]["id"])
        Review_author.append(tv_review_list[a]["results"][b]["author"])
        tv_show_id.append(tv_review_list[a]["id"])
        Review_Content.append(tv_review_list[a]["results"][b]["content"])
        tv_show_id.append(tv_review_list[a]["id"])
        Review_url.append(tv_review_list[a]["results"][b]["url"])
        
#dataframe created for structure data
Dataframe_Reviews = pd.DataFrame(list(zip(tv_show_id, Review_author, Review_Content, Review_url)),columns = ["tvshowid", 'author', 'content', 'url']) 


####################################################PostgreSQL Connectivity##############################################################################
try:
    dbConnection = psycopg2.connect(
            user = "dapgrpl",
            password = "dapgrpl",

            host = "91.164.112.170",
            #port = "5432",
            database = "tmdb")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.close()
    
except (Exception , psycopg2.Error) as dbError :
        print ("Error while connecting to PostgreSQL", dbError)
        
#######################################To remove \r and \n#############################################################################
        
for i in range(0,1687):
    Dataframe_Reviews['content'][i] = Dataframe_Reviews['content'][i].replace('\n', '')
    Dataframe_Reviews['content'][i] = Dataframe_Reviews['content'][i].replace('\r', '')        
        
        

#################Table creation and insertion####################################


sqlio.to_sql(Dataframe_Reviews, 'tv_review', 'postgresql+psycopg2://dapgrpl:dapgrpl@91.164.112.170/tmdb', if_exists = 'replace')


#########################View Table data#####################################

Data_Query = "Select tvshowid, author, content from tv_review;"

sqlio.read_sql_query(Data_Query, dbConnection)

####################Inner join to extract from TV_All table######################################################


Data_Query = "Select tvshowid, tv_name, author, content, tv_popularity  from tv_review INNER JOIN tv_all ON tv_review.tvshowid = tv_all.tv_id;"
Data_Query1 = "Select tv_origin_country,tvshowid, tv_name, author, content, tv_popularity  from tv_review INNER JOIN tv_all ON tv_review.tvshowid = tv_all.tv_id;"
Data_Query2 = "Select tv_review.author, tv_review.content from tv_review INNER JOIN movies_reviews ON tv_review.author = movies_reviews.author;"
Data_Query3 = "Select *  from tv_review INNER JOIN tv_all ON tv_review.tvshowid = tv_all.tv_id;"


Data_join = sqlio.read_sql_query(Data_Query, dbConnection)
Data_join1 = sqlio.read_sql_query(Data_Query1, dbConnection)
Data_join3 = sqlio.read_sql_query(Data_Query2, dbConnection)
Data_join2 = sqlio.read_sql_query(Data_Query3, dbConnection)

###############################################Sentiment Analysis Data Join###################################################################


import nltk.sentiment.vader
from nltk.corpus import stopwords
import nltk.tokenize as nt  
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words('english'))

Data_join['word_list'] = Data_join['content'].apply(lambda x: [item for item in x.split() if item not in stop_words])

Data_join['sentiment_scores'] = ""
Data_join['total_score'] = ""
Data_join['review'] = ""

from afinn import Afinn
af = Afinn()

 

for i in range(0, len(Data_join)):
        Data_join['sentiment_scores'][i] = [af.score(article) for article in Data_join['word_list'][i]]


for i in range(0,len(Data_join)):
    Data_join['total_score'][i] = sum(Data_join['sentiment_scores'][i])

 

sentiment_category = ['positive' if score > 0 
                          else 'negative' if score < 0 
                              else 'neutral' 
                                  for score in Data_join['total_score']]

Data_join['review'] = sentiment_category
 
#Interactive word plot
%matplotlib inline
import scattertext as st
import re, io
from pprint import pprint
import pandas as pd
import numpy as np
from scipy.stats import rankdata, hmean, norm
import spacy as sp
import os, pkgutil, json, urllib
from urllib.request import urlopen
from IPython.display import IFrame
from IPython.core.display import display, HTML
from scattertext import CorpusFromPandas, produce_scattertext_explorer
display(HTML("&lt;style>.container { width:98% !important; }&lt;/style>"))

#Corpus Creation
nlp = st.WhitespaceNLP.whitespace_nlp
corpus = st.CorpusFromPandas(Data_join, 
                              category_col='review', 
                              text_col='content',
                              nlp=nlp).build()

#Frequent Words extraction 
print(list(corpus.get_scaled_f_scores_vs_background().index[:10]))
term_freq_df = corpus.get_term_freq_df()

#Frequent Positive Words extraction
term_freq_df['positive Score'] = corpus.get_scaled_f_scores('positive')
pprint(list(term_freq_df.sort_values(by='positive Score', ascending=False).index[:10]))

##Frequent Neagtive Words extraction 
term_freq_df['negative score'] = corpus.get_scaled_f_scores('negative')
pprint(list(term_freq_df.sort_values(by='negative score', ascending=False).index[:10]))

################################################Scatterplot1###################################################################

html = st.produce_scattertext_explorer(corpus,
          category='positive',
          category_name='positive',
          not_category_name='negative',
          width_in_pixels=1000,
          metadata=Data_join['content'])
open("C:/Users/Ruchira Talekar/Desktop/Convention-Visualization.html", 'wb').write(html.encode('utf-8'))

 
################################################Scatterplot2###################################################################

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
import scattertext as st
from scipy.sparse.linalg import svds

 
Data_join['parse'] = Data_join['content'].apply(st.whitespace_nlp_with_sentences)

 
#Corpus for scatterplot2
corpus = (st.CorpusFromParsedDocuments(Data_join,
                                       category_col='review',
                                       parsed_col='parse')
              .build()
              .get_stoplisted_unigram_corpus()) 

 

corpus = corpus.add_doc_names_as_metadata(corpus.get_df()['author'])
corpus.get_df()['content']
len(corpus.get_metadata())

print(corpus.get_term_doc_mat()) 

#Eigen value matrix creation
embeddings = TfidfTransformer().fit_transform(corpus.get_term_doc_mat())
u, s, vt = svds(embeddings, k=167, maxiter=20000, which='LM')
projection = pd.DataFrame({'term': corpus.get_metadata(), 'x': u.T[0], 'y': u.T[1]}).set_index('term')


#plotting of graph 
category = 'positive'
scores = (corpus.get_category_ids() == corpus.get_categories().index(category)).astype(int)
html = st.produce_pca_explorer(corpus,
                               category=category,
                               category_name='positive',
                               not_category_name='negative',
                               metadata=Data_join['author'],
                               width_in_pixels=1000,
                               show_axes=False,
                               use_non_text_features=True,
                               use_full_doc=True,
                               projection=projection,
                               scores=scores,
                               show_top_terms=False)
open("C:/Users/Ruchira Talekar/Desktop/Convention-Visualization1.html", 'wb').write(html.encode('utf-8'))


#################Comparison Graph####################################################################################

#Datajoin3 sentiment analysis
import nltk.sentiment.vader
from nltk.corpus import stopwords
import nltk.tokenize as nt  
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words('english'))

Data_join3['word_list'] = Data_join3['content'].apply(lambda x: [item for item in x.split() if item not in stop_words])

Data_join3['sentiment_scores'] = ""
Data_join3['total_score'] = ""
Data_join3['review'] = ""

from afinn import Afinn
af = Afinn()

 

for i in range(0, len(Data_join3)):
        Data_join3['sentiment_scores'][i] = [af.score(article) for article in Data_join3['word_list'][i]]


for i in range(0,len(Data_join3)):
    Data_join3['total_score'][i] = sum(Data_join3['sentiment_scores'][i])


sentiment_category = ['positive' if score > 0 
                          else 'negative' if score < 0 
                              else 'neutral' 
                                  for score in Data_join3['total_score']]

Data_join3['review'] = sentiment_category
 

########################################Author Vs Review Category##########################################################

import plotly.graph_objects as go
from plotly.offline import plot


fig1 = go.Figure(data= go.Heatmap(
        x=Data_join3['author'],
        y=Data_join3['review'],
        z= Data_join3['total_score'],
        colorscale= 'Viridis'))

fig1.update_layout(
        title='Author Vs Review category',
        xaxis_nticks=36)
plot(fig1)


########################################Author Vs Popularity##########################################################
fig2 = go.Figure(data=[go.Bar(
        x=Data_join3['author'],
        y=Data_join['tv_popularity']
        )])

plot(fig2)
fig2.update_layout(
        title='Tv authors Vs Tv popularity',
        xaxis_nticks=36, plot_bgcolor='white')
plot(fig2)


#########################################Genres Vs Sentiment Score##############################################################

fig6 = go.Figure()
fig6.add_trace(go.Bar(
        x = Data_join2['tv_genres_name'],
        y = Data_join['total_score'],
        
        marker_color = 'darkviolet',
        width = [0.8]))
fig6.update_layout(
        title='TV Genres Vs TV Sentiment Score',
        xaxis_nticks=36, plot_bgcolor='white')
plot(fig6)

