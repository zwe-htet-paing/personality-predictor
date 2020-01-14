from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVR
from sklearn.svm import SVC

class Model():
    def __init__(self):
        self.svr = SVR(kernel='linear')
        self.svc = SVC(kernel='linear')
        self.tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')

    def fit(self, X, y, regression=True):
        X = self.tfidf.fit_transform(X)
        if regression:
            self.svr = self.svr.fit(X, y)
        else:
            self.svc = self.svc.fit(X, y)

    def predict(self, X, regression=True):
        X = self.tfidf.transform(X)
        if regression:
            return self.svr.predict(X)
        else:
            return self.svc.predict(X)
