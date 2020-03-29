#w/o star preload

from flask import Flask
from flask import request
from flask import current_app
import json
from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route("/started") #az eredeti URL mögé localhost:5113 ha beírod a /started-et, akkor kiírja, hogy fing
def started():         #azért kell csak, hogy lecsekkoljuk, hogy működik-e a szerver
    return "FING"


@app.route("/")        #ha megpróbálom a porton lévő szervert elérni localhost:5113, akkor ez fut le 
def solution():        #mivel a proccess.py helyén ez van, szóval a teszt fv. ezt hívja meg, így kapcsolódik össze
    
    app.input_dicts = tuple(json.load(open("inputs.json", "r")))
    app.df = app.dfo
    
    answers2 = filter(app.dfo, app.input_dicts)

    json.dump(answers2,open('outputs.json','w'))
    
    return "Outputot droppoltam az aktuális mappába"


def filter(data, input_):
    answers = []
    for input_idx, input_dict in enumerate(input_):
        data = data[data['stars'] == input_dict['stars']]
        data = data[data['current-price'] >= input_dict['min_price']]
        data = data[data['current-price'] <= input_dict['max_price']]
    
        if len(data) > 0:
            query_all = (input_dict['lat'], input_dict['lon'])
            query_all = np.array(query_all)
            query_all = query_all.reshape(1,-1)
            tree = KDTree(data[['lat', 'lon']].values)
            dist, ind = tree.query(query_all)
            [answers.append(dict(data.iloc[i[0]])) for i in ind]


        else:
            answers.append({"missing": True})
        data = df
    return answers



def shutdown_server(): #fv definíció, amit később meghívunk, hogy lője le a szervert
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown") 
def shutdown():
    shutdown_server()      #itt hívja meg az fv-t, hogy lelője a szerót
    return "Server shutting down..."


data_file_path = "data.csv"

app.dfo = pd.read_csv(data_file_path)

app.dfo.drop_duplicates().assign(
    price=lambda _df: _df["current-price"]
    .str[1:]
    .str.replace(",", "")
    .astype(float)
).loc[:, ["lon", "lat", "name", "stars", "price"]]

    

if __name__ == "__main__":
    app.run(debug=True, port=5113)