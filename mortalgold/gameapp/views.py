#views.py
from . import models, serializers
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class MatchCreateList(generics.ListCreateAPIView):
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return models.Match.objects.filter(player2__isnull=True)

    def perform_create(self, serializer):
        serializer.save(player1=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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

