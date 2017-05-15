from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary

from utils import *

media = MongoClient(mongoDBUri)['Fwitter']['Media']

def add(bytes):
    result = media.insert_one({'content': Binary(bytes)})
    if result.acknowledged:
        return str(result.inserted_id)

def get(mediaId):
    return media.find_one({'_id': ObjectId(mediaId)})

def delete(mediaIds):
    for i in xrange(0, len(mediaIds)):
        mediaIds[i] = ObjectId(mediaIds[i])

    result = media.delete_many({'_id': {'$in': mediaIds}})
    if result.acknowledged and result.deleted_count == len(mediaIds):
        return True
    else:
        return False