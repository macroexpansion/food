import numpy as np
import pandas as pd
from recommender import CollaborativeFiltering

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

def recommend():
    cols = ['user_id', 'item_id', 'rating']
    ratings = pd.read_csv('data.dat', sep=' ', names=cols, encoding='latin-1')
    data = ratings.values
    # print(rate_train)

    rs = CollaborativeFiltering(data, k=30, mode='user')
    rs.fit()
    return rs.return_recommendation()

if __name__ == '__main__':
    # res = rec()
    # print(res)
    pass