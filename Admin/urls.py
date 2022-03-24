from django.urls import path

from Admin import views

app_name = 'Admin'
urlpatterns = [
    path('', views.Admin.as_view(), name='admin'),
    path('programs/program/', views.AdminProgram.as_view(), name='program'),
    path('programs/program/<int:num>', views.AdminProgramView.as_view(), name='program_view'),
    path('programs/program/edit/<int:num>', views.AdminProgramEdit.as_view(), name='program_edit'),
    path('programs/datetype/', views.AdminDateType.as_view(), name='datetype'),
    path('programs/datetype/<int:num>', views.AdminDateTypeView.as_view(), name='datetype_view'),
    path('programs/datetype/edit/<int:num>', views.AdminDateTypeEdit.as_view(), name='datetype_edit'),
    path('programs/streamtype/', views.AdminStreamType.as_view(), name='streamtype'),
    path('programs/streamtype/<int:num>', views.AdminStreamTypeView.as_view(), name='streamtype_view'),
    path('programs/streamtype/edit/<int:num>', views.AdminStreamTypeEdit.as_view(), name='streamtype_edit'),
    path('programs/videocontent/', views.AdminVideoContent.as_view(), name='videocontent'),
    path('programs/videocontent/<int:num>', views.AdminVideoContentView.as_view(), name='videocontent_view'),
    path('programs/videocontent/edit/<int:num>', views.AdminVideoContentEdit.as_view(), name='videocontent_edit'),
    path('programs/videostat/', views.AdminVideoStat.as_view(), name='videostat'),
    path('programs/videostat/<int:num>', views.AdminVideoStatView.as_view(), name='videostat_view'),
    path('programs/videostat/edit/<int:num>', views.AdminVideoStatEdit.as_view(), name='videostat_edit'),
    path('programs/voicecontent/', views.AdminVoiceContent.as_view(), name='voicecontent'),
    path('programs/voicecontent/<int:num>', views.AdminVoiceContentView.as_view(), name='voicecontent_view'),
    path('programs/voicecontent/edit/<int:num>', views.AdminVoiceContentEdit.as_view(), name='voicecontent_edit'),
    path('programs/voicestat/', views.AdminVoiceStat.as_view(), name='voicestat'),
    path('programs/voicestat/<int:num>', views.AdminVoiceStatView.as_view(), name='voicestat_view'),
    path('programs/voicestat/edit/<int:num>', views.AdminVoiceStatEdit.as_view(), name='voicestat_edit'),
]