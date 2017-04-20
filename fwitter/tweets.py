from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

import time, sys

from . import users, media
from utils import *

tweets = MongoClient(mongoDBUri)['Fwitter']['Tweets']

def add(userId, username, tweetContent, parentId, mediaIds):
    tweet = {
        'userId': userId,
        'username': username,
        'content': tweetContent,
        'timestamp': int(time.time()),
    }
    if parentId is not None:
        tweet['parentId'] = parentId
    if mediaIds is not None:
        tweet['media'] = mediaIds

    result = tweets.insert_one(tweet)

    if result.acknowledged:
        # if parentId is not None:
        #     result2 = tweets.find_one_and_update({'_id': ObjectId(parentId)},
        #                                {'$addToSet': {'replies': result.inserted_id}})
        #     if result2 is not None:
        #         return str(result.inserted_id)
        # else:
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
        if media.delete(result['media']):
            return True
        else:
            return False

def search(username, timestamp, limit, query, filtername, following, parentId, replies):
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

    if query is not None:
        filter['$text'] = {'$search': query}

    if parentId is not None:
        filter['parentId'] = parentId

    filter['parentId'] = {'$exists': True} if replies else {'$exists': False}

    results = tweets.find(filter, limit=limit)
    for tweet in results:
        tweet['id'] = str(tweet['_id'])
        del tweet['_id']

    return results

def likeTweet(tweetId, like):
    incr = 1 if like else -1
    result = tweets.find_one_and_update({'_id': ObjectId(tweetId)},
                                        {'$inc': {'likes': incr}})
    return True if result is not None else False
