from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np
import json

input_locations = json.load(open('inputs.json', 'r'))
df = pd.read_pickle('filtered.pkl')
query_all = list(map(lambda dic: tuple(dic.values()), input_locations))
tree = KDTree(np.deg2rad(df[['lat', 'lon']].values), metric = 'euclidean')
dist, ind = tree.query(np.deg2rad(query_all))
answers = list(map(lambda i: dict(df.iloc[i[0]]), ind))
json.dump(answers,open('outputs.json','w'))