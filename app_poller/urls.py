from app_poller import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'app_poller'

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),
    path('dashboard/questions/', views.dashboard_questions, name='dashboard_questions'),
    path('dashboard/questions/create/', views.dashboard_questions_create, name='dashboard_questions_creaete'),
    path('dashboard/questions/delete/<int:id>/', views.dashboard_questions_delete, name='dashboard_questions_delete'),
    path('dashboard/questions/edit/<int:id>/', views.dashboard_questions_edit, name='dashboard_questions_edit'),
    path('dashboard/polls/', views.dashboard_polls, name='dashboard_polls'),
    path('dashboard/polls/create/', views.dashboard_polls_create, name='dashboard_polls_create'),
    path('dashboard/polls/delete/<int:id>/', views.dashboard_polls_delete, name='dashboard_polls_delete'),
    path('dashboard/polls/edit/<int:id>/', views.dashboard_polls_edit, name='dashboard_polls_edit'),
    path('dashboard/tests/', views.dashboard_tests, name='dashboard_tests'),
    path('dashboard/tests/take/<int:id>/', views.dashboard_tests_take, name='dashboard_tests_take'),
    path('dashboard/answers/', views.dashboard_answers, name='dashboard_answers'),
    path('dashboard/answers/<int:id>/', views.dashboard_answers_id, name='dashboard_answers_id'),
    path('dashboard/answers/<int:id>/<int:userid>/', views.dashboard_answers_user, name='dashboard_answers_user'),
    path('dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('dashboard/users/<int:id>/', views.dashboard_users_edit, name='dashboard_users_edit'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    # path('reset_password/<str:link>/', views.reset_password_link, name='reset_password_link'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app_poller.views.handler404'
handler500 = 'app_poller.views.handler500'
