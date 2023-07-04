from django.contrib import admin
from . import models


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'player1',
        'player2',
        'created_at',
        'winner',
        'looser')
    list_filter = ('id', 'created_at')
    

class GameActionAdmin(admin.ModelAdmin):
    pass