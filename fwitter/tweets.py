from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

import time, sys

from . import users
from utils import *

tweets = MongoClient(mongoDBUri)['Fwitter']['Tweets']

def add(userId, username, tweetContent):
    result = tweets.insert_one({
        'userId': userId,
        'username': username,
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

def delete(userId, tweetId):
    result = tweets.find_one_and_delete({'_id': ObjectId(tweetId), 'userId': userId})
    if result is not None:
        return True

def search(username, timestamp, limit, query, filtername, following):
    filter = {'timestamp': {'$lte': timestamp}}

    if following:
        followedUsers = users.getFollowing(username, sys.maxint)
        if filtername is not None:
            if filtername in followedUsers:
                filter['username'] = filtername
            else:
                return []
        else:
            filter['username'] = {'$in': followedUsers}
    elif filtername is not None:
        filter['username'] = filtername


    results = tweets.find(filter, limit=limit)
    resultTweets = []
    for tweet in results:
        id = str(tweet['_id'])
        del tweet['_id']
        tweet['id'] = id
        resultTweets.append(tweet)

    return resultTweets
