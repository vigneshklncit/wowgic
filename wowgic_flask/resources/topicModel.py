#! /usr/bin/python
#===============================================================================
# File Name      : intercom.py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    :
# How to run     :twit_test.py -l info
#                :twit_test.py -h
#===============================================================================
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models, similarities
from collections import defaultdict
from bson import json_util
import json
import requests
import re
import sys
sys.path.append('common')
import loggerRecord,globalS
logger =  loggerRecord.get_logger()

stop_words = set(stopwords.words('english'))  
#word_set = []
lemmatizer = WordNetLemmatizer()
onlySentence = {} 


class topicModel:
    ''' gensim topic modelling - 
        Cration of corpus creation & dictionary creation should in written in iter methods <placeholder>
    '''
    def __init__(self, feeds):
        logger.debug('who invoked me ? hey u - %s',__name__)
        self.feeds = feeds
        self.dictionary = {}
        self.sentList=[]


    def __iter__(self):
        ''' The Iteration Protocol. is invoked while calling the class obj in for loop
        '''
        logger.debug('in iteration function')
        for tweet in self.feeds:
            if 'text' in tweet:
                sent = tweet['text']
                filtered_sentence = self.prepareSentence(sent)
                yield self.dictionary.doc2bow(filtered_sentence)
        logger.info('end of iteration function')

    def prepareSentence(self, sent):
        ''' lematizing the words and prepare the sentences
        '''
        #logger.debug('Entering function')
        sent=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",sent).split())
        sent =sent.replace("RT", "", 1)
        filtered_sentence1=[]
        word_tokens = nltk.word_tokenize(sent)
        pos_tag = nltk.pos_tag(word_tokens)
        for w in word_tokens:
            if w not in stop_words:
                lemWord = lemmatizer.lemmatize(w)
                lemWord = lemWord.lower()
                filtered_sentence1.append(lemWord)
        #logger.info('exiting function')
        return filtered_sentence1

    def tryPos(self):
        for tweet in self.feeds:
            if 'text' in tweet:
                sent = tweet['text']
                filtered_sentence1=[]
                word_tokens = nltk.word_tokenize(sent)
                pos_tag = nltk.pos_tag(word_tokens)
                allowed_word_types = ["N","V"]
                print(pos_tag)
                for w in pos_tag:
                    '''print(w[1][0])
                    print('\n')'''
                    if w[1][0] in allowed_word_types:
                        filtered_sentence1.append(w[0].lower())
                logger.debug('---------------------')        
                logger.debug(' %s',sent)
                logger.debug(' %s',filtered_sentence1)
                logger.debug('**********************')
    
    def createDictionary(self, keyword):
        
        allowed_word_types = ["NNP","NNS","CD"]
        ''' The mapping between the questions and ids is called a dictionary
        '''
        #logger.debug('Entering function')
        for tweet in self.feeds:
            if 'text' in tweet:
                sent = tweet['text']
                #filtered_sentence = self.prepareSentence(sent)
                #call the prepareSentence function <placeholder>
                sent=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",sent).split())
                sent =sent.replace("RT", "", 1)
                filtered_sentence1=[]
                filtered_sentence2 = []
                word_tokens = nltk.word_tokenize(sent)
                for w in word_tokens:
                    if w not in stop_words and w != keyword:
                        lemWord = lemmatizer.lemmatize(w)
                        lemWord = lemWord.lower()
                        filtered_sentence1.append(lemWord)
            pos_tag = nltk.pos_tag(filtered_sentence1)
            for w in pos_tag:
                if w[1] not in allowed_word_types:
                    filtered_sentence2.append(w[0].lower())

            self.sentList.append(set(filtered_sentence2))
        #logger.debug('create dict sent length %s',len(self.sentList))
        # to create unique dictionary words
        logger.debug('self.sentList %s',self.sentList)
        self.dictionary = corpora.Dictionary(self.sentList)
        logger.debug(self.dictionary.token2id)
        #self.dictionary = dictionary
        #logger.info('exiting function')
        return self.dictionary

    def createLSIModel(self,corpus,feeds = '', keyword =''):
        ''' actually convert tokenized documents to vectors
        '''
        #corpus = [self.dictionary.doc2bow(text) for text in self.sentList]
        lsi = models.LsiModel(corpus, id2word=self.dictionary,num_topics= 300)
        index = similarities.MatrixSimilarity(lsi[corpus])
        #initialising an array which store the similarity tweets
        similarTweet_Id = []
        parentId = []
        parentToChildMap ={}
        childId = []
        processedTweet = []
        similarTweet_Ratio = []
        ogTweets = 0
        similarTweetId_parentId = []
        if feeds == '':
            feeds = self.feeds 
        #logger.debug('new corpus length :%s ',len(feeds))
        for tweet in feeds:
            if tweet['id'] not in processedTweet:
                if 'text' in tweet:
                    ogTweets += 1
                    #logger.debug('chelloi tweet text :%s', tweet) # logger.debug (document_number, document_similarity) 2-tuples
                    #filtered_sentence = self.prepareSentence(sentence)
                    #call the prepareSentence function <placeholder>
                    sentence=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet['text']).split())
                    sentence =sentence.replace("RT", "", 1)
                    word_tokens = nltk.word_tokenize(sentence)
                    filtered_sentence = ''
                    for w in word_tokens:
                        w = w.lower()
                        if w not in stop_words and w != keyword:
                            lemWord = lemmatizer.lemmatize(w)
                            filtered_sentence += lemWord+' '

                    if len(filtered_sentence.split()) >= 4:
                    
                        vec_bow = self.dictionary.doc2bow(filtered_sentence.split())
                        vec_lsi = lsi[vec_bow] # convert the query to LSI space
                        sims = index[vec_lsi] # perform a similarity query against the corpus
                        #logger.debug(list(enumerate(sims))) # logger.debug (document_number, document_similarity) 2-tuples
                        sims = sorted(enumerate(sims), key=lambda item: -item[1])
                        #logger.debug(sims)
                     
                        logger.debug('\n\n\n\n----------------Start title------------')
                        logger.debug(tweet['text'])
                        logger.debug('id:%s',tweet['id'])
                        word_tokens = nltk.word_tokenize(sentence)
                        pos_tag = nltk.pos_tag(word_tokens)
                        print(pos_tag)
                        allowed_word_types = []
                        filtered_sentence1 = []
                        for w in pos_tag:
                            if w[1] not in allowed_word_types:
                                filtered_sentence1.append(w[0].lower())
                        print("#####",filtered_sentence1,"#####")
                        logger.debug('----------titlke End ---------')
                        parentId.append(tweet['id'])
                        parentChildList = []
                        for sim in sims:
                            if sim[1] > 0.70:
                                childDict = {}
                                indexKey = sim[0]
                                if self.feeds[indexKey]:
                                    if sim[1] != 1.0 and feeds[indexKey]['id'] != tweet['id'] and feeds[indexKey]['id'] not in processedTweet:
                                        childDict['id'] = feeds[indexKey]['id']
                                        childDict['parent'] = tweet['id']
                                        childDict['ratio'] = sim[1]
                                        parentChildList.append(feeds[indexKey]['id']) 
                                        childId.append(childDict)
                                    
                                    logger.debug('******** sims[0]%s',sim[0])
                                    logger.debug(sim[1])
                                    logger.debug(self.feeds[indexKey]['id'])
                                    logger.debug(self.feeds[indexKey].get('text'))
                                    logger.debug('=========')
                                    processedTweet.append(feeds[indexKey]['id'])
                        parentToChildMap[tweet['id']] = parentChildList
        '''
        logger.debug('totoal no tweets: %s, Total no of parent tweets: %s, Total no of child tweets: %s',len(self.feeds), ogTweets,len(similarTweet_Id))
        logger.debug('length of id : %s, ratio : %s, parentId : %s', len(similarTweet_Id),len(similarTweet_Ratio),len(similarTweetId_parentId))'''
        #logger.debug('parentToChildMap %s',parentToChildMap)
        similarTweet = [parentId, childId, parentToChildMap]
      #  logger.info('similarTweets wrt to corpus: %s',similarTweet)
        return similarTweet
                
