from django.urls import path

from AdminPanel import views

app_name = 'AdminPanel'
urlpatterns = [
    path('', views.Admin, name='admin_panel'),
    path('programs/program/', views.AdminProgram, name='admin_panel_program'),
    path('programs/program/add/', views.AdminProgramAdd, name='admin_panel_program_add'),
    path('programs/program/<int:num>/', views.AdminProgramView, name='admin_panel_program_view'),
    path('programs/program/<int:num>/edit/', views.AdminProgramEdit, name='admin_panel_program_edit'),
    path('programs/program/<int:num>/duplicate/', views.AdminProgramDuplicate, name='admin_panel_program_duplicate'),
]
