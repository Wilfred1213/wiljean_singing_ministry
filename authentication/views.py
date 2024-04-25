from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from wiljeanApp.search import newsletter
from wiljeanApp.models import Album, Other_peoples_music

# Create your views here.
def signup(request):
    album = Album.objects.all()
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:2]
    newsletter(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:

            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username already exist')
                return redirect('authentication:signup')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email already exist')
                return redirect('authentication:signup')
            user_data = User(username = username, email =email, password = password)
            user_data.save()
            messages.info(request, 'Signup successfull. Sign in')
            return redirect('authentication:signin')
        else:
             messages.info(request, 'Password not match')
             return redirect('authentication:signup')
    return render(request, 'authentication/signup.html', {'albums':album, 'latests':latest_music})
        

def signin(request):
    album = Album.objects.all()
    
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:2]
    # user = request.user
    newsletter(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Loggin successfull')
            return redirect('index')
        messages.info(request, 'Invalid Credential')
        return redirect('authentication:signin')
    return render(request, 'authentication/login.html', {'albums':album, 'latests':latest_music})

def signout(request):
    logout(request)
    messages.info(request, 'You logged out. Login again')
    return redirect('authentication:signin')
        



