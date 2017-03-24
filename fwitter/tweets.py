from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from time import time

from . import users

tweets = MongoClient()['Fwitter']['Tweets']

def add(userId, tweetContent):
    try:
        result = tweets.insert_one({
            'userId': userId,
            'username': users.getUsername(userId),
            'content': tweetContent,
            'timestamp': int(time())
        })
    except DuplicateKeyError:
        return None

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
