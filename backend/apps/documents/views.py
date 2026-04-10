from rest_framework import viewsets

from apps.users.permissions import IsConsultantOrReadOnly
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('project', 'phase', 'task', 'approved_by')
    serializer_class = DocumentSerializer
    permission_classes = [IsConsultantOrReadOnly]
