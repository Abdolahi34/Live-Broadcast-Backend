from django.urls import path
from Api import views

app_name = 'Api'
urlpatterns = [
    path('v1/programs/', views.ProgramApi.as_view(), name='programs'),
    path('v1/check-live/', views.check_live, name='check_live'),
    path('v1/create-programs-json/', views.create_programs_json, name='create_programs_json'),
    path('v1/menu/', views.MenuApi.as_view(), name='menu'),
    path('v1/create-menu-json/', views.create_menu_json, name='create_menu_json'),
    path('v1/every-10-sec/', views.every_10_second, name='every_10_second'),
]
