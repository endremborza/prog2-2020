import pandas as pd
import numpy as np
import json

input_locations = json.load(open('inputs.json', 'r'))

df = pd.read_pickle('filtered.pkl')

answers = []

min_distances = [np.inf] * len(input_locations)
answers = [{}] * len(input_locations)

for idx,row in df.iterrows():
    
    for lidx, place in enumerate(input_locations):
        
        distance = ((place['lon']-row['lon']) ** 2 + (place['lat']-row['lat']) ** 2) ** 0.5
        
        if distance < min_distances[lidx]:
            min_distances[lidx] = distance
            answers[lidx] = row[['lon','lat','name']].to_dict()

json.dump(answers,open('outputs.json','w'))