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

urlpatterns = [
    path('api/', include('Programs.urls-api')),
    path('admin/', include('AdminPanel.urls')),
    path('admin2/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler403 = 'RadioRahh.views.status_code_403_forbidden'
handler404 = 'RadioRahh.views.status_code_404_not_found'
handler500 = 'RadioRahh.views.status_code_500_internal_server_error'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'پیشخوان مدیریت سایت راه'
admin.site.site_title = 'پیشخوان مدیریت سایت راه'
admin.site.index_title = 'پیشخوان مدیریت'
