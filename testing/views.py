from django.shortcuts import render,HttpResponse

# Create your views here.
def home():
    return HttpResponse("This content is sent from the server.")