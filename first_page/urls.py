from django.urls import path
from .views import FirstPage, SignupPage, LoginPage
from . import views

app_name = 'first_page'
urlpatterns = [
    path('',       FirstPage.as_view(),  name="first_page"),
    path('signup', SignupPage.as_view(), name="register_page"),
    path('login',  LoginPage.as_view(),  name="login_page"),
    path('logout', views.user_logout,    name="logout"),
]
