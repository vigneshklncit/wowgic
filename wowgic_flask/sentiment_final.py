import sentiment_mod as s

class wowgicRunClassifier:
    def __init__(self, feeds):
        self.feeds = feeds

    def runClassifier(self):
    	result =[]
    	for tweet in self.feeds:
            if 'text' in tweet:
            	obj = {}
            	sent = tweet['text']
            	print(sent)
            	print(s.sentiment(sent))
            	obj['id'] = tweet['id']
            	obj['category'] = s.sentiment(sent)[0]
            result.append(obj)
        return result
