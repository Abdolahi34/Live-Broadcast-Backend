from django.urls import path
from Programs import views

app_name = 'Programs-api'
urlpatterns = [
    path('v1/create-programs-json/', views.create_programs_json, name='create_programs_json'),
    path('v1/create-menu-json/', views.create_menu_json, name='create_menu_json'),
    path('v1/programs/', views.ProgramApi.as_view(), name='programs'),
    path('v1/menu/', views.MenuApi.as_view(), name='menu'),
]
