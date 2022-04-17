from django.urls import path
from Programs import views

app_name = 'Programs-api'
urlpatterns = [
    path('v1/programs/', views.ProgramApi.as_view()),
    path('v1/menu/', views.MenuApi.as_view()),
]