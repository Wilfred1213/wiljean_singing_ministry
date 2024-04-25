from django.contrib import admin
from . models import ChooseUs, Blog, blogComment, EventComment, replyContact, WiljeanGallery, Gallery, Other_peoples_music, Slider,Events, Quotes, About, Album, Contact,Subscription,  Music
from parler.admin import TranslatableAdmin
# Register your models here.

admin.site.register(Slider)
admin.site.register(ChooseUs)
admin.site.register(Events)
admin.site.register(Quotes)
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(Subscription)
admin.site.register(Music)
admin.site.register(Album)
admin.site.register(Blog, TranslatableAdmin)
admin.site.register(Other_peoples_music)
admin.site.register(Gallery)
admin.site.register(WiljeanGallery)
admin.site.register(replyContact)
admin.site.register(blogComment)
admin.site.register(EventComment)