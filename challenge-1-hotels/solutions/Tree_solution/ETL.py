import pandas as pd

data_file_path = "data.csv"

df = pd.read_csv(data_file_path)
df.loc[:, ["name", "lon", "lat"]].to_csv("filtered.csv", index=None)
