from joblib import load
from nlp import featurize

class Model():
    
    def __init__(self):
        self._pipeline = load('training/vector.joblib')

    def score(self, candidate):
        ft = featurize(candidate['title'] + ' ' + candidate['description'])['vector']
        return self._pipeline.predict_proba([ft])[0, 1]
