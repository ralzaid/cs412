from django.db import models
from django.contrib.auth.models import User
import random

# model to track teams and their scores and match mates if needed
class Team(models.Model):
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one_teams')
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_two_teams', null=True, blank=True)

    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # assign a random teammate if player_two is not provided
        if not self.player_two:
            available_users = User.objects.exclude(
                id__in=Team.objects.values_list('player_one', flat=True)
            ).exclude(
                id__in=Team.objects.values_list('player_two', flat=True)
            ).exclude(
                id=self.player_one.id
            )
            if available_users.exists():
                self.player_two = random.choice(available_users)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Team: {self.player_one.username} & {self.player_two.username if self.player_two else 'Solo'}"


# model to track individual matches
class Match(models.Model):
    round = models.IntegerField()
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_two')
    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')

    def save(self, *args, **kwargs):
        # determine the winner based on scores
        if self.team_one_score > self.team_two_score:
            self.winner = self.team_one
        elif self.team_two_score > self.team_one_score:
            self.winner = self.team_two
        else:
            self.winner = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Round {self.round}: {self.team_one} vs {self.team_two}"
