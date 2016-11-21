import sentiment_mod as s

class wowgicRunClassifier:
    def __init__(self, feeds):
        self.sObj = s.loadClassifier()
        self.sObj.loadPickle()
        self.feeds = feeds

    def runClassifier(self):
    	result =[]
    	for tweet in self.feeds:
            if 'text' in tweet:
            	obj = {}
            	sent = tweet['text']
            	print(sent)
            	print(self.sObj.sentiment(sent))
            	obj['id'] = tweet['id']
            	temp = self.sObj.sentiment(sent)
                obj['category'] =  temp[0]
            result.append(obj)
        return result
