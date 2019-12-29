import flask
import numpy as np
import pandas as pd
import pymongo

from recommender import CollaborativeFiltering

srv = 'mongodb+srv://dung18dv:dangvandung1811@cluster0-zzvgt.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(srv)
collections = client['test']
DishMetric = collections['dishes']

dblist = client.list_database_names()
# print(dblist)
# if 'test' in dblist:
#     print("The database exists.")

collist = collections.list_collection_names()
# print(collist)
# print(list(DishMetric.find()))
for x in DishMetric.find():
    print(x)
