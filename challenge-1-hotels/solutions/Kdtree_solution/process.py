import pandas as pd
from scipy import spatial
import json
import pickle

i_locations = json.load(open('inputs.json', 'r'))

hotels = pd.read_pickle("hotels")

with open('KD_tree', 'rb') as f:
    tree = pickle.load(f)

def find_population(lat, lon):
    coordinates = [lat, lon]
    closest = tree.query([coordinates], p = 2) #distant_upper_bound = highest distance between hotels
    index = closest[1][0]
    return {
        'name' : hotels.name[index],
        'lat' : hotels.lat[index],
        'lon' : hotels.lon[index]
    }

answer = []

[answer.append(find_population(i['lat'], i['lon'])) for i in i_locations]

json.dump(answer,open('outputs.json','w'))