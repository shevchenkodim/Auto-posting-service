from django.urls import path
from . import views

urlpatterns = [
    path('',            views.studio,         name="studio"),
    path('tasks/',      views.tasks,          name="tasks"),
    path('tasks/create',views.taskcreate,     name="taskcreate"),
    path('tasks/create/new',views.taskcreatenew,  name="taskcreatenew"),
    path('tasks/delete',views.taskdelete,     name="taskdelete"),
    path('statistics/', views.statistics,     name="statistics"),
    path('settings/',   views.settings,       name="settings"),
    path('settings/create/telegram', views.settingscreatetelegram, name="settingscreatetelegram"),
    path('settings/create/facebbok', views.settingscreatefacebook, name="settingscreatefacebook"),
]
