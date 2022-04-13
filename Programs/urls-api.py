from django.urls import path
from Programs import views

app_name = 'Programs-api'
urlpatterns = [
    path('programs/v1/', views.ProgramApi.as_view()),
    path('menu/v1/', views.MenuApi.as_view()),
]
