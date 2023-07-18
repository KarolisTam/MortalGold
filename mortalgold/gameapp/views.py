#views.py
from . import models, serializers
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import render


class MatchCreateList(generics.ListCreateAPIView):
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return models.Match.objects.filter(player2__isnull=True)

    def perform_create(self, serializer):
        serializer.save(player1=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_matches = queryset.filter(player1=self.request.user)
        if user_matches.exists():
            return Response({"detail": "You cannot join your own created room."}, status=403)

        if queryset.exists():
            match = queryset.first()
            match.player2 = self.request.user
            match.save()
            return Response(serializers.MatchSerializer(match).data)
        else:
            serializer = serializers.MatchSerializer(data={"player1": request.user})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })