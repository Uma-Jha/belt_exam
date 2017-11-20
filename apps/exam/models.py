from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re
from datetime import date, datetime
from dateutil.parser import parse as parse_date

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = []
        try:
            user = self.get(email=postData['email'])
        except:
            user = None
        if user:
            errors.append("This email is already registered. Please use other")
        if len(postData['name']) < 2:
            errors.append("Name should be more than 1 character")
        if not postData['name'].isalpha():
            errors.append("Name should only contain characters")
        if len(postData['alias']) < 2:
            errors.append("Alias should be more than 1 character")
        if not postData['alias'].isalpha():
            errors.append("Alias should only contain characters")
        if len(postData['email']) < 1:
            errors.append("Email should not be blank")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email is not valid!")
        if len(postData['pwd']) < 8:
            errors.append("Password should be at least 8 characters")
        if len(postData['confirmPwd']) < 8 or postData['pwd']!=postData['confirmPwd']:
            errors.append("Password and Confirm Password should match")
        if len(postData['bday']) < 1:
            errors.append("Birthday cannot be blank")
        else:
            bday = parse_date(postData['bday'])
            age = int(str(date.today())[:4]) - int(str(bday)[:4])
            if age < 18:
                errors.append("Sorry, below 18 not allowed")
        if errors:
            return (False, errors)  
        else:
            hashPwd = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            user = self.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashPwd, bday=postData['bday'])
            return (True, user)

    def validate_login(self, postData):
        errors = []
        if len(postData['email'])==0 or len(postData['pwd'])==0:
            errors.append("Username or password cannot be blank")
            return(False, errors)
        try:
            user = self.get(email=postData['email'])
        except:
            user = None
        if user and bcrypt.hashpw(postData['pwd'].encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            return (True, user)
        errors.append("Invalid login. Email or password is incorrect")
        return(False, errors)

    def displayFriends(self, user_id):
        user = self.get(id=user_id)
        friends = user.friendships.all()
        if not friends:
            return (False, [])
        else:
            return (True, friends)

    def addFriend(self, user_id, friend_id):
        errors = []
        if int(friend_id) == int(user_id):
            errors.append("You cannot be friends with yourself")
        try:
            friend = self.get(id=friend_id)
        except:
            errors.append('Your friend is not in our database')
        try:
            user = self.get(id=user_id)
        except:
            errors.append('You must be logged in to be friends with others')
        if len(errors)==0:
            if user in friend.friendships.all():
                errors.append("")
                return (False, errors)
            else:
                friend.friendships.add(user)
                return (True, friend)
        return (False, errors)

    def removeFriend(self, user_id, friend_id):
        errors = []
        if int(friend_id) == int(user_id):
            errors.append("You cannot be friends with yourself")
        try:
            friend = self.get(id=friend_id)
        except:
            errors.append('Your friend is not in our database')
        try:
            user = self.get(id=user_id)
        except:
            errors.append('You must be logged in to be friends with others')
        if len(errors)==0:
            if user not in friend.friendships.all():
                errors.append("")
                return (False, errors)
            else:
                friend.friendships.remove(user)
                return (True, friend)
        return (False, errors)

    def viewFriend(self, friend_id, user_id):
        errors = []
        try:
            friend = self.get(id=friend_id)
            print "**************** {}".format(friend.name)
        except:
            errors.append('Your friend is not in our database')
        try:
            user = self.get(id=user_id)
            print "**************** {}".format(user.name)
        except:
            errors.append('You must be logged in to be friends with others')
        if len(errors)==0:  
            friend = self.get(id=friend_id) 
            return (True, friend) 
        else:
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    bday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friendships = models.ManyToManyField('self')
    objects = UserManager()