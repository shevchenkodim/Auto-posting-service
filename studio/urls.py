from django.urls import path
from .views import Studio, Tasks, Taskscreate, Taskupdate, Statistics, Settings, SocialNetworkPage
from . import views

app_name = 'studio'
urlpatterns = [
    path('',                         Studio.as_view(),      name="studio"),
    path('profile/save',             views.saveprofile,     name='saveprofile'),
    path('tasks/',                   Tasks.as_view(),       name="tasks"),
    path('tasks/create',             Taskscreate.as_view(), name="taskcreate"),
    path('tasks/create/new',         views.taskcreatenew,   name="taskcreatenew"),
    path('tasks/update/<pk>',        Taskupdate.as_view(),  name="taskupdate"),
    path('tasks/update/save/<pk>',   views.taskupdatesave,  name="taskupdatesave"),
    path('tasks/delete',             views.taskdelete,      name="taskdelete"),
    path('statistics/',              Statistics.as_view(),  name="statistics"),
    path('settings/',                Settings.as_view(),    name="settings"),
    path('social-network',           SocialNetworkPage.as_view(), name="social_network_page"),
    path('social-network/create/telegram', views.createtelegram,  name="settingscreatetelegram"),
    path('social-network/delete/telegram', views.deletetelegram,  name="settingsdeletetelegram"),
    path('social-network/create/facebbok', views.createfacebook,  name="settingscreatefacebook"),
    path('social-network/delete/facebbok', views.deletefacebook,  name="settingsdeletefacebook"),
]
