from . import models
from rest_framework import serializers


class MatchSerializer(serializers.ModelSerializer):
    player1_id = serializers.ReadOnlyField(source='player1.id')
    player2_id = serializers.ReadOnlyField(source='player2.id')
    player1 = serializers.ReadOnlyField(source='player1.username')
    player2 = serializers.ReadOnlyField(source='player2.username')
    played_at = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Match
        fields = ['id', 'player1_id', 'player2_id', 'player1', 'player2', 'played_at']


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    played = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = ['id', 'user', 'user_id', 'score', 'played', 'match']
