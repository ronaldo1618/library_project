from django.shortcuts import render

def home(request):
    if request.method == 'GET':
        template = 'home.html'

        return render(request, template)