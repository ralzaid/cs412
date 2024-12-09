from django.views.generic import ListView, DetailView
from .models import Team, Match
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeamForm, MatchForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import math


# List of all teams
class TeamListView(ListView):
    model = Team
    template_name = 'project/team_list.html'
    context_object_name = 'teams'


# Display the tournament bracket
class MatchBracketView(ListView):
    model = Match
    template_name = 'project/match_bracket.html'
    context_object_name = 'matches'

def match_bracket(request):
    teams = Team.objects.all()
    total_teams = len(teams)

    if total_teams < 2:
        # Handle case where there are not enough teams
        return render(request, 'project/match_bracket.html', {
            'error': "Not enough teams to create a bracket. Add more teams!"
        })

    # Calculate number of rounds needed (log2 of total teams, rounded up)
    rounds = math.ceil(math.log2(total_teams))
    matches_by_round = {}

    # Generate initial matches for the first round
    round_matches = []
    for i in range(0, total_teams, 2):
        team1 = teams[i] if i < total_teams else None
        team2 = teams[i + 1] if i + 1 < total_teams else None
        match, created = Match.objects.get_or_create(
            team1=team1,
            team2=team2,
            round_number=1
        )
        round_matches.append(match)

    matches_by_round[1] = round_matches

    # Populate subsequent rounds with placeholders
    for r in range(2, rounds + 1):
        matches_by_round[r] = [None] * (len(matches_by_round[r - 1]) // 2)

    return render(request, 'project/match_bracket.html', {
        'matches_by_round': matches_by_round,
        'rounds': range(1, rounds + 1)
    })


# Show details of a specific match
class MatchDetailView(DetailView):
    model = Match
    template_name = 'project/match_detail.html'
    context_object_name = 'match'


# Create a new team (Restricted to logged-in users)
@login_required(login_url='/signin/')
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Team created successfully!")
            return redirect('team-list')
        else:
            messages.error(request, "Failed to create team. Please check your input.")
    else:
        form = TeamForm()
    return render(request, 'project/create_team.html', {'form': form})


# Update match details (Restricted to logged-in users)
@login_required(login_url='/signin/')
def update_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, "Match updated successfully!")
            return redirect('match-bracket')
        else:
            messages.error(request, "Failed to update match. Please check your input.")
    else:
        form = MatchForm(instance=match)
    return render(request, 'project/update_match.html', {'form': form})


# Homepage view
def home(request):
    return render(request, 'project/home.html')


# User signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('signin')

    return render(request, 'project/signup.html')


# User signin view
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('signin')

    return render(request, 'project/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('signin')