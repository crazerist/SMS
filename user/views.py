from django.shortcuts import render

def home(request):
    return render(request, "user/login_home.html")
