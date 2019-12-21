import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import scipy
import pandas as pd


class CollaborativeFiltering:
    def __init__(self, data, k=5, mode='user', distance_function=cosine_similarity):
        self.distanceOf = distance_function
        self.mode = mode
        self.knearest = k
        self.data = data if mode == 'user' else data[:, [1,0,2]]
        self.Ybar_data = None

        self.n_users = int(np.max(self.data[:, 0])) + 1
        self.n_items = int(np.max(self.data[:, 1])) + 1

    def add(self, new_data):
        self.data = np.concatenate((self.data, new_data), axis=0)

    def normalize(self):
        users = self.data[:, 0] # all users - first col of the data
        self.Ybar_data = self.data.copy()
        self.means = np.zeros((self.n_users,))
        for n in range(self.n_users):
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.data[ids, 1] 
            ratings = self.data[ids, 2]

            mean_rating = np.mean(ratings) 
            if np.isnan(mean_rating):
                mean_rating = 0
            self.means[n] = mean_rating

            self.Ybar_data[ids, 2] = ratings - self.means[n]

        self.Ybar = scipy.sparse.coo_matrix(
            (self.Ybar_data[:, 2],(self.Ybar_data[:, 1], self.Ybar_data[:, 0])), 
            (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        self.sim = self.distanceOf(self.Ybar.T, self.Ybar.T)

    def refresh(self):
        self.normalize()
        self.similarity()

    def fit(self):
        self.refresh()

    def __pred(self, user, item, normalized = True):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all users who rated i
        ids = np.where(self.data[:, 1] == item)[0].astype(np.int32)
        users_rated_i = (self.data[ids, 0]).astype(np.int32) 
        # Step 2: find similarity btw the current user and others 
        # who already rated i
        sim = self.sim[user, users_rated_i]
        # Step 4: find the k most similarity users
        k_nearest_user = np.argsort(sim)[-self.knearest:] 
        # and the corresponding similarity levels
        nearest_sim = sim[k_nearest_user]
        # How did each of 'near' users rated item i
        rated = self.Ybar[item, users_rated_i[k_nearest_user]]
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (rated * nearest_sim)[0] / (np.abs(nearest_sim).sum() + 1e-8)

        return (rated * nearest_sim)[0] / (np.abs(nearest_sim).sum() + 1e-8) + self.means[user]
    
    def pred(self, user, item, normalized = True):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.mode == 'user': 
            return self.__pred(user, item, normalized)
        return self.__pred(item, user, normalized)

    def recommend(self, user, normalized = 1):
        """
        Determine all items should be recommended for user u. (mode =1)
        or all users who might have interest on item u (mode = 0)
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which 
        have not been rated by u yet. 
        """
        ids = np.where(self.data[:, 0] == user)[0]
        items_rated_by_user = self.data[ids, 1].tolist()              
        recommended_items = []

        # print('item %s, rated by %s' % (user, items_rated_by_user))
        for i in range(self.n_items):
            # rating = self.__pred(user, i)
            # if rating > 0: 
            #     recommended_items.append(i)

            if i not in items_rated_by_user:
                rating = self.__pred(user, i)
                if rating > 0: 
                    recommended_items.append(i)
        
        return recommended_items 

    def print_recommendation(self):
        """
        print all items which should be recommended for each user 
        """
        print('Recommendation: ')
        for user in range(self.n_users):
            recommended_items = self.recommend(user)

            if self.mode == 'user':
                print('Recommend item(s): {}, to user {}'.format(recommended_items, user))
            else: 
                print('Recommend item {} to user(s): {} '.format(user, recommended_items))