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
    path('dashboard/questions', views.dashboard_questions, name='dashboard_questions'),
    path('dashboard/questions/create', views.dashboard_questions_create, name='dashboard_questions_creaete'),
    path('dashboard/questions/delete/<int:id>/', views.dashboard_questions_delete, name='dashboard_questions_delete'),
    path('dashboard/questions/edit/<int:id>/', views.dashboard_questions_edit, name='dashboard_questions_edit'),
]

handler404 = 'app_poller.views.handler404'
handler500 = 'app_poller.views.handler500'
