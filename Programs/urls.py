from django.urls import path
from . import views

app_name = 'Programs'
urlpatterns = [
    path('', views.programs, name='programs'),
    path('add', views.add_program, name='add_program'),
    path('<title_slug>/<stream_slug>', views.stream, name='stream'),
]

