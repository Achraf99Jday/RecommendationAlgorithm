import pymongo as pm
import psycopg2 as pc2
import pandas.io.sql as sqlio
import requests
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as psub
from plotly.offline import plot
import plotly.io as pio
from statistics import mean
from plotly.offline import iplot, init_notebook_mode
pio.renderers.default = "svg"

#client = MongoClient("mongodb://dapgrpl:dapgrpl@18.203.68.115/TMDB")
json_data = {}
movie_list = []
count = 0
for a in range(1,51):
    response = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=e26739c583461de65e1a334904cf7883&language=en-US&page="+str(a))
    json_data[a] = response.json()
    for b in range(0,20):
        movie_list.append(json_data[a]["results"][b]["id"])

json_data = {}
for a in range(0,1000):
    response = requests.get("https://api.themoviedb.org/3/tv/"+str(movie_list[a])+"?api_key=e26739c583461de65e1a334904cf7883")
    if response.status_code == 200:
       json_data[count] = response.json()
       count = count+1


#from pprint import pprint
dbconn = pm.MongoClient("mongodb://dapgrpl:dapgrpl@18.203.68.115/")
tmdb = dbconn["TMDB"]
tv_all = tmdb["tv_all"]
collname = tmdb.list_collection_names()
if "tv_all" in collname:
    tv_all.drop()
tv_all = tmdb["tv_all"]
mongo_id = []
for a in range(0,len(movie_list)):
    mongo_ins = tv_all.insert_one(json_data[a])
    mongo_id.append(mongo_ins.inserted_id)
print("Inserted full data of movies into MongoDB database.\n")


json_data = tv_all.find({},{"_id":0,"networks":1,"origin_country":1, "id":1, "name":1, "first_air_date":1, "in_production":1, "number_of_episodes":1, "popularity":1, "status":1, "vote_average":1, "vote_count":1, "type":1, "genres":1, "production_companies":1, "created_by":1, "episode_run_time":1, "languages":1})

tv_name = []
tv_id = []
tv_created_by_name = []
tv_episode_run_time = []
tv_first_air_date = []
tv_genres_name = []
tv_in_production = []
tv_languages = []
tv_networks_name = []
tv_no_of_episodes = []
tv_origin_country = []
tv_popularity = []
tv_production_companies = []
tv_status = []
tv_type = []
tv_vote_average = []
tv_vote_count = []

for i in range(0,1000):
           tv_name.append(json_data[i]['name'])
           tv_id.append(json_data[i]['id'])
         
           tv_first_air_date.append(json_data[i]['first_air_date'])
           tv_in_production.append(json_data[i]['in_production'])
          
           tv_no_of_episodes.append(json_data[i]['number_of_episodes'])
           tv_popularity.append(json_data[i]['popularity'])
           
           tv_status.append(json_data[i]['status']) 
           tv_type.append(json_data[i]['type'])
           tv_vote_average.append(json_data[i]['vote_average'])
           tv_vote_count.append(json_data[i]['vote_count'])
           createdby = []
           for j in range(0,len(json_data[i]["created_by"])):
               createdby.append(json_data[i]["created_by"][j]["name"])
           createdby = ','.join(map(str, createdby))
           tv_created_by_name.append(createdby)
           episoderuntime = []
           for k in range(0,len(json_data[i]['episode_run_time'])):
               episoderuntime.append(json_data[i]['episode_run_time'][k])
           episoderuntime = ','.join(map(str, episoderuntime))
           tv_episode_run_time.append(episoderuntime)
           genres = []
           for l in range (0,len(json_data[i]['genres'])):
                genres.append(json_data[i]['genres'][l]['name'])
           genres = ','.join(map(str, genres))
           tv_genres_name.append(genres)
           language = []
           for m in range (0,len(json_data[i]['languages'])):
               language.append(json_data[i]['languages'][m])
           language = ','.join(map(str, language))
           tv_languages.append(language)   
           networks = []
           for n in range(0,len(json_data[i]["networks"])):
               networks.append(json_data[i]["networks"][n]["name"])
           networks = ','.join(map(str, networks))
           tv_networks_name.append(networks) 
           origincountry = []
           for o in range(0,len(json_data[i]["origin_country"])):
               origincountry.append(json_data[i]["origin_country"][o])
           origincountry= ','.join(map(str, origincountry))
           tv_origin_country.append(origincountry)
           productioncompany = []
           for p in range(0,len(json_data[i]["production_companies"])):
               productioncompany.append(json_data[i]["production_companies"][p]["name"])
           productioncompany = ','.join(map(str, productioncompany))
           tv_production_companies.append(productioncompany)
           
       
        
# Creating a Dataframe.
tv_all_df = pd.DataFrame(
        {"tv_id": tv_id,
        "tv_name":tv_name,
        "tv_created_by_name": tv_created_by_name,
        "tv_episode_run_time": tv_episode_run_time,
        "tv_first_air_date": tv_first_air_date,
        "tv_genres_name":tv_genres_name,
        "tv_in_production": tv_in_production,
        "tv_languages": tv_languages,
        "tv_networks_name":tv_networks_name,
        "tv_no_of_episodes":tv_no_of_episodes,
        "tv_origin_country":tv_origin_country,
        "tv_popularity": tv_popularity ,
        "tv_production_companies":tv_production_companies,
        "tv_status": tv_status,
        "tv_type": tv_type,
        "tv_vote_average":tv_vote_average,
        "tv_vote_count":tv_vote_count     
        })

# converting list of various episode runtimes into their average values and replacing in the dataframe

tv_all_df["tv_episode_run_time"] =tv_all_df["tv_episode_run_time"].replace('', '0')
runtime = list(tv_all_df["tv_episode_run_time"])
average_runtime_list = []
for i in range(0, len(runtime)):
    runtime[i] = runtime[i].split(",")
    average_runtime = list(map(int, runtime[i]))
    average_runtime_list.append(mean(average_runtime))
len(average_runtime_list)

tv_all_df["tv_episode_run_time"] = average_runtime_list


try:
    dbConnection = pc2.connect(
            user = "dapgrpl",
            password = "dapgrpl",
            host = "18.203.68.115",
            database = "tmdb")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    sql = "SELECT 1 AS RESULT FROM pg_database WHERE DATNAME = 'tmdb';"
    dbexists = sqlio.read_sql_query(sql, dbConnection)
    if dbexists.empty:
        dbCursor.execut("CREATE DATABASE tmdb;")
    dbCursor.close()
except (Exception , pc2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


try:
    sqlio.to_sql(tv_all_df, 'tv_all', if_exists='replace',index=False, con="postgresql+psycopg2://dapgrpl:dapgrpl@18.203.68.115/tmdb")
   
except (Exception , pc2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)



try:
    dbConnection = pc2.connect(
            user = "dapgrpl",
            password = "dapgrpl",
            host = "18.203.68.115",
            database = "tmdb")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    tv_all_sel = sqlio.read_sql_query("SELECT * FROM tv_all;", dbConnection)
except (Exception , pc2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()
    

#for genrating unique values
unique_createdby = list(tv_all_sel["tv_created_by_name"])
unique_createdby_list = []
for i in range(0, len(unique_createdby)):
    unique_createdby_list.append(unique_createdby[i])
unique_createdby_list = ','.join(map(str, unique_createdby_list))
unique_createdby_list = unique_createdby_list.split(",")
unique_createdby_list = list(set(unique_createdby_list))

unique_genres = list(tv_all_sel["tv_genres_name"])
unique_genres_list = []
for i in range(0, len(unique_genres)):
    unique_genres_list.append(unique_genres[i])
unique_genres_list = ','.join(map(str,  unique_genres_list))
unique_genres_list =  unique_genres_list.split(",")
unique_genres_list= list(set( unique_genres_list))

unique_languages = list(tv_all_sel["tv_languages"])
unique_languages_list = []
for i in range(0, len(unique_languages)):
    unique_languages_list.append(unique_languages[i])
unique_languages_list = ','.join(map(str,  unique_languages_list))
unique_languages_list =  unique_languages_list.split(",")
unique_languages_list= list(set(unique_languages_list))

unique_networks = list(tv_all_sel["tv_networks_name"])
unique_networks_list = []
for i in range(0, len(unique_networks)):
    unique_networks_list.append(unique_networks[i])
unique_networks_list = ','.join(map(str,  unique_networks_list))
unique_networks_list = unique_networks_list.split(",")
unique_networks_list= list(set( unique_networks_list))

unique_country = list(tv_all_sel["tv_origin_country"])
unique_country_list = []
for i in range(0, len(unique_country)):
    unique_country_list.append(unique_country[i])
unique_country_list = ','.join(map(str,  unique_country_list ))
unique_country_list  = unique_country_list .split(",")
unique_country_list = list(set( unique_country_list ))

unique_production = list(tv_all_sel["tv_production_companies"])
unique_production_list = []
for i in range(0, len(unique_production)):
    unique_production_list.append(unique_production[i])
unique_production_list = ','.join(map(str,  unique_production_list))
unique_production_list = unique_production_list.split(",")
unique_production_list= list(set(unique_production_list))

 
# Extracting and Visualizing trend of tv shows as per release year
try:
    dbConnection = pc2.connect(
            user = "dapgrpl",
            password = "dapgrpl",
            host = "18.203.68.115",
            database = "tmdb")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    tv_all_sel_year = sqlio.read_sql_query("SELECT count(tv_id) AS TV_COUNT, date_part('year', cast(tv_first_air_date AS DATE)) as RELEASE_YEAR from tv_all where date_part('year', cast(tv_first_air_date AS DATE))>'1989' group by date_part('year', cast(tv_first_air_date AS DATE)) order by date_part('year', cast(tv_first_air_date AS DATE)) asc;", dbConnection)
except (Exception , pc2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()
    
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*tv_all_sel_year.shape[0])
color[tv_all_sel_year["tv_count"].idxmax()]="red"
fig.add_trace(go.Bar(x=tv_all_sel_year["release_year"], y=tv_all_sel_year["tv_count"], name="No. of movies", marker=dict(color=color.tolist())))
fig.update_layout(title="Popular TV Shows through the years", xaxis_title="YEAR", yaxis_title="No. of tv shows", plot_bgcolor="white")
plot(fig)


# Extracting and Visualizing average popularity and vote average as per release year for released tv shows
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    popularity_year = sqlio.read_sql_query("SELECT avg(tv_popularity), date_part('year', cast(tv_first_air_date AS DATE)) as RELEASE_YEAR from tv_all where date_part('year', cast(tv_first_air_date AS DATE))>'1959' group by date_part('year', cast(tv_first_air_date AS DATE)) order by date_part('year', cast(tv_first_air_date AS DATE)) asc;", dbconn)
    tv_vote_average = sqlio.read_sql_query("SELECT avg(tv_vote_average), date_part('year', cast(tv_first_air_date AS DATE)) as RELEASE_YEAR from tv_all where date_part('year', cast(tv_first_air_date AS DATE))>'1959' group by date_part('year', cast(tv_first_air_date AS DATE)) order by date_part('year', cast(tv_first_air_date AS DATE)) asc;", dbconn)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
fig = go.Figure()
fig.add_trace(go.Scatter(name="Vote Average" ,x=tv_vote_average["release_year"], y=tv_vote_average["avg"], fill='tozeroy', fillcolor="rgb(160,160,160)", line_color="rgb(32,32,32)"))
fig.add_trace(go.Scatter(name="Popularity", x=popularity_year["release_year"], y=popularity_year["avg"], fill='tonexty', fillcolor="rgb(34,139,34)", line_color="rgb(0,102,0)"))
fig.update_layout(title="Trend of TV Popularity and Vote averages", xaxis_title="YEAR", yaxis_title="POPULARITY/VOTE AVERAGE", plot_bgcolor="white")
plot(fig)

# Extracting and Visualizing average tv shows runtime as per release year
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    runtime_year = sqlio.read_sql_query("SELECT avg(tv_episode_run_time), date_part('year', cast(tv_first_air_date AS DATE)) as RELEASE_YEAR from tv_all where date_part('year', cast(tv_first_air_date AS DATE))>'1959' group by date_part('year', cast(tv_first_air_date AS DATE)) order by date_part('year', cast(tv_first_air_date AS DATE)) asc;", dbconn)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*runtime_year.shape[0])
color[runtime_year["avg"].idxmax()]="rgb(255,0,0)"
fig.add_trace(go.Bar(x=runtime_year["release_year"], y=runtime_year["avg"], name="runtime of movies", marker=dict(color=color.tolist())))
fig.update_layout(title="Average runtime of tv shows throughout the years", xaxis_title="YEAR", yaxis_title="Average Runtime of tv shows", plot_bgcolor="white")
plot(fig)

# Extracting and Visualizing tv shows genre as per tv count
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    genre=pd.DataFrame(columns=['genre', 'count'])
    for i in range(1, len(unique_genres_list)):
        genre_each = sqlio.read_sql_query("SELECT count(tv_id) from tv_all where tv_genres_name like '%"+unique_genres_list[i]+"%';", dbconn)
        genre = genre.append({'genre': unique_genres_list[i], 'count': genre_each["count"][0]}, ignore_index=True)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
genre["count"] = genre["count"].astype(int)
genre = genre.sort_values('count', ascending=False)
genre = genre.reset_index(drop=True)
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*genre.shape[0])
color[genre["count"].idxmax()] = "rgb(255,0,0)"
fig.add_trace(go.Bar(x=genre["genre"], y=genre["count"], name="genre of tv shows", marker=dict(color=color.tolist())))
fig.update_layout(title="Spread of tv shows as per genres", xaxis_title="GENRE", yaxis_title="NO. OF TV SHOWS", plot_bgcolor="white")
plot(fig)

# Extracting and Visualizing tv shows production companies as per tv count
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    prod_cmpny=pd.DataFrame(columns=['prod_cmpny', 'count'])
    for i in range(1, len(unique_production_list)):
        prod_cmpny_each = sqlio.read_sql_query("SELECT count(tv_id) from tv_all where tv_production_companies like $$%"+unique_production_list[i]+"%$$;", dbconn)
        prod_cmpny = prod_cmpny.append({'prod_cmpny': unique_production_list[i], 'count': prod_cmpny_each["count"][0]}, ignore_index=True)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
prod_cmpny["count"] = prod_cmpny["count"].astype(int)
prod_cmpny = prod_cmpny.sort_values('count', ascending=False)
prod_cmpny = prod_cmpny.reset_index(drop=True)
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*prod_cmpny.shape[0])
color[prod_cmpny["count"].idxmax()] = "rgb(255,0,0)"
fig.add_trace(go.Bar(x=prod_cmpny["prod_cmpny"][:30], y=prod_cmpny["count"][:30], name="production company of movies", marker=dict(color=color.tolist())))
fig.update_layout(title="Tv show count as per production companies", xaxis_title="PRODUCTION COMPANY", yaxis_title="NO. OF SHOWS", plot_bgcolor="white")
plot(fig)


# Extracting and Visualizing tv shows production countries as per tv count
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    prod_cntry=pd.DataFrame(columns=['prod_cntry', 'count'])
    for i in range(1, len(unique_country_list)):
        prod_cntry_each = sqlio.read_sql_query("SELECT count(tv_id) from tv_all where tv_origin_country like $$%"+unique_country_list[i]+"%$$;", dbconn)
        prod_cntry = prod_cntry.append({'prod_cntry': unique_country_list[i], 'count': prod_cntry_each["count"][0]}, ignore_index=True)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
prod_cntry["count"] = prod_cntry["count"].astype(int)
prod_cntry = prod_cntry.sort_values('count', ascending=False)
prod_cntry = prod_cntry.reset_index(drop=True)
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*prod_cntry.shape[0])
color[prod_cntry["count"].idxmax()] = "rgb(255,0,0)"
color[1] = "rgb(0,0,255)"
fig.add_trace(go.Bar(x=prod_cntry["prod_cntry"][:20], y=prod_cntry["count"][:20], name="production country of tv shows", marker=dict(color=color.tolist())))
fig.update_layout(title="Tv shows count as per production countries", xaxis_title="PRODUCTION COUNTRY", yaxis_title="NO. OF TV SHOWS", plot_bgcolor="white")
plot(fig)

# Extracting and Visualizing tv shows languages as per tv count
try:
    dbconn = pc2.connect(
        user="dapgrpl",
        password="dapgrpl",
        host="18.203.68.115",
        port="5432",
        database="tmdb")
    dbcur = dbconn.cursor()
    tv_lang=pd.DataFrame(columns=['language', 'count'])
    for i in range(1, len(unique_languages)):
        tv_lang_each = sqlio.read_sql_query("SELECT count(tv_id) from tv_all where tv_languages like '%"+unique_languages_list[i]+"%';", dbconn)
        tv_lang = tv_lang.append({'language': unique_languages_list[i], 'count': tv_lang_each["count"][0]}, ignore_index=True)
    dbcur.close()
    print("Extracted data from postgres for visualizations.\n")
except (Exception, pc2.Error) as dbError:
    print("Error while connecting to PostgreSQL\n", dbError)
finally:
    print("Proceeding to perform visualization on the data...\n")
tv_lang["count"] = tv_lang["count"].astype(int)
tv_lang = tv_lang.sort_values('count', ascending=False)
tv_lang = tv_lang.reset_index(drop=True)
fig = go.Figure()
color=np.array(["rgb(100,100,100)"]*tv_lang.shape[0])
color[tv_lang["count"].idxmax()] = "rgb(255,0,0)"
color[1] = "rgb(0,0,255)"
fig.add_trace(go.Bar(x=tv_lang["language"][:20], y=tv_lang["count"][:20], name="languages of tv shows", marker=dict(color=color.tolist())))
fig.update_layout(title="Trend of tv show count as per languages", xaxis_title="LANGUAGE", yaxis_title="NO. OF TV SHOWS", plot_bgcolor="white")
plot(fig)
