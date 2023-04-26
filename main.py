from flask import Flask, render_template, request
from search import search_db
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')

app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template("index.html")
    
@app.route('/movies', methods=['GET','POST'])
def movie_search():
    default_value = '0'
    data = request.form['fname']
    n = request.form['num']
    results=search_db(data,model,int(n))
    return render_template("index.html", result=results)

if __name__ == '__main__':

	app.run(use_reloader = True, debug = True)
