from django.urls import path

from AdminPanel import views

app_name = 'AdminPanel'
urlpatterns = [
    path('', views.Admin, name='admin_panel'),
    path('Api/program/', views.AdminProgram, name='admin_panel_program'),
    path('Api/program/add/', views.AdminProgramAdd, name='admin_panel_program_add'),
    path('Api/program/<int:num>/', views.AdminProgramView, name='admin_panel_program_view'),
    path('Api/program/<int:num>/edit/', views.AdminProgramEdit, name='admin_panel_program_edit'),
    path('Api/program/<int:num>/duplicate/', views.AdminProgramDuplicate, name='admin_panel_program_duplicate'),
]
