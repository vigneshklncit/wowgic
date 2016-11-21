import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode, StatisticsError
from nltk.tokenize import word_tokenize



class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        print(votes)
        try:
            return mode(votes)
        except StatisticsError:
            return 'NA' 

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        try:
            choice_votes = votes.count(mode(votes))
            conf = choice_votes / len(votes)
            return conf
        except StatisticsError:
            return 'NA' 

class loadClassifier():
    def find_features(self,document):
        words = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in words)

        return features


    def loadPickle(self):
        
        documents_f = open("pickled_algos/documents.pickle", "rb")
        self.documents = pickle.load(documents_f)
        documents_f.close()


        word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
        self.word_features = pickle.load(word_features5k_f)
        word_features5k_f.close()
        
        featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
        self.featuresets = pickle.load(featuresets_f)
        featuresets_f.close()

        random.shuffle(self.featuresets)
        print(len(self.featuresets))
        length_val = len(self.featuresets)/2
        testing_set = self.featuresets[length_val:]
        training_set = self.featuresets[:length_val]



        open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
        self.classifier = pickle.load(open_file)
        open_file.close()


        open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
        self.MNB_classifier = pickle.load(open_file)
        open_file.close()



        open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
        self.BernoulliNB_classifier = pickle.load(open_file)
        open_file.close()


        open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
        self.LogisticRegression_classifier = pickle.load(open_file)
        open_file.close()


        open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
        self.LinearSVC_classifier = pickle.load(open_file)
        open_file.close()


        open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
        self.SGDC_classifier = pickle.load(open_file)
        open_file.close()




        self.voted_classifier = VoteClassifier(
                                          self.classifier,
                                          self.LinearSVC_classifier,
                                          self.MNB_classifier,
                                          self.BernoulliNB_classifier,
                                          self.LogisticRegression_classifier)




    def sentiment(self, text):
        feats = self.find_features(text)
        return self.voted_classifier.classify(feats),self.voted_classifier.confidence(feats)
