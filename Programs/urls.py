from django.urls import path
from Programs import views

app_name = 'Programs'
urlpatterns = [
    path('api/', views.ProgramApi.as_view()),
]
