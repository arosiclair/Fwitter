from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, InvalidOperation
from bson.objectid import ObjectId

import string, random
from datetime import datetime

from utils import keygen

users = MongoClient()['Fwitter']['Users']

def add(username, email, password):
    verifyKey = keygen()
    try:
        result = users.insert_one({
            'username': username,
            'email': email,
            'password': password,
            'verified': False,
            'verifyKey': verifyKey,
            'following': [],
            'followers': []
        })
    except DuplicateKeyError:
        return None

    if result.acknowledged:
        return verifyKey
    else:
        return None

def verify(email, key):
    if key == "abracadabra":
        user = users.find_one({ 'email': email })
    else:
        user = users.find_one({
            'email': email,
            'verifyKey': key
        })

    if user is not None:
        result = users.update_one({ "_id" : user['_id'] },
                         {'$set': { 'verified': True } })
        return result.acknowledged
    else:
        return False

def login(username, password):
    userDoc = users.find_one({
        'username': username,
        'password': password
    })

    if userDoc is not None and userDoc['verified'] == True:
        return str(userDoc['_id'])
    else:
        return None

def getUsername(userId):
    user = users.find_one({'_id': ObjectId(userId)})
    if user is not None:
        return user['username']
    else:
        return None

def getId(username):
    user = users.find_one({'username': username})
    if user is not None:
        return str(user['_id'])
    else:
        return None

def follow(userId, followName):
    user = users.find_one({'_id': ObjectId(userId)})
    followed = users.find_one({'username': followName})

    if user is None or followed is None:
        return False
    else:
        userResult = users.update_one({'_id': user['_id']},
                         {'$addToSet': {'following': str(followed['username'])}})
        followedResult = users.update_one({'_id': followed['_id']},
                         {'$addToSet': {'followers': str(user['username'])}})

        try:
            if userResult.modified_count == 1 and followedResult.modified_count == 1:
                return True
            else:
                return False
        except InvalidOperation:
            return False

def getInfo(username):
    user = users.find_one({'username': username})
    if user is not None:
        return {'email': user['email'],
                'followers': len(user['followers']),
                'following': len(user['following'])}

def getFollowers(username, limit):
    user = users.find_one(({'username': username}))
    if user is not None:
        return user['followers'][: limit]

def getFollowing(username, limit):
    user = users.find_one(({'username': username}))
    if user is not None:
        return user['following'][: limit]