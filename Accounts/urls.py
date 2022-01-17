from django.urls import path
from . import views


app_name = 'Accounts'
urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path('signup', views.signup_view2),
    path('login/', views.login_view, name='login'),
    path('login', views.login_view2),
    path('logout/', views.logout_view, name='logout'),
    path('logout', views.logout_view2),
    path('changepassword/', views.change_pass, name='change_pass'),
    path('changepassword', views.change_pass2),
]

