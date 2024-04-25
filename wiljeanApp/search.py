from wiljeanApp.models import Music, Other_peoples_music, Subscription
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse

def search_music(request):
    musics = Music.objects.all()
    other_music = Other_peoples_music.objects.all()
    if 'query' in request.GET:
        query = request.GET.get('query')
        music_query = Q(title__icontains=query) | Q(artist__icontains=query)
        musics_search = musics.filter(music_query)
        other_music_query = Q(title__icontains=query) | Q(artist__icontains=query)
        other_music_search = other_music.filter(other_music_query)
        search = list(musics_search) + list(other_music_search)

        return search
    
def newsletter(request):
    next_url = request.POST.get('next', '/')
    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST.get('email')
        if Subscription.objects.filter(email = email).exists():
            messages.info(request, f'Someone has already subscribe with this email {email}')
            return redirect(next_url)
            
        Subscription.objects.create(email = email)
        messages.info(request, 'Thank you for subscribing to our newsletter')
        return redirect(next_url)
        
    