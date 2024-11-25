import DBManager as dbm
import pandas as pd

db = dbm.DBManager()

db.init_database()

with open("ecolabel_dataset.csv", 'r', encoding='utf-8') as fin:
    data = pd.read_csv(fin)

# print(data[data.index < 10])

for r in data.iterrows():
    info = {
        "name": r[1][0],
        "short_description": r[1][3],
        "description": r[1][1],
        "image_url": r[1][2]
    }
    
    db.insert_ecolabel(info)

db.close_database_connection()