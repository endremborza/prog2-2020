import json
import pandas as pd
import numpy as np
from flask import Flask
from flask import request
from flask import current_app
from sklearn.neighbors import KDTree

app = Flask(__name__)


@app.route("/started") #az eredeti URL mögé localhost:5113 ha beírod a /started-et, akkor kiírja, hogy fing
def started():         #azért kell csak, hogy lecsekkoljuk, hogy működik-e a szerver
    return "FING"


@app.route("/")        #ha megpróbálom a porton lévő szervert elérni localhost:5113, akkor ez fut le 
def solution():        #mivel a proccess.py helyén ez van, szóval a teszt fv. ezt hívja meg, így kapcsolódik össze
    input_dicts = json.load(open("inputs.json", "r"))
    min_distances = [np.inf] * len(input_dicts)
    answers = [{"missing": True}] * len(input_dicts)
    for input_idx, input_dict in enumerate(input_dicts):
        try:
            stardict_tmp = app.stardict[input_dict["stars"]]
        except:
            continue
        for idx, row in stardict_tmp.iterrows():
            if (row["current-price"] < input_dict["max_price"]) and (row["current-price"] > input_dict["min_price"]):
                distance = ((input_dict["lon"] - row["lon"]) ** 2 + (input_dict["lat"] - row["lat"]) ** 2)
                if distance < min_distances[input_idx]:
                    min_distances[input_idx] = distance
                    answers[input_idx] = row[["lon", "lat", "name", "stars", "current-price"]].to_dict()
    json.dump(answers, open("outputs.json", "w"))
    return "Outputot droppoltam az aktuális mappába"


def shutdown_server(): #fv definíció, amit később meghívunk, hogy lője le a szervert
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown") 
def shutdown():
    shutdown_server()      #itt hívja meg az fv-t, hogy lelője a szerót
    return "Server shutting down..."



app.dfo = pd.read_csv("data.csv")
app.dfo.loc[:, ['lon','lat','name', 'current-price', 'stars']]

app.dfo['current-price'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
app.dfo['current-price'] = app.dfo['current-price'].astype('int64')
app.dfo = app.dfo.sort_values(by = 'current-price')
app.dfo.drop_duplicates(inplace = True)
app.dfo.dropna(how = "all")


app.starunique = sorted(app.dfo['stars'].unique())
app.stardict = {elem : pd.DataFrame() for elem in app.starunique}

for key in app.stardict.keys():
    app.stardict[key] = app.dfo[app.dfo['stars'] == key]
    

if __name__ == "__main__":
    app.run(debug=True, port=5113)
