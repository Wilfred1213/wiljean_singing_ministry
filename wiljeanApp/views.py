from django.shortcuts import render, redirect, get_object_or_404
from . models import Slider,Quotes, Events, Blog, EventComment, blogComment, replyContact, WiljeanGallery, Gallery, Other_peoples_music, Blog, Album, ChooseUs, About, Subscription, Contact, Music
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from wiljeanApp.search import search_music, newsletter
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
import os
from . forms import MusicForm, EventCommentForm, BlogForm, EventForm, replyForm, commentForm
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize, deserialize
from django.utils.translation import activate

# Create your views here.

def unsubscribe(request, news_id):
    del_news = Subscription.objects.get(id = news_id)
    if del_news:
        del_news.delete()
        messages.info(request, 'You unsubcribe from our newsletter. If this is a mistake feel free to subscribe again')
        return redirect('index')

def index(request):
    slide = Slider.objects.all()
    quotes =Quotes.objects.all()
    event = Events.objects.all()
    choose = ChooseUs.objects.all()
    
    newsletter(request)
    
    context = {
        'slider':slide,
        'quotes':quotes,
        'events':event,
        'chooseus':choose
    }
    return render(request, 'wiljeanApp/index.html', context)

@login_required(login_url='authentication:signin')
def add_event(request):
    
    album = Album.objects.all()
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:5]
    form = EventForm(request.POST, request.FILES)
    
    if request.method =='POST':
        
        if form.is_valid():
            form.save()
            messages.info(request, 'Event added successfully')
            
            return JsonResponse({
                'success':True, 
                'message':'Event added successful'
                })
        
    newsletter(request)
    context = {
        'form':form,
        'albums':album,
        'latests':latest_music
    }
    
    return render(request, 'wiljeanApp/event_form.html', context)


def delete_event(request, event_id):
    event = Events.objects.get(id = event_id)
    if event.date < timezone.now().date():
        # If the event date has passed, delete the event
        event.delete()
        messages.info(request, 'This event has expired and has been deleted.')
        return redirect('index')
    return redirect(reverse('event_detail', args=[event_id]))


def event_detail(request, event_id):
    user= request.user
    event = Events.objects.get(id = event_id)
    
    if request.method =='POST':
        form = EventCommentForm(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                save_form =form.save(commit = False)
                save_form.user = request.user
                save_form.event = event
                save_form.save()


                return JsonResponse({
                    'success':True,
                    'message':'You commented on this Event',
                    
                })
            
            save_form =form.save(commit = False)   
            save_form.event = event
            save_form.save()
            
            return JsonResponse({
                    'success':True,
                    'message':'You commented on this Event',
                    
                })

        
    newsletter(request)
    form = EventCommentForm()
    context= {
        'events':event,
        'form':form
    }
    return render(request, 'wiljeanApp/event_detail.html', context)

def fetch_event_comments(request, event_id):
    event = Events.objects.get(id=event_id)
    comments = EventComment.objects.filter(event=event).order_by('-date')[:8]

    serialize_comment = serialize('json', comments)
    deserialized_comments = list(deserialize('json', serialize_comment))
    
    comments_data = []
    
    # Iterate through each comment and add required fields to the list
    for deserialized_obj in deserialized_comments:
        comment = deserialized_obj.object
        user = comment.user.username if comment.user else comment.name
        
        comment_data = {
            'user': user,
            'text': comment.message,
            'date': comment.date.strftime('%Y-%m-%d')
        }
        comments_data.append(comment_data)

        print('this is the user printed', comments_data)
        print('User:', comment_data['user'])
    
    # Return the list of comments data as JSON response
    return JsonResponse({'comments': comments_data})

def about(request):
    abouts = About.objects.all()
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:8]

    album= Album.objects.all()

    newsletter(request)
    
    context = {
        'abouts':abouts,
        'albums':album,
        'latests':latest_music
    }
    return render(request, 'wiljeanApp/about.html', context)

def gallery(request):
    all_gallery = Gallery.objects.all()
    wil_gallery = WiljeanGallery.objects.all()
    newsletter(request)

    context = {
        'galleries':all_gallery,
        'wiljean': wil_gallery
    }
    
    return render(request, 'wiljeanApp/gallery.html', context)

def download(request):
    musics = Music.objects.all()
    other_music = Other_peoples_music.objects.all()
    # search = None
    searches = search_music(request)

    newsletter(request)
    context = {
        'musics': musics,
        'other_musics': other_music,
        'searches': searches,
    }
    return render(request, 'wiljeanApp/download.html', context)


def blog(request):
    # activate('ha')
    album = Album.objects.all()
    blog_list = Blog.objects.all().order_by('-publish_date')

    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:8]

    paginator = Paginator(blog_list, 2)  # Show 5 blog posts per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

     # Get user's language preference from session or user profile
    user_language = request.session.get('user_language', 'en')  # Default to English if not set

    # Activate user's language
    # activate(user_language)

    newsletter(request)

    context = {
        'albums': album,
        'blogs': blogs,
        'latests':latest_music
    }
    request.session['last_visited_page'] = request.path
    return render(request, 'wiljeanApp/blog.html', context)


def set_language(request):
    if 'lang' in request.GET:
        language = request.GET['lang']
        request.session['user_language'] = language
        activate(language)
    # Redirect back to the referring page or a specific page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='authentication:signin')
def delete_blog(request, blog_id):
    user = request.user
    if user.is_authenticated and user.is_staff:
        blog = Blog.objects.get(id = blog_id)
        blog.delete()
        messages.info(request, 'Blog deleted!')
        return redirect('blog')
    messages.info(request, 'You are not permitted to delete this blog')
    return redirect('blog')
       
    
def delete_blog_confirmation(request, blog_id):
    return render(request, 'wiljeanApp/blog_confirmation.html', {'blog_id':blog_id })
  

    
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return str(obj)  # Use the string representation of the user
        return super().default(obj)

def blog_detail(request, blog_id):
    user = request.user
    album = Album.objects.all()
    blog = Blog.objects.get(id=blog_id)
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:8]
    comment = blogComment.objects.filter(blog=blog).order_by('-date')[:8]

    if request.method =='POST':
        form = commentForm(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                save_form =form.save(commit = False)
                save_form.user = request.user
                save_form.blog = blog
                save_form.save()


                return JsonResponse({
                    'success':True,
                    'message':'You commented on this post',
                    
                })
            
            save_form =form.save(commit = False)   
            save_form.blog = blog
            save_form.save()
            
            return JsonResponse({
                    'success':True,
                    'message':'You commented on this post',
                    
                })

    # Set the session variable
    request.session['last_visited_page'] = request.path

    print("Session Data:", dict(request.session))

    newsletter(request)

    form = commentForm()

    context = {
        'blogs': blog,
        'albums': album,
        'latests':latest_music,
        'form':form,
        
    }

    return render(request, 'wiljeanApp/blog_detail.html', context)



def fetch_comments(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = blogComment.objects.filter(blog=blog).order_by('-date')[:8]

    serialize_comment = serialize('json', comments)
    deserialized_comments = list(deserialize('json', serialize_comment))
    
    comments_data = []
    
    # Iterate through each comment and add required fields to the list
    for deserialized_obj in deserialized_comments:
        comment = deserialized_obj.object
        user = comment.user.username if comment.user else comment.name
        
        comment_data = {
            'user': user,
            'text': comment.message,
            'date': comment.date.strftime('%Y-%m-%d')
        }
        comments_data.append(comment_data)

        print('this is the user printed', comments_data)
        print('User:', comment_data['user'])
    
    # Return the list of comments data as JSON response
    return JsonResponse({'comments': comments_data})



def all_comment(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comment = blogComment.objects.filter(blog=blog).order_by('-date')

    context = {
        'comments':comment
    }
    return render(request, 'wiljeanApp/all_comment.html', context)

def other_music_detail(request, other_id):
    music_id = Other_peoples_music.objects.get(id=other_id)

    newsletter(request)
    context = {
        'music': music_id,
        
    }
    return render(request, 'wiljeanApp/other_music_detail.html', context)


def contact(request):
    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        # website = request.POST.get('website')
        message = request.POST.get('message')

        if Contact.objects.filter(email = email, message=message).exists():

            return JsonResponse({
                'success': False,
                'message': 'You are sending this message for the second time'
                
                
            })
            
        Contact.objects.create(name=name, email = email, message=message)
        messages.info(request, 'Thanks for mailing us. We will get back to you')
        # return redirect('index')
        return JsonResponse({
                'success': True,
                'message': 'Created successfully.'
                
            })


    newsletter(request)
    
    return render(request, 'wiljeanApp/contact.html', {})
  
def download_music(request, music_id):
    
    music = get_object_or_404(Music, pk=music_id)
    
    file_path = music.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{music.title}--{music.artist}.mp3"'
        return response
    
def download_other_music(request, music_id):
    try:
        music = Other_peoples_music.objects.get(pk=music_id)
        print(f'this is the location {music.file.path}')
        file_path = music.file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{music.title}--{music.artist}.mp3"'
            return response
    except Other_peoples_music.DoesNotExist:
        raise Http404("Music file not found")
    

def play_mp3(request, music_id, other_music_id ):
    
    context={
        'music_id': music_id,
        'other_music_id': other_music_id,

    }

    return render(request, 'wiljeanApp/audio.html', context)

def stream_audio(request, music_id):
    
    music = get_object_or_404(Music, pk=music_id)
    filepath = os.path.join(settings.MEDIA_ROOT, str(music.file))

    def generate_audio():
        with open(filepath, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(1024)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(generate_audio(), content_type='audio/mpeg')
    return response

def stream_other_audio(request, music_id):
    
    music = get_object_or_404(Other_peoples_music, pk=music_id)
    filepath = os.path.join(settings.MEDIA_ROOT, str(music.file))

    def generate_audio():
        with open(filepath, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(1024)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(generate_audio(), content_type='audio/mpeg')
    return response

@login_required(login_url='authentication:signin')
def upload(request):
    user = request.user
    gallery = Gallery.objects.all()
    wil = WiljeanGallery.objects.all()

    album = Album.objects.all()
    
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:1]


    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            save_music = form.save(commit=False)
            save_music.user = user

            title = form.cleaned_data['title']
            music_file = form.cleaned_data['file']
            
            if Other_peoples_music.objects.filter(user=user, title=title, file=music_file).exists():
                messages.info(request, 'Sorry this music already exist!')
                return JsonResponse({
                    'success':False, 
                    'message':'Sorry, this music already exist'
                    })

            else:
                save_music.save()
                save_music.save_image_to_galary()
            # Gallery.objects.create(photo = save_music.photo)
            messages.info(request, 'You successfully upload one mp3!')            
            return JsonResponse({
                'success':True, 
                'message':'You successfully upload one mp3'
                })

            # messages.success(request, 'You successfully uploaded one MP3')
            # return redirect('upload')
    else:
        form = MusicForm()
    
    newsletter(request)
    context = {
        
        'form': form,
        'galleries':gallery,
        'wiljean':wil,
        'albums':album,
        'latests':latest_music
            
        }
    return render(request, 'wiljeanApp/upload.html', context)

def music_details(request, music_id):
    album = Album.objects.all()
    
    latest_music = Other_peoples_music.objects.all().order_by('-publish_date')[:5]

    other_music = Other_peoples_music.objects.all().order_by("-publish_date")[:10]
    album_id = Album.objects.get(id = music_id)

    get_musics_album = album_id.music_set.all()

    # get_musics_album = Music.objects.filter(album = album_id)
    newsletter(request)

    context={
        'album':album_id,
        'musics':get_musics_album,
        'other_musics':other_music,
        'albums':album,
        'latests':latest_music
    }
    return render(request, 'wiljeanApp/album1.html', context)

def all_music(request):
    other_music_list = Other_peoples_music.objects.all()

    searches = search_music(request)

    # Number of items per page
    items_per_page = 10

    paginator = Paginator(other_music_list, items_per_page)
    page_number = request.GET.get('page')

    try:
        other_music = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        other_music = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        other_music = paginator.page(paginator.num_pages)

    newsletter(request)
    context = {
        'other_musics': other_music,
        'searches': searches,
        
    }
    return render(request, 'wiljeanApp/all_music.html', context)

@login_required(login_url='authentication:signin')
def edit_music(request, music_id):
    music = Other_peoples_music.objects.get(id = music_id)
    if request.method =='POST':
        form = MusicForm(request.POST, request.FILES, instance=music)

        if form.is_valid():
            form.save()

        #    Gallery.objects.create(photo = save_photo.photo)

            messages.info(request, 'Edited Successfull')
            # return redirect('download')
            return JsonResponse({
                'success':True, 'message':'Editted Successfully!'
            })
        return JsonResponse({
                'success':False, 'message':'Fail!'
            })
    form = MusicForm(instance=music)

    newsletter(request)
    context = {
        'form':form
    }
    return render(request, 'wiljeanApp/edit.html', context)

def confirmation(request, other_music_id, wil_id):
    
    return render(request, 'wiljeanApp/confirmation.html', {'other_music_id':other_music_id, 'wil_id':wil_id })

@login_required(login_url='authentication:signin')
def delete(request, other_music_id, wil_id):
    user = request.user
    
    try:
        delete_wiljean = Music.objects.get(id=wil_id)
    except Music.DoesNotExist:
        delete_wiljean = None

    try:
        delete_other_music = Other_peoples_music.objects.get(id=other_music_id)
    except Other_peoples_music.DoesNotExist:
        delete_other_music = None

    if delete_other_music is not None and user == delete_other_music.user or user.is_staff:
        delete_other_music.delete()
        messages.success(request, 'The music has been deleted successfully.')
        return redirect('all_music')
    elif delete_wiljean is not None and user.is_staff:
        delete_wiljean.delete()
        messages.success(request, 'The music has been deleted successfully.')
        return redirect('all_music')
    else:
        messages.error(request, 'You are not authorized to delete this music.')
        return redirect('all_music')

@login_required(login_url='authentication:signin')
def blog_upload(request):
    blog = Blog.objects.all()
    user = request.user
    if request.method =='POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            save_wiljean = form.save(commit=False)
            save_wiljean.user = user
        
            save_wiljean.save()
            save_wiljean.save_image_to_galary()

            messages.info(request, 'Saved successfull')
            return redirect('blog_upload')
        messages.info(request, 'Error saving your form')
        return redirect('blog_upload')
    
    form = BlogForm()
    context = {
        'form':form
    }
    return render(request, 'wiljeanApp/blogform.html', context)

@login_required(login_url='authentication:signin')
def all_contacts(request):
    contacts = Contact.objects.all().order_by('-date')
    
    replymessage = []
    replied_contacts = []
    for contact in contacts:
        replied_contacts.append(contact)
        if replyContact.objects.filter(contact=contact, reply=True).exists():
            msg = replyContact.objects.filter(contact=contact, reply=True).order_by('-date')
            replymessage.append(list(msg))
        else:
            replymessage.append([])
        
    zipped_data = zip(replied_contacts, replymessage)
    
    context = {
        'zipped_data':zipped_data,
        'contacts':contacts,
        'reply':replied_contacts,

        'replymessage':replymessage
    }
    return render(request, 'wiljeanApp/all_contact.html', context)

@login_required(login_url='authentication:signin') 
def reply(request, contact_id):
    contact = Contact.objects.get(id = contact_id)

    replied = replyContact.objects.filter(contact = contact)

    if request.method =='POST':
        form = replyForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit = False)
            save_form.contact =contact
            save_form.reply = True
            save_form.save()
            messages.info(request, f'You replied {contact.name}')
            return redirect('reply', contact_id)
    form = replyForm()
    context = {
        'form':form,
        'contacts':contact,
        'replies':replied,


    }
    return render(request, 'wiljeanApp/reply_contact.html', context)




