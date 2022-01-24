from django.urls import path
from Accounts import views

app_name = 'Accounts'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('changepassword/', views.ChangePass.as_view(), name='change_pass'),
]
