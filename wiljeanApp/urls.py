from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,  PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('download/', views.download, name='download'),
    path('blog/', views.blog, name='blog'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('fetch_comments/<int:blog_id>/', views.fetch_comments, name='fetch_comments'),
    path('all_comment/<int:blog_id>/', views.all_comment, name='all_comment'),
    path('contact/', views.contact, name='contact'),
    path('download_music/<int:music_id>/', views.download_music, name='download_music'),
    path('download_other_music/<int:music_id>/', views.download_other_music, name='download_other_music'),
    path('play_mp3/<int:music_id>/<int:other_music_id>', views.play_mp3, name='play_mp3'),
    path('stream_audio/<int:music_id>/', views.stream_audio, name='stream_audio'),
    path('stream_other_audio/<int:music_id>/', views.stream_other_audio, name='stream_other_audio'),
    path('upload/', views.upload, name='upload'),
    path('music_details/<int:music_id>/', views.music_details, name='music_details'),
    path('all_music/', views.all_music, name='all_music'),
    path('blog_upload/', views.blog_upload, name='blog_upload'),
    path('edit_music/<int:music_id>/', views.edit_music, name='edit_music'),
    path('confirmation/<int:other_music_id>/<int:wil_id>/', views.confirmation, name='confirmation'),
    path('delete/<int:other_music_id>/<int:wil_id>/', views.delete, name='delete'),
    path('add_event/', views.add_event, name='add_event'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('fetch_event_comments/<int:event_id>/', views.fetch_event_comments, name='fetch_event_comments'),
    
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('other_music_detail/<int:other_id>/', views.other_music_detail, name='other_music_detail'),
    path('all_contacts/', views.all_contacts, name='all_contacts'),
    path('reply/<int:contact_id>/', views.reply, name='reply'),
    path('unsubscribe/<int:news_id>/', views.unsubscribe, name='unsubscribe'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('delete_blog_confirmation/<int:blog_id>/', views.delete_blog_confirmation, name='delete_blog_confirmation'),
    path('set_language/', views.set_language, name='set_language'),

   
]
