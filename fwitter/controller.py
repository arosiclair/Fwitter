from django.shortcuts import render, redirect
from django.http import JsonResponse

from json import loads

from . import users

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