from django.contrib import admin
from .models import User, Team, Match

admin.site.register(Team)
admin.site.register(Match)
