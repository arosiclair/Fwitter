from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from json import loads
import time

from . import users, tweets, media
from fwitter_app.logger import log

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
        request.session['username'] = username
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error', 'error': 'login - failed'})

def logout(request):
    try:
        del request.session['userId']
        del request.session['username']
        # request.session['loggedOut'] = True
    except KeyError:
        pass
    return JsonResponse({ 'status': 'OK'})

def additem(request):
    try:
        userId = request.session['userId']
        username = request.session['username']
    except KeyError:
        return JsonResponse({'status': 'error', 'error': 'additem - user not logged in'})

    if request.method == "POST":
        content = loads(request.body)
        try:
            tweetContent = content['content']
            parent = content.get('parent', None)
            mediaIds = content.get('media', None)
        except KeyError:
            return JsonResponse({'status': 'error', 'error': 'additem - incorrect parameters'})
    else:
        return JsonResponse({'status': 'error', 'error': 'additem - request is not POST'})

    tweetId = tweets.add(userId, username, tweetContent, parent, mediaIds)
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

def likeitem(request, tweetId):
    username = request.session.get('username', None)
    if username is None:
        return JsonResponse({'status': 'error', 'error': 'likeitem - user not logged in'})

    if request.method == "POST":
        content = loads(request.body)
        like = content.get('like', True)

        if tweets.likeTweet(tweetId, like):
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'error', 'error': 'likeitem - tweet {0} not found'.format(tweetId)})
    else:
        return JsonResponse({'status': 'error', 'error': 'likeitem - request is not POST'})

def deleteitem(request, tweetId):
    userId = request.session.get("userId", None)
    if userId is None:
        return JsonResponse({'status': 'error', 'error': 'delete - user not logged in'})

    result = tweets.delete(userId, tweetId)
    if result:
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'error',
                             'error': 'delete - tweetId {0} from user {1} something went wrong'.format(tweetId, userId)})

def search(request):
    username = request.session.get('username', None)
    if username is None:
        return JsonResponse({'status': 'error', 'error': 'search - user not logged in'})

    if request.method == "POST":
        content = loads(request.body)
        log.debug("Search - " + str(content))
        timestamp = content.get('timestamp', int(time.time()))
        limit = content.get('limit', 25)
        if limit < 0 or limit > 100:
            limit = 25
        query = content.get('q', None)
        filterUsername = content.get('username', None)
        following = content.get('following', True)
        parentId = content.get('parent', None)
        replies = content.get('replies', True)
    else:
        return JsonResponse({'status': 'error', 'error': 'search - request is not POST'})

    tweetList = tweets.search(username, timestamp, limit, query, filterUsername, following, parentId, replies)
    log.debug("Search Result length: " + len(tweetList))
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

        result = users.follow(userId, username, follow)
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
            return JsonResponse({'status': 'OK', 'users': result})
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
            return JsonResponse({'status': 'OK', 'users': result})
        else:
            return JsonResponse({'status': 'error', 'error': 'following - user not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'following - request is not GET'})

def addmedia(request):
    if request.method == "POST":
        try:
            contents = request.FILES['content'].read()
        except:
            return JsonResponse({'status': 'error', 'error': 'addmedia - content key error'})

        mediaId = media.add(contents)
        if mediaId is not None:
            return JsonResponse({'status': 'OK', 'id': mediaId})
        else:
            return JsonResponse({'status': 'error', 'error': 'addmedia - insertion didn\'t work'})
    else:
        return JsonResponse({'status': 'error', 'error': 'addmedia - request is not POST'})

def getmedia(request, mediaId):
    if request.method == "GET":
        mediaBinary = media.get(mediaId)
        if mediaBinary is not None:
            return HttpResponse(mediaBinary, content_type='image/jpeg')
        else:
            return JsonResponse({'status': 'error', 'error': 'getmedia - mediaId: {0} not found'.format(mediaId)})
    else:
        return JsonResponse({'status': 'error', 'error': 'getmedia - request is not GET'})