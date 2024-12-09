from django.urls import path
from .views import TeamListView, MatchBracketView, MatchDetailView, create_team, update_match, home, signin, signup, signout

urlpatterns = [
    path('', home, name='home'), 
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('match_bracket/', MatchBracketView.as_view(), name='match-bracket'),
    path('match_detail/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('create_team/', create_team, name='create-team'),
    path('update_match/<int:pk>/', update_match, name='update-match'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
]