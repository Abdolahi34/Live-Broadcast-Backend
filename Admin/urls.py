from django.urls import path

from Admin import views

app_name = 'Admin'
urlpatterns = [
    path('', views.Admin, name='admin'),
    path('programs/program/', views.AdminProgram, name='program'),
    path('programs/program/add/', views.AdminProgramAdd, name='program_add'),
    path('programs/program/<int:num>', views.AdminProgramView, name='program_view'),
    path('programs/program/edit/<int:num>', views.AdminProgramEdit, name='program_edit'),
    path('programs/datetype/', views.AdminDateType, name='datetype'),
    path('programs/datetype/add/', views.AdminDateTypeAdd, name='datetype_add'),
    path('programs/datetype/<int:num>', views.AdminDateTypeView, name='datetype_view'),
    path('programs/datetype/edit/<int:num>', views.AdminDateTypeEdit, name='datetype_edit'),
    path('programs/streamtype/', views.AdminStreamType, name='streamtype'),
    path('programs/streamtype/add/', views.AdminStreamTypeAdd, name='streamtype_add'),
    path('programs/streamtype/<int:num>', views.AdminStreamTypeView, name='streamtype_view'),
    path('programs/streamtype/edit/<int:num>', views.AdminStreamTypeEdit, name='streamtype_edit'),
    path('programs/videocontent/', views.AdminVideoContent, name='videocontent'),
    path('programs/videocontent/add/', views.AdminVideoContentAdd, name='videocontent_add'),
    path('programs/videocontent/<int:num>', views.AdminVideoContentView, name='videocontent_view'),
    path('programs/videocontent/edit/<int:num>', views.AdminVideoContentEdit, name='videocontent_edit'),
    path('programs/videostat/', views.AdminVideoStat, name='videostat'),
    path('programs/videostat/add/', views.AdminVideoStatAdd, name='videostat_add'),
    path('programs/videostat/<int:num>', views.AdminVideoStatView, name='videostat_view'),
    path('programs/videostat/edit/<int:num>', views.AdminVideoStatEdit, name='videostat_edit'),
    path('programs/voicecontent/', views.AdminVoiceContent, name='voicecontent'),
    path('programs/voicecontent/add/', views.AdminVoiceContentAdd, name='voicecontent_add'),
    path('programs/voicecontent/<int:num>', views.AdminVoiceContentView, name='voicecontent_view'),
    path('programs/voicecontent/edit/<int:num>', views.AdminVoiceContentEdit, name='voicecontent_edit'),
    path('programs/voicestat/', views.AdminVoiceStat, name='voicestat'),
    path('programs/voicestat/add/', views.AdminVoiceStatAdd, name='voicestat_add'),
    path('programs/voicestat/<int:num>', views.AdminVoiceStatView, name='voicestat_view'),
    path('programs/voicestat/edit/<int:num>', views.AdminVoiceStatEdit, name='voicestat_edit'),
]
