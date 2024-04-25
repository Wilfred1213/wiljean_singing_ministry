from django.urls import path
from authentication.views import signup, signin, signout

app_name = 'authentication'
urlpatterns = [
    path('signup/', signup, name= 'signup'),
    path('signin/', signin, name= 'signin'),
    path('signout/', signout, name= 'signout')

   
]
