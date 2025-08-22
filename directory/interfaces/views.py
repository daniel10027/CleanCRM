from rest_framework import viewsets, permissions
from directory.infrastructure.models import Directory
from .serializers import DirectorySerializer

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Directory.objects.filter(owner=self.request.user)