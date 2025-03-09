import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 
from sentence_transformers import SentenceTransformer, util
from learnlog.models import LearnLog
from learning_outcomes.models import Learning_Outcome

import pickle

course_similarities = None
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
        
    def __pred(self, u, i, normalized=1, student_id = None, course_id = None):
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

        if not check_course_has_score(course_id): # if there is no score or no student has score for course i
            return predict_score_with_learning_outcome(student_id, course_id)
        
        if normalized:
            return (r * nearest_student).sum() / (np.abs(nearest_student).sum() + 1e-8)
        return (r * nearest_student).sum() / (np.abs(nearest_student).sum() + 1e-8) + self.mu[u]



    def pred(self, u, i, normalized=1, student_id = None, course_id = None):
        if self.uuCF:
            score = self.__pred(u, i, normalized, student_id, course_id)
            if type(score) == np.float64:
                if score > 10:
                    return 10
                else:
                    return score
            return score
        return self.__pred(i, u, normalized, student_id, course_id)
    
    
def predict_score_with_learning_outcome(student_id, course_id, top_k = 10):
    try:
        global course_similarities
        if course_similarities is None:
            with open("course_similarity.pkl", "rb") as f:
                course_similarities = pickle.load(f)
                
        similar_courses = sorted(course_similarities.get(course_id, {}).items(), key=lambda x: x[1], reverse=True)[:top_k]
    
        learnlog = LearnLog.objects.filter(student=student_id)
        total_weight = 0
        weighted_score_sum = 0
        
        for similar_course, similarity in similar_courses:
            learnlog_instance = learnlog.filter(course__course_code=similar_course).first()
            if learnlog_instance:
                weighted_score_sum += similarity * float(learnlog_instance.score)
                total_weight += similarity

        predicted_score = weighted_score_sum / (total_weight + 1e-8)
        return float(predicted_score)
    
       
    except Exception as e:
        return str(e)
    
def check_course_has_score(course_id):
    try:
        learnlog = LearnLog.objects.filter(course__course_code=course_id).first()
        if learnlog:
            return True
        return False
    except Exception as e:
        return False