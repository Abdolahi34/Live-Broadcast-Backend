from django.urls import path
from Programs import views

app_name = 'Programs-api'
urlpatterns = [
    path('v1/programs/', views.ProgramApi.as_view(), name='programs'),
    path('v1/check-live/', views.check_live, name='check_live'),
    path('v1/check-on-planning/', views.check_on_planning, name='check_on_planning'),
    path('v1/create-programs-json/', views.create_programs_json, name='create_programs_json'),
    path('v1/send-message-to-channel/', views.send_message_to_channel, name='send_message_to_channel'),
    path('v1/menu/', views.MenuApi.as_view(), name='menu'),
    path('v1/create-menu-json/', views.create_menu_json, name='create_menu_json'),
]
