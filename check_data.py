import pandas as pd

df = pd.read_csv("cable_landing_stations.csv")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst row sample:")
print(df.iloc[0])