from pymongo import MongoClient
import pandas as pd
import os
import certifi

client = MongoClient(os.getenv("connection_url"),tlsCAFile = certifi.where())
print(os.getenv("connection_url"))
db = client["resume"]
collection = db["resume_dataset"]

df = pd.read_csv(r"data\dataset.csv")
print(df)
data = df.to_dict(orient="records")

collection.insert_many(data)

print("Done")