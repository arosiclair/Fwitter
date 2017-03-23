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
            'name': username,
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