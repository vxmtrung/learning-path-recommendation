import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 

class CF:
    """Collaborative Filtering"""
    def __init__(self, Y_data, k, dist_func=cosine_similarity, uuCF=1, students = None, courses = None):
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF
        self.Y_data = np.array(Y_data if uuCF else Y_data[:, [1, 0, 2]], dtype=object)
        self.k = k  # number of nearest neighbors
        self.dist_func = dist_func
        self.Ybar_data = None
        self.students = students
        self.courses = courses
        
    def normalize_Y(self):
        users = self.Y_data[:, 0] # all users
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros(len(self.students)) # mean score of each student
       
        for n in range(len(self.students)):
            ids = np.where(users == n)[0] # indices of scores of student 
            scores = self.Y_data[ids, 2] # scores of student n
            mean = 0 
            count = 0
            for score in scores:
                if score != None:
                    mean += score
                    count += 1
            mean = mean/count 
            self.mu[n] = mean
            # normalize
            for i in ids:
                if self.Ybar_data[i, 2] is not None: 
                    self.Ybar_data[i, 2] -= self.mu[n]
                else:
                    self.Ybar_data[i, 2] = 0
 
        # Create the sparse matrix
        row_indices = self.Ybar_data[:, 0]
        col_indices = self.Ybar_data[:, 1]
        scores = self.Ybar_data[:, 2].astype(float)
        self.Ybar = sparse.coo_matrix((scores, (col_indices, row_indices)), shape=(len(self.courses), len(self.students)))
        
    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
    
    def fit(self):
        self.normalize_Y()
        self.similarity()
        
    def __pred(self, u, i, normalized=1):
        # print("Ybar ", self.Ybar)
        student_ids = np.where(self.Y_data[:, 1] == i)[0]  # Find the indices of students who has score for course i
        students = self.Y_data[student_ids, 0].astype(int)  # Get student
        sim = self.S[u, students]  # Get the similarity between student u and students who has score for course i
        a = np.argsort(sim)[-self.k:]  # Keep k students who has the highest similarity
        nearest_student = sim[a]  # Get the similarity of the nearest students

    
        if isinstance(self.Ybar, sparse.coo_matrix):
            rows = np.where(self.Ybar.row == i)[0]  # Find the indices of rows (courses) which has value i
            cols = self.Ybar.col[rows]  # Get the user indices from the corresponding columns
            r = self.Ybar.data[rows][np.isin(cols, students[a])]  
        else:
            r = self.Ybar[i, students[a]]  # Truy cập giá trị từ ma trận dense

        if normalized:
            return (r * nearest_student).sum() / (np.abs(nearest_student).sum() + 1e-8)
        return (r * nearest_student).sum() / (np.abs(nearest_student).sum() + 1e-8) + self.mu[u]



    def pred(self, u, i, normalized=1):
        if self.uuCF:
            score = self.__pred(u, i, normalized)
            if score > 10:
                return 10
            return score
        return self.__pred(i, u, normalized)