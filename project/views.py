from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Team, Match
from .forms import TeamForm, MatchForm
import math

# Homepage view
def home(request):
    return render(request, 'project/home.html')


# List of all teams & Brackets
class TeamListView(ListView):
    model = Team
    template_name = 'project/team_list.html'
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = list(self.get_queryset())
        total_teams = len(teams)

        if total_teams < 2:
            context['error'] = "Not enough teams to create a bracket. Add more teams!"
            return context

        # Calculate the next power of two greater than or equal to total_teams
        next_power_of_two = 2 ** math.ceil(math.log2(total_teams))
        while len(teams) < next_power_of_two:
            teams.append(None)

        rounds = math.ceil(math.log2(next_power_of_two))
        matches_by_round = {}

        # Generate matches by round
        for r in range(1, rounds + 1):
            matches_by_round[r] = Match.objects.filter(round=r).order_by('id')

        context['matches_by_round'] = matches_by_round
        context['rounds'] = range(1, rounds + 1)
        return context



# Match Detail View with Update Functionality
@login_required(login_url='/signin/')
def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    user_involved = request.user in [
        match.team_one.player_one,
        match.team_one.player_two,
        match.team_two.player_one if match.team_two else None,
        match.team_two.player_two if match.team_two else None
    ]

    if request.method == 'POST' and user_involved:
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()  # Automatically updates the winner and advances them if status is completed
            messages.success(request, "Match updated successfully!")
            return redirect('team-list')
        else:
            messages.error(request, "Failed to update match. Please check your input.")
    else:
        form = MatchForm(instance=match) if user_involved else None

    return render(request, 'project/match_detail.html', {
        'match': match,
        'form': form,
        'user_involved': user_involved
    })




# Create a New Team
@login_required(login_url='/signin/')
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Team created successfully!")
            return redirect('team-list')
    else:
        form = TeamForm()

    return render(request, 'project/create_team.html', {'form': form})


# User Signup View
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('signin')

    return render(request, 'project/signup.html')


# User Signin View
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'project/signin.html')


# User Signout View
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('signin')



def create_and_display_bracket(request):
    # Fetch all teams
    teams = list(Team.objects.all())
    total_teams = len(teams)

    # Ensure teams fit into a power of 2
    if total_teams < 2:
        return render(request, 'project/team-list.html', {
            'error': "Not enough teams to create a bracket. Add more teams!"
        })

    next_power_of_two = 2 ** math.ceil(math.log2(total_teams))
    while len(teams) < next_power_of_two:
        teams.append(None)  # Add placeholder teams

    rounds = math.ceil(math.log2(next_power_of_two))
    matches_by_round = {}

    # Generate matches for Round 1
    round_matches = []
    for i in range(0, len(teams), 2):
        team_one = teams[i]
        team_two = teams[i + 1] if i + 1 < len(teams) else None
        match= Match.objects.get_or_create(
            team_one=team_one,
            team_two=team_two,
            round=1
        )
        round_matches.append(match)

    matches_by_round[1] = round_matches

    # Automatically progress winners to the next round
    for r in range(2, rounds + 1):
        previous_round_matches = matches_by_round[r - 1]
        current_round_matches = []
        for i in range(0, len(previous_round_matches), 2):
            winner_one = previous_round_matches[i].winner if previous_round_matches[i] else None
            winner_two = previous_round_matches[i + 1].winner if i + 1 < len(previous_round_matches) else None
            match = Match.objects.get_or_create(
                team_one=winner_one,
                team_two=winner_two,
                round=r
            )
            current_round_matches.append(match)
        matches_by_round[r] = current_round_matches

    # Pass matches grouped by round to the template
    return render(request, 'project/team-list.html', {
        'matches_by_round': matches_by_round,
        'rounds': range(1, rounds + 1)
    })