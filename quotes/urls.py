from django.urls import path
# from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/', views.random_quote, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]