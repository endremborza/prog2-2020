import pandas as pd
from scipy.spatial import kdtree
from scipy import spatial
import pickle

def tree_maker():
    df = pd.read_csv("data.csv")
    hotels = df.loc[:, ["lon", "lat", "name"]]
    places = []
    for index, row in hotels.iterrows():
        coordinates = [row['lat'], row['lon']]
        places.append(coordinates)
    
#numpy df.loc[lat, lon].values -> azonnal betölthető a treebe, nem kell iterálni

    hotels.to_pickle('hotels')
    tree = spatial.KDTree(places)
    return tree

tree = tree_maker()

with open('KD_tree', 'wb') as f:
    pickle.dump(tree, f)
