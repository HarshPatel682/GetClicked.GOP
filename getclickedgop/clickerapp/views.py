from django.shortcuts import render
from django.http import HttpResponse
import cgi
import os
import subprocess
import json
from django.contrib.auth import authenticate, login, logout
from models import *

def index(request):
    return HttpResponse("Welcome to GetClicked.GOP!")

def testpost(request):
    try:
        text = "This is what the server got as part of the POST:\n" + cgi.escape(str(request.POST))
    except:
        text = "Something went wrong, so this is just static text."
    return HttpResponse(text)

def deploy(request):
    #text = subprocess.check_output('touch /home/bitnami/public/DEPLOY', stderr=subprocess.STDOUT, shell=True)
    text = subprocess.check_output('w', stderr=subprocess.STDOUT, shell=True)
    return HttpResponse(text)

def createuser(request):
    result = {}
    if "username" not in request.POST:
        result["success"] = False
        result["comment"] = "A username was not supplied."
        return HttpResponse(json.dumps(result))
    elif "password" not in request.POST:
        result["success"] = False
        result["comment"] = "A password was not supplied."
        return HttpResponse(json.dumps(result))
    username = request.POST["username"]
    password = request.POST["password"]
    if len(User.objects.filter(username=username)) != 0:
        result["success"] = False
        result["comment"] = "That username is already taken."
        return HttpResponse(json.dumps(result))
    User.objects.create_user(username, None, password)
    result["success"] = True
    result["comment"] = "A new user was successfully created."
    return HttpResponse(json.dumps(result))

def loginuser(request):
    result = {}
    if "username" not in request.POST:
        result["success"] = False
        result["comment"] = "A username was not supplied."
        return HttpResponse(json.dumps(result))
    elif "password" not in request.POST:
        result["success"] = False
        result["comment"] = "A password was not supplied."
        return HttpResponse(json.dumps(result))
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is None:
        result["success"] = False
        result["comment"] = "The username and password combination was not recognized."
        return HttpResponse(json.dumps(result))
    else:
        result["success"] = True
        result["comment"] = "The user has been logged in successfully."
        login(request, user)
        return HttpResponse(json.dumps(result))

def logoutuser(request):
    result = {}
    logout(request)
    result["success"] = True
    return HttpResponse(json.dumps(result))
