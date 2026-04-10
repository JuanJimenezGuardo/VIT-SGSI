from rest_framework import viewsets

from apps.users.permissions import IsConsultantOrReadOnly
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('company', 'user')
    serializer_class = ContactSerializer
    permission_classes = [IsConsultantOrReadOnly]
