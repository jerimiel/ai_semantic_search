import pinecone
import requests
import json
import config
import pandas as pd

df = pd.read_csv("mpst_full_data.csv")

def search_db(data,model,n):
    pinecone.init(
        api_key=config.PINECONE_API_KEY,
        environment=config.PINECONE_ENV
    )
    index_name = "movie-search"
    index = pinecone.Index(index_name)
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
    return results
        