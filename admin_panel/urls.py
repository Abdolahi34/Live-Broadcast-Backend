from django.urls import path

from admin_panel import views

app_name = 'admin_panel'
urlpatterns = [
    path('', views.Admin, name='admin_panel'),
    path('api/program/', views.AdminProgram, name='admin_panel_program'),
    path('api/program/add/', views.AdminProgramAdd, name='admin_panel_program_add'),
    path('api/program/<int:num>/', views.AdminProgramView, name='admin_panel_program_view'),
    path('api/program/<int:num>/edit/', views.AdminProgramEdit, name='admin_panel_program_edit'),
    path('api/program/<int:num>/duplicate/', views.AdminProgramDuplicate, name='admin_panel_program_duplicate'),
]
