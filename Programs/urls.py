from django.urls import path
from Programs import views

app_name = 'Programs'
urlpatterns = [
    path('add/', views.AddProgramView.as_view(), name='add_program'),
    path('delete/', views.DeleteProgramView.as_view(), name='delete_program'),
    path('delete/<slug>/', views.ProgramViewBeforeDelete.as_view(), name='view_program_before_delete'),
    path('streamtype/add/', views.AddStreamTypeView.as_view(), name='add_stream_type'),
    path('videocontent/add/', views.AddVideoContentView.as_view(), name='add_video_content'),
    path('videostat/add/', views.AddVideoStatView.as_view(), name='add_video_stat'),
    path('voicecontent/add/', views.AddVoiceContentView.as_view(), name='add_voice_content'),
    path('voicestat/add/', views.AddVoiceStatView.as_view(), name='add_voice_stat'),
    path('datetype/add/', views.AddDateTypeView.as_view(), name='add_date_type'),
    path('api/', views.ProgramApi.as_view()),
]
