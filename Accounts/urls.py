from django.urls import path
from . import views


app_name = 'Accounts'
urlpatterns = [
    path('', views.user_view, name='profile'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('changepassword', views.change_pass, name='change_pass'),
]

