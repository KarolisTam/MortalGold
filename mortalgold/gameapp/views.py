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


class MatchDetailJoin(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return models.Match.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            match = models.Match.objects.get(pk=kwargs['pk'], player2__isnull=True)
        except Exception as e:
            raise ValidationError('You cannot join this game.')
        else:
            return self.update(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.player2 = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializers.MatchSerializer(instance).data)
