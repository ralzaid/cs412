from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='Show_all'),
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]