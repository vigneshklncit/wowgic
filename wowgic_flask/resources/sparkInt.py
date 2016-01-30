from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.mllib.util import MLUtils
import sys
sys.path.append('../common')
import loggerRecord
logger =  loggerRecord.get_logger()

#creating a standalone spark context
sc = SparkContext("local", "wowgicApp")


def Parallelized(data):
    ''' Parallelized collections are created by calling SparkContext's parallelize method
    '''
    # Load tweets into Spark for analysis
    allTweetsRDD = sc.parallelize(data)
    # Set up filter to only get tweets from the last week

    # Filter tweets to get rid of those who either have no hashtags or are too old
    filteredTweetsRDD = allTweetsRDD.filter(lambda t: t['id'] > 0)

    #words = allTweetsRDD.tweets_by_lang = tweets['lang'].value_counts()

    # Count each word in each batch
    #pairs = words.map(lambda word: (word, 1))
    #wordCounts = pairs.reduceByKey(lambda x, y: x + y)
    logger.debug('spark filteredTweetsRDD: %s',filteredTweetsRDD.count())
    return 1