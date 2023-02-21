from django.shortcuts import render
from .models import Client


# Create your views here.
def list():
    clients = Client.objects.all()
