from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='Show_all'),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]