import pandas as pd
import numpy as np
import json

input_locations = json.load(open('inputs.json', 'r'))

df = pd.read_pickle('filtered.pkl')


min_distances = [np.inf] * len(input_locations)
answers = [{}] * len(input_locations)


for row in df.itertuples():

    for lidx, place in enumerate(input_locations):

        distance = ((place['lon']-row[1]) ** 2 + (place['lat']-row[2]) ** 2) ** 0.5

        if distance < min_distances[lidx]:
            min_distances[lidx] = distance
            answers[lidx] = {'lon':row[1],'lat':row[2],'name':row[3]}
    
json.dump(answers,open('outputs.json','w'))