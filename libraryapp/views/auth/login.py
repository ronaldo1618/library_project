from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import login

def login_user(request):
    template = 'login.html'
    return render(request, template)