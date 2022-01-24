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

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('profile/', include('Accounts.urls')),
    path('login/', RedirectView.as_view(pattern_name='Accounts:login')),
    path('signup/', RedirectView.as_view(pattern_name='Accounts:signup')),
    path('logout/', RedirectView.as_view(pattern_name='Accounts:logout')),
    path('changepassword/', RedirectView.as_view(pattern_name='Accounts:change_pass')),
    path('programs/', include('Programs.urls')),
]

handler403 = 'BroadcastSite.views.status_code_403_forbidden'
handler404 = 'BroadcastSite.views.status_code_404_not_found'
handler500 = 'BroadcastSite.views.status_code_500_internal_server_error'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
