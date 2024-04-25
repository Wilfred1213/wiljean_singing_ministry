"""
URL configuration for wiljean_singing_ministry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('wiljeanApp/', include('wiljeanApp.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,  PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('wiljeanApp.urls')),
    path('rosetta/', include('rosetta.urls')),


    path('authentication/', include('authentication.urls')),
    path('cookie-consent/', include('cookie_consent.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # change password
    path('change-password/', PasswordChangeView.as_view(
        template_name ='wiljeanApp/auth/change-password.html'),   
        name='change-password'),
    path('change_password_done/', PasswordChangeDoneView.as_view(
        template_name ='wiljeanApp/auth/password_change_done.html'),   
        name='password_change_done'),

    #forget password
    path('password_reset/', PasswordResetView.as_view(template_name ='wiljeanApp/auth/password_reset.html'), 
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name ='wiljeanApp/auth/password_reset_done.html'), 
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name ='wiljeanApp/auth/password_reset_form.html', 
        ), 
        name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name ='wiljeanApp/auth/password_reset_complete.html'),
        name='password_reset_complete'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)