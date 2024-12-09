from django.db import models
from django.contrib.auth.models import User
import random
from django.core.exceptions import ValidationError

class Team(models.Model):
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one_teams')
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_two_teams', null=True, blank=True)
    score = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player_one', 'player_two'],
                name='unique_team'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.player_two:
            available_users = User.objects.exclude(
                id__in=Team.objects.values_list('player_one', flat=True)
            ).exclude(
                id__in=Team.objects.values_list('player_two', flat=True)
            ).exclude(
                id=self.player_one.id
            ).distinct()

            if available_users.exists():
                self.player_two = random.choice(list(available_users))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Team: {self.player_one.username} & {self.player_two.username if self.player_two else 'Solo'}"


STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
]

class Match(models.Model):
    round = models.IntegerField()
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_two')
    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def clean(self):
        if self.team_one_score < 0 or self.team_two_score < 0:
            raise ValidationError("Scores cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        if self.team_one_score > self.team_two_score:
            self.winner = self.team_one
        elif self.team_two_score > self.team_one_score:
            self.winner = self.team_two
        else:
            self.winner = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Round {self.round}: {self.team_one} vs {self.team_two}"

    @classmethod
    def get_round_winners(cls, round_number):
        return cls.objects.filter(round=round_number, winner__isnull=False).values_list('winner', flat=True)
