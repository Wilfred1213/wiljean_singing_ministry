from django import forms
from .models import Other_peoples_music, Blog, Subscription,EventComment, Events, replyContact, blogComment
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm

class MusicForm(forms.ModelForm):
    class Meta:
        model = Other_peoples_music
        fields = ['title', 'artist', 'file', 'album', 'photo', 'location']

# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['title', 'content', 'image']


class BlogForm(TranslatableModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Translate form labels
        self.fields['title'].label = _('Title')
        self.fields['content'].label = _('Content')
        self.fields['image'].label = _('Image')

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'body', 'image', 'author', 'date', 'time', 'address']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class replyForm(forms.ModelForm):
    class Meta:
        model = replyContact
        fields = ['name', 'message']

class commentForm(forms.ModelForm):
    class Meta:
        model = blogComment
        fields = ['name', 'message']

class subtForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email',]

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['name', 'message']





