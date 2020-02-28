from django.urls import path
from . import views

app_name = 'first_page'
urlpatterns = [
    path('', views.page, name="first_page")
]
