from django.shortcuts import render, redirect
from django.http import JsonResponse

from json import loads
import time

from . import users, tweets

def index(request):
    return render(request, 'fwitter/index.html')

def adduser(request):
    if request.method == "POST":
        content = loads(request.body)
        try:
            name = content['username']
            email = content['email']
            password = content['password']
        except:
            return JsonResponse({'status': 'error', 'error': 'adduser - incorrect parameters'})
    else:
        return JsonResponse({'status': 'error', 'error': 'request is not POST'})

    verifyKey = users.add(name, email, password)
    if verifyKey is not None:
        # TODO: email verification key
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error', 'error': 'add user failed'})

def verify(request):
    if request.method == "POST":
        content = loads(request.body)
        try:
            email = content['email']
            key = content['key']
        except KeyError:
            return JsonResponse({'status': 'error', 'error': 'verify - incorrect parameters'})
    else:
        return JsonResponse({'status': 'error', 'error': 'request is not POST'})

    if users.verify(email, key):
        #request.session['verified'] = True
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error', 'error': 'verify - failed'})

def login(request):
    if request.method == "POST":
        content = loads(request.body)
        try:
            username = content['username']
            password = content['password']
        except KeyError:
            return JsonResponse({'status': 'error', 'error': 'login - incorrect parameters'})
    else:
        return JsonResponse({'status': 'error', 'error': 'request is not POST'})

    userId = users.login(username, password)
    if userId is not None:
        # Save MongoDB doc ID in cookie data for user
        request.session['userId'] = userId
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error', 'error': 'login - failed'})

def logout(request):
    try:
        del request.session['userId']
        # request.session['loggedOut'] = True
    except KeyError:
        pass
    return JsonResponse({ 'status': 'OK'})

def additem(request):
    if request.method == "POST":
        content = loads(request.body)
        try:
            tweetContent = content['content']
        except KeyError:
            return JsonResponse({'status': 'error', 'error': 'additem - incorrect parameters'})
    else:
        return JsonResponse({'status': 'error', 'error': 'request is not POST'})

    userId = request.session.get('userId', None)
    if userId is None:
        return JsonResponse({'status': 'error', 'error': 'additem - user not logged in'})

    tweetId = tweets.add(userId, tweetContent)
    if tweetId is not None:
        return JsonResponse({'status': 'OK', 'id': tweetId})
    else:
        return JsonResponse({'status': 'error', 'error': 'additem - tweet post failed'})

def getitem(request, tweetId):
    if request.method == "GET":
        result = tweets.get(tweetId)
        if result is not None:
            return JsonResponse({
                'status': 'OK',
                'item': result
            })
        else:
            return JsonResponse({'status': 'error', 'error': 'tweet GET failed'})
    elif request.method == "DELETE":
        return deleteitem(request, tweetId)
    else:
        return JsonResponse({'status': 'error', 'error': 'item - request method {0} is not allowed'.format(request.method)})

def deleteitem(request, tweetId):
    userId = request.session.get("userId", None)
    if userId is None:
        return JsonResponse({'status': 'error', 'error': 'delete - user not logged in'})

    result = tweets.delete(userId, tweetId)
    if result:
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error',
                             'error': 'delete - tweetId {0} from user {1} was not found'.format(tweetId, userId)})

def search(request):
    userId = request.session.get('userId', None)
    if userId is None:
        return JsonResponse({'status': 'error', 'error': 'search - user not logged in'})

    if request.method == "POST":
        content = loads(request.body)
        timestamp = content.get('timestamp', int(time.time()))
        limit = content.get('limit', 25)
        if limit < 0 or limit > 100:
            limit = 25
    else:
        return JsonResponse({'status': 'error', 'error': 'search - request is not POST'})

    tweetList = tweets.search(timestamp, limit)
    return JsonResponse({
        'status': 'OK',
        'items': tweetList
    })

def follow(request):
    userId = request.session.get('userId', None)
    if userId is None:
        return JsonResponse({'status': 'error', 'error': 'follow - user not logged in'})

    if request.method == "POST":
        content = loads(request.body)
        try:
            username = content['username']
        except KeyError:
            return JsonResponse({'status': 'error', 'error': 'follow - no username provided'})
        follow = content.get('follow', True)

        result = users.follow(userId, username)
        if result:
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'error', 'error': "follow - a user wasn't found or write failed"})
    else:
        return JsonResponse({'status': 'error', 'error': 'follow - request is not POST'})

def getUserInfo(request, username):
    if request.method == "GET":
        result = users.getInfo(username)
        if result is not None:
            return JsonResponse({'status': 'OK',
                                 'user': result})
        else:
            return JsonResponse({'status': 'error', 'error': 'username - user not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'username - request is not GET'})

def getUserFollowers(request, username):
    if request.method == "GET":
        limit = request.GET.get('limit', 50)
        if limit > 200 or limit < 0:
            limit = 50

        result = users.getFollowers(username, limit)
        if result is not None:
            return JsonResponse({'status': 'OK', 'followers': result})
        else:
            return JsonResponse({'status': 'error', 'error': 'followers - user not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'followers - request is not GET'})

def getUserFollowing(request, username):
    if request.method == "GET":
        limit = request.GET.get('limit', 50)
        if limit > 200 or limit < 0:
            limit = 50

        result = users.getFollowing(username, limit)
        if result is not None:
            return JsonResponse({'status': 'OK', 'following': result})
        else:
            return JsonResponse({'status': 'error', 'error': 'following - user not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'following - request is not GET'})