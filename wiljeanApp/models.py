from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# from parler.models import TranslatableModel, TranslatedFields
from parler.models import TranslatableModel, TranslatedFields
# Create your models here.

class Slider(models.Model):
    header = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    body = models.CharField(max_length =255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'slider'

class Quotes(models.Model):
    author = models.CharField(max_length =255)
    body = models.CharField(max_length =500)
    more_info = models.CharField(max_length =255, null = True)

    def __str__(self):
        return self.author
    class Meta:
        db_table = 'quote'
        

class Events(models.Model):
    title = models.CharField(max_length =255)
    body = models.TextField(max_length =1500)
    image = models.ImageField(upload_to='media', null = True)
    author = models.CharField(max_length =255, null = True)
    address = models.CharField(max_length =500, null = True)
    time = models.CharField(max_length =255, null = True)
    date = models.DateField(default =timezone.now)

    def __str__(self):
        return self.title

    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return None


    class Meta:
        db_table = 'events'


class ChooseUs(models.Model):
    title = models.CharField(max_length =255)
    body = models.CharField(max_length =1500)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'choose us'
class About(models.Model):
    title = models.CharField(max_length =255)
    body = models.TextField(max_length =10000)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.title

class Subscription(models.Model):
    email = models.EmailField(max_length = 255)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'subscription'

class Contact(models.Model):
    name = models.CharField(max_length =255)
    email = models.EmailField(max_length = 255)
    message =models.TextField(max_length =1000)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'contact'

class replyContact(models.Model):
    name = models.CharField(max_length =255)
    date = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message =models.TextField(max_length =1000)
    reply = models.BooleanField(default=False)


    def __str__(self):
        return self.name
    

class Album(models.Model):
    name =models.CharField(max_length = 255)
    tracks = models.IntegerField(default = 0)
    year_of_publish = models.DateField()
    cover = models.ImageField(upload_to='media', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'album'


class Music(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    file = models.FileField(upload_to='music_files')
    album = models.ForeignKey(Album, on_delete = models.CASCADE, null =True)
    publish_date = models.DateField()


    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'music'

class Blog(TranslatableModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    publish_date=models.DateTimeField(auto_now_add=True)
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=100),
        content=models.TextField(_('content'), max_length=10000),
        image=models.ImageField(_('image'), upload_to='music_files'),
        
    )

    def save_image_to_galary(self):
        Gallery.objects.create(photo = self.image)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'blog'
    
class Other_peoples_music(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    file = models.FileField(upload_to='music_files')
    album = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now = True)
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='image_file', null=True)

    def save_image_to_galary(self):
        Gallery.objects.create(photo = self.photo)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'other_music'

class Gallery(models.Model):
    photo = models.ImageField(upload_to='image_file')

    class Meta:
        ordering = ('-photo',)

class WiljeanGallery(models.Model):
    photo = models.ImageField(upload_to='image_file')

    class Meta:
        ordering = ('-photo',)

class blogComment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length=100, null = True, blank=True)
    message = models.TextField(max_length=100)
    blog =models.ForeignKey(Blog, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class EventComment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length=100, null = True, blank=True)
    message = models.TextField(max_length=100)
    event =models.ForeignKey(Events, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message