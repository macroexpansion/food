import flask
import numpy as np
import pandas as pd
import pymongo
from bson.objectid import ObjectId
import time, random

from recommender import CollaborativeFiltering

srv = 'mongodb+srv://dung18dv:dangvandung1811@cluster0-zzvgt.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(srv)
collections = client['test']
dishes = collections['dishes']

dblist = client.list_database_names()
# print(dblist)
# if 'test' in dblist:
#     print("The database exists.")

# collist = collections.list_collection_names()
# print(collist)
# print(list(DishMetric.find()))
# a = ['Cơm rang dưa bò', 'Phở bò', 'Phở gà', 'Bún vịt', 'Bún cua', 'Mì quảng', 'Miến lươn', 'Bún trộn']
# for i in a:
#     obj = {
#         'name': i,
#         'category': ''
#     }
#     res = dishes.insert_one(obj).inserted_id
#     print(res)

# for x in dishes.find():
    # print(x)

useractions = collections['useractions']
for i in range(random.randint(3,10)):
    # res = useractions.insert_one(a).inserted_id
    a = {
        "_id": ObjectId(),
        "type" : "search",
        "user" : ObjectId("5e08763727440628633c68fd"),
        "dish" : ObjectId("5e08467635cd117771d9f45d")
    }
    useractions.update_one( {'_id': a['_id'] }, { "$set": a }, upsert=True)
    print(i)

# for x in useractions.find():
#     print(x)

