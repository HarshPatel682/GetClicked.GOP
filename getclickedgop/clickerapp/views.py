from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to GetClicked.GOP!")

def testpost(request):
    text = "This is what the server got as part of the POST:\n" + str(request.POST)
    return HttpResponse(text)
