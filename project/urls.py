from django.urls import path
from .views import TeamListView, MatchBracketView, MatchDetailView, create_team, update_match


urlpatterns = [
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('match_bracket/', MatchBracketView.as_view(), name='match-bracket'),
    path('match_detail/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('', TeamListView.as_view(), name='project-home'),
    path('create_team/', create_team, name='create-team'),
    path('update_match/<int:pk>/', update_match, name='update-match'),
]
