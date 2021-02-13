import sys
import os

from pymongo import MongoClient
import pandas

def read_data_values(data_dir):
    """Возвращает (values, collection_name)"""
    res = []
    for file_in_dir in os.listdir(data_dir):
        if file_in_dir.endswith('.csv'):
            csv_data_path = os.path.join(data_dir, file_in_dir)
            csv_data_frame = pandas.read_csv(csv_data_path)
            collection_name = file_in_dir.split('.')[0]
            res.append((csv_data_frame.values, collection_name))
    return res

def connect_db(host, port, db_name):
    mongo_client = MongoClient(host=host, port=port)
    return mongo_client[db_name]

def main():
    data_dir = sys.argv[1]
    db_host = sys.argv[2]
    db_port = int(sys.argv[3])
    db_name = sys.argv[4]
    db = connect_db(host=db_host, port=db_port, db_name=db_name)
    data = read_data_values(data_dir)
    for values, collection_name in data:
        data = [dict([tuple(row)]) for row in values]
        db[collection_name].insert_many(data)
    
    # Проверка, что данные вставились
    collections = db.list_collection_names()
    print('inserted collections => ', collections)
    assert(len(collections) == len(data))
    
    print('data successfully filled in DB')
    
main()
