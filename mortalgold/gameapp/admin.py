from django.contrib import admin
from . import models


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'player1',
        'player2',
        'created_at',
        'winner',
        'loser')
    list_filter = ('id', 'created_at')
    
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.GameAction)