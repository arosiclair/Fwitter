from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

def add(userId, tweetContent):
    tweets = MongoClient()['Fwitter']['Tweets']
    try:
        result = tweets.insert_one({
            'userId': userId,
            'content': tweetContent
        })
    except DuplicateKeyError:
        return None

    if result.acknowledged:
        return str(result.inserted_id)
    else:
        return None