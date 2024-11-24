from django.views.generic import ListView, DetailView
from .models import Team, Match
from django.shortcuts import render, redirect
from .forms import TeamForm, MatchForm

class TeamListView(ListView):
    model = Team
    template_name = 'project/team_list.html'
    context_object_name = 'teams'

class MatchBracketView(ListView):
    model = Match
    template_name = 'project/match_bracket.html'
    context_object_name = 'matches'

class MatchDetailView(DetailView):
    model = Match
    template_name = 'project/match_detail.html'
    context_object_name = 'match'

def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team-list')
    else:
        form = TeamForm()
    return render(request, 'project/create_team.html', {'form': form})

def update_match(request, pk):
    match = Match.objects.get(pk=pk)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match-bracket')
    else:
        form = MatchForm(instance=match)
    return render(request, 'project/update_match.html', {'form': form})
