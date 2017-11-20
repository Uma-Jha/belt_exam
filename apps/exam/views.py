from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
import bcrypt
from django.contrib import messages

def index(request):
    if 'userid' not in request.session:
        request.session['logged'] = False
    return render(request, 'exam/index.html')

def register(request):
        result = User.objects.validate_register(request.POST)
        if not result[0]:
            for m in result[1]:
                messages.warning(request, m)
            return redirect('/')
        else:
            request.session['userid'] = result[1].id
            request.session['name'] = result[1].name
            request.session['logged'] = True
            return redirect('/friends')

def login(request):
    result = User.objects.validate_login(request.POST)
    if not result[0]:
        for m in result[1]:
            messages.warning(request, m)
        return redirect('/')
    else:
        request.session['userid'] = result[1].id
        request.session['name'] = result[1].name
        request.session['logged'] = True
        return redirect('/friends')

def friends(request):
    result = User.objects.displayFriends(request.session['userid'])
    notFriends = User.objects.exclude(friendships=result).exclude(id=request.session['userid'])
    #context = {}
    '''if not result[0]:
        for m in result[1]:
            messages.warning(request, m)
            return redirect('/friends')
            return render(request, 'exam/dashboard.html', context)
        else:
            context = {
            'user': User.objects.get(id=request.session['userid']),
            'friends': result[1],
            'notFriends': notFriends
        }'''
    context = {
            'user': User.objects.get(id=request.session['userid']),
            'friends': result[1],
            'notFriends': notFriends
    }
    return render(request, 'exam/dashboard.html', context)

def viewUser(request, no):
    result = User.objects.viewFriend(no, request.session['userid'])
    print result[0], result[1]
    if not result[0]:
        for m in result[1]:
            messages.warning(request, m)
            return redirect('/friends')
    else:
        context = {
            'friend' : result[1]
            } 
        return render(request, 'exam/viewFriend.html', context)


def addFriend(request, no):
    result = User.objects.addFriend(request.session['userid'], no)
    if not result[0]:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/friends')

def removeFriend(request, no):
    result = User.objects.addFriend(request.session['userid'], no)
    if not result[0]:
        for m in result[1]:
            messages.warning(request, m)
    return redirect('/friends')

def logout(request):
    request.session.clear()
    return redirect("/")