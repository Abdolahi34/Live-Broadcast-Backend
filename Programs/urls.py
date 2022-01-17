from django.urls import path
from . import views

app_name = 'Programs'
urlpatterns = [
    path('', views.program, name='program'),
    path('add/', views.add_program, name='add_program'),
    path('add', views.add_program2),
    # path('<slug>/', views.view_program, name='view_program'),
    path('<title_slug>/<stream_slug>', views.stream, name='stream'),
]

