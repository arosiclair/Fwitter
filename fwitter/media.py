from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary

from utils import *

media = MongoClient(mediaUri)['Fwitter']['Media']

def add(bytes):
    result = media.insert_one({'content': Binary(bytes)})
    if result.acknowledged:
        return str(result.inserted_id)

def get(mediaId):
    return media.find_one({'_id': ObjectId(mediaId)})