from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout

def home(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')
