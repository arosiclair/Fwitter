from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

import time

from . import users

tweets = MongoClient()['Fwitter']['Tweets']

def add(userId, tweetContent):
    result = tweets.insert_one({
        'userId': userId,
        'username': users.getUsername(userId),
        'content': tweetContent,
        'timestamp': int(time.time())
    })

    if result.acknowledged:
        return str(result.inserted_id)
    else:
        return None

def get(tweetId):
    result = tweets.find_one({ '_id': ObjectId(tweetId) })
    if result is not None:
        del result['_id']
        result['id'] = tweetId
        return result

def search(timestamp, limit):
    results = tweets.find({'timestamp': {'$lte': timestamp}}, limit=limit)
    resultTweets = []
    for tweet in results:
        id = str(tweet['_id'])
        del tweet['_id']
        tweet['id'] = id
        resultTweets.append(tweet)

    return resultTweets
