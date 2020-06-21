from app_poller import views
from django.urls import path

app_name = 'app_poller'

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile', views.dashboard_profile, name='dashboard_profile'),
]
