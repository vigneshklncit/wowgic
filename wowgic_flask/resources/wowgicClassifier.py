import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
import glob
import loggerRecord
logger =  loggerRecord.get_logger()
class wowgicNaiveBayes:
    def __init__(self):  
        #self.feeds = feeds
        self.all_words = []
        self.documents = []


    def find_features(self, document):
        words = word_tokenize(document)
        features = {}
        print('\n \n Actual teet %s',document)
        for w in self.word_features:
            features[w] = (w in words)
        print('\n \n PROCESSED WORDS %s',features)
        return features

    def createClassifiers(self):

        logger.debug('list file %s',glob.glob("trainingData/*.txt"))
        trainingFiles = glob.glob("trainingData/*.txt")
        allowed_word_types=['N','V','J']
        otherStopWords = ['for','best','s','amp','a','the','me','at','here','chennai']
        stop_words = set(stopwords.words('english'))
        classifierResult = {}
        for trFile in trainingFiles:
            category = os.path.basename(trFile)
            category = os.path.splitext(category)[0]
            short_pos = open(trFile,"r").read()
            for p in short_pos.split('\n'):
                sent=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",p).split())
                self.documents.append((sent, category))
                words = word_tokenize(sent)
                pos = nltk.pos_tag(words)
                for w in pos:
                    word = w[0].lower()
                    if w[1][0] in allowed_word_types and word not in stop_words and word not in otherStopWords:
                        logger.debug('adjectivesss %s',w[0])
                        self.all_words.append(word)
                    else:                        
                        logger.debug('banned words3456 %s',w[0].lower())
                    #logger.debug('banned1 words123 %s',w[0].lower())
        #logger.debug('all words345 %s',self.all_words)        
        #return
        save_documents = open("pickled_algos/documents.pickle","wb")
        pickle.dump(self.documents, save_documents)
        save_documents.close()
        self.all_words = nltk.FreqDist(self.all_words)
        self.word_features = list(self.all_words.keys())[:5000]
        save_word_features = open("pickled_algos/word_features5k.pickle","wb")
        pickle.dump(self.word_features, save_word_features)
        save_word_features.close()

        featuresets = [(self.find_features(rev), category) for (rev, category) in self.documents]
        logger.debug('featuresets %s',featuresets)
        logger.debug('length of feature sets %s',len(featuresets))
        random.shuffle(featuresets)
        #return
        save_feature_sets = open("pickled_algos/featuresets.pickle","wb")
        pickle.dump(featuresets, save_feature_sets)
        save_feature_sets.close()
        print(len(featuresets))
        splitLength = len(featuresets)/2
        testing_set = featuresets[(splitLength):]
        training_set = featuresets[:(splitLength)]

        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
        classifier.show_most_informative_features(15)

        ###############
        save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
        pickle.dump(classifier, save_classifier)
        save_classifier.close()

        MNB_classifier = SklearnClassifier(MultinomialNB())
        MNB_classifier.train(training_set)
        print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
        classifierResult['MNB_classifier'] = (nltk.classify.accuracy(MNB_classifier, testing_set))*100

        save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
        pickle.dump(MNB_classifier, save_classifier)
        save_classifier.close()

        BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        BernoulliNB_classifier.train(training_set)
        print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
        classifierResult['BernoulliNB_classifier'] = (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100

        save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
        pickle.dump(BernoulliNB_classifier, save_classifier)
        save_classifier.close()

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier.train(training_set)
        print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
        classifierResult['LogisticRegression_classifier'] = (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100

        save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
        pickle.dump(LogisticRegression_classifier, save_classifier)
        save_classifier.close()


        LinearSVC_classifier = SklearnClassifier(LinearSVC())
        LinearSVC_classifier.train(training_set)
        print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
        classifierResult['LinearSVC_classifier'] = (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100

        save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
        pickle.dump(LinearSVC_classifier, save_classifier)
        save_classifier.close()


        ##NuSVC_classifier = SklearnClassifier(NuSVC())
        ##NuSVC_classifier.train(training_set)
        ##print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


        SGDC_classifier = SklearnClassifier(SGDClassifier())
        SGDC_classifier.train(training_set)
        print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)
        classifierResult['SGDClassifier'] = nltk.classify.accuracy(SGDC_classifier, testing_set)*100

        save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
        pickle.dump(SGDC_classifier, save_classifier)
        save_classifier.close()
        return classifierResult