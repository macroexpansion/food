
# r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

# ratings_base = pd.read_csv('ml-100k/ub.base', sep='\t', names=r_cols, encoding='latin-1')
# ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

# rate_train = ratings_base.values
# rate_test = ratings_test.values

# # indices start from 0
# rate_train = rate_train[:, :3] - 1
# rate_test = rate_test[:, :3] - 1

# cols = ['user_id', 'item_id', 'rating']
# ratings = pd.read_csv('data.dat', sep = ' ', names = cols, encoding='latin-1')
# data = ratings.values
# print(rate_train)

# rs = CollaborativeFiltering(data, k = 30, mode='item')
# rs.fit()
# rs.print_recommendation()

# n_tests = rate_test.shape[0]
# SE = 0 # squared error
# for n in range(n_tests):
#     pred = rs.pred(rate_test[n, 0], rate_test[n, 1], normalized = False)
#     SE += (pred - rate_test[n, 2])**2 
# RMSE = np.sqrt(SE/n_tests)
# print('Item-item CF, RMSE =', RMSE)
import numpy as np
import pandas as pd
from recommender import CollaborativeFiltering
import flask
import pymongo
from bson.objectid import ObjectId
import time

from recommender import CollaborativeFiltering


srv = 'mongodb+srv://dung18dv:dangvandung1811@cluster0-zzvgt.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(srv)
collections = client['test']
dishes = collections['dishes']
users = collections['users']
useractions = collections['useractions']
recommendations = collections['recommendations']

user_list = [user['_id'] for user in users.find({ 'type': 'customer' })]
dish_list = [dish['_id'] for dish in dishes.find()]

def recommend():
    cols = ['user_id', 'item_id', 'rating']
    ratings = pd.read_csv('data.csv', sep=' ', names=cols, encoding='latin-1')
    data = ratings.values
    # print(rate_train)
    try:
        rs = CollaborativeFiltering(data, k=30, mode='user')
        rs.fit()
        results = rs.return_recommendation(user_list, dish_list)
        for result in results:
            recommendations.update_one( { 'user':  result['user']}, { "$set": result }, upsert=True)
    except:
        return {'message': 'error'}

    return {'message': 'success'}

def get_data():
    with open('data.csv', 'w') as f:
        for user_idx, user in enumerate(user_list):
            print(user_idx)
            for dish_idx, dish in enumerate(dish_list):
                ratings = useractions.count_documents({ 'type': 'search', 'user': user['_id'], 'dish': dish['_id'] })
                if ratings == 0:
                    continue

                sequence = '{} {} {}\n'.format(user_idx, dish_idx, ratings)
                f.write(sequence)


if __name__ == '__main__':
    get_data()
    res = recommend()
    print(res)
    pass