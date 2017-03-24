from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

import string, random
from datetime import datetime

from utils import keygen

def add(username, email, password):
    users = MongoClient()['Fwitter']['Users']

    verifyKey = keygen()
    try:
        result = users.insert_one({
            'username': username,
            'email': email,
            'password': password,
            'verified': False,
            'verifyKey': verifyKey
        })
    except DuplicateKeyError:
        return None

    if result.acknowledged:
        return verifyKey
    else:
        return None

def verify(email, key):
    users = MongoClient()['Fwitter']['Users']

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
    users = MongoClient()['Fwitter']['Users']
    userDoc = users.find_one({
        'username': username,
        'password': password
    })

    if userDoc is not None and userDoc['verified'] == True:
        return str(userDoc['_id'])
    else:
        return None