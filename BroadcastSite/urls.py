"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('superuser/', admin.site.urls, name='superuser'),
    path('', views.main, name='main'),
    path('profile/', include('Accounts.urls')),
    path('profile', views.profile_view_redirect),
    path('login/', views.login_redirect),
    path('login', views.login_redirect),
    path('signup/', views.signup_redirect),
    path('signup', views.signup_redirect),
    path('logout/', views.logout_redirect),
    path('logout', views.logout_redirect),
    path('changepassword/', views.change_pass_redirect),
    path('changepassword', views.change_pass_redirect),
    path('program/', include('Programs.urls')),
    path('program', views.program_redirect),
    path('api/', include('Api.urls')),
    path('access-denied', views.access_denied, name='access_denied'),
    path('<etc>', views.etc),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

