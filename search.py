import pinecone
import requests
import json
import config
import pandas as pd

df = pd.read_csv("mpst_full_data.csv")

#A function to connect to pinecone database
#It returns the index after connection is established
def pinecone_connect():
    try:
        pinecone.init(
                api_key=config.PINECONE_API_KEY,
                environment=config.PINECONE_ENV
            )
        index_name = "movie-search"
        index = pinecone.Index(index_name)
        print(type(index))
        return index
    except Exception as error:
        return str(error)
    

#search_db is a function that searches the online 'movie_search' database for closest movies to a query.
#It takes in data which is the query, model which is the pretrained model, index which is the pinecone index and n which is the number of 
#results to be returned.
#It returns results, a list of movie titles and synopsis closest to your search query

def search_db(data,model,n,index):
    try:
        query = data
        xq = model.encode(query).tolist()
        xc = index.query(xq, top_k=n, include_metadata=True)
        results=[]
        for i in xc["matches"]:
            id = i["metadata"]["text"]
            #res = requests.get(f"https://api.themoviedb.org/3/find/{id}?api_key={config.TMDB_KEY}&external_source=imdb_id")
            #results.append((json.loads(res.content)["movie_results"][0]["title"],
            #json.loads(res.content)["movie_results"][0]["overview"],str(int(float(i["score"])*100))+"%"))
            results.append((df[df["imdb_id"]==id]["title"].values[0],
                            df[df["imdb_id"]==id]["plot_synopsis"].values[0],
                            str(int(float(i["score"])*100))+"%"
                           ))
    except Exception as e:
        return str(e)
    return results
        