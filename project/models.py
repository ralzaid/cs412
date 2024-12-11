from django.db import models
from django.contrib.auth.models import User
import random
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
import random

class Team(models.Model):
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one_teams')
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_two_teams', null=True, blank=True)
    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Assign a random teammate if player_two is not provided
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

        # Save the team
        super().save(*args, **kwargs)

        # Automatically create or update a Round 1 match
        self.add_to_round_one()

    def add_to_round_one(self):
        from .models import Match

        # Fetch existing teams for round 1 matches
        existing_matches = Match.objects.filter(round=1)

        # Find any match with an open slot
        for match in existing_matches:
            if not match.team_two:
                match.team_two = self
                match.save()
                return

        # If no open slot, create a new match
        Match.objects.create(
            round=1,
            team_one=self
        )

    def __str__(self):
        return f"Team: {self.player_one.username} & {self.player_two.username if self.player_two else 'Solo'}"



STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
]

class Match(models.Model):
    team_one = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='matches_as_team_one')
    team_two = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='matches_as_team_two', null=True, blank=True)
    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)
    winner = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')
    round = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def clean(self):
        super().clean()
        if self.team_one_score < 0 or self.team_two_score < 0:
            raise ValidationError("Scores cannot be negative.")
        if self.status == 'completed' and self.team_one_score == self.team_two_score:
            raise ValidationError("A completed match cannot end in a tie.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the match

        # Determine the winner
        if self.team_one_score > self.team_two_score or not self.team_two:
            self.winner = self.team_one
        elif self.team_two and self.team_two_score > self.team_one_score:
            self.winner = self.team_two
        else:
            self.winner = None  # No winner in case of a tie

        super().save(*args, **kwargs)

        # Advance winner to the next round if match is completed
        if self.status == 'completed' and self.winner:
            self.advance_winner_to_next_round()

    def advance_winner_to_next_round(self):
        next_round = self.round + 1

        # Find all matches in the next round
        matches_in_next_round = Match.objects.filter(round=next_round).order_by('id')

        # Determine position in the next round
        position = len(matches_in_next_round)

        if position % 2 == 0:  # First slot in a new match
            Match.objects.create(
                team_one=self.winner,
                round=next_round,
                status='scheduled'
            )
        else:  # Fill the second slot in the last match or set as a "TBD"
            last_match = matches_in_next_round.last()
            if last_match and not last_match.team_two:
                last_match.team_two = self.winner
                last_match.save()
            else:
                # If no match exists, create one with "TBD"
                Match.objects.create(
                    team_one=self.winner,
                    team_two=None,  # No opponent yet, treated as a TBD
                    round=next_round,
                    status='scheduled'
                )

