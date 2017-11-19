from django.shortcuts import render
from django.http import HttpResponse
import cgi
import os
import subprocess

def index(request):
    return HttpResponse("Welcome to GetClicked.GOP!")

def testpost(request):
    try:
        text = "This is what the server got as part of the POST:\n" + cgi.escape(str(request.POST))
    except:
        text = "Something went wrong, so this is just static text."
    return HttpResponse(text)

def deploy(request):
    text = subprocess.check_output('touch /home/bitnami/public/DEPLOY', stderr=subprocess.STDOUT, shell=True)
    return HttpResponse(text)
