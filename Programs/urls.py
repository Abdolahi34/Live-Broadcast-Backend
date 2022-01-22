from django.urls import path, include
from Programs import views

app_name = 'Programs'
urlpatterns = [
    path('add/', views.AddProgram.as_view, name='add_program'),
    path('api/', views.ProgramView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
