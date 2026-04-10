from django.db import models

from apps.contacts.models import Contact
from apps.projects.models import Project
from apps.users.models import User


class Asset(models.Model):
    ASSET_TYPES = [
        ('HARDWARE', 'Hardware'),
        ('SOFTWARE', 'Software'),
        ('SERVICE', 'Servicio'),
        ('INFRASTRUCTURE', 'Infraestructura'),
    ]

    CLASSIFICATIONS = [
        ('PUBLIC', 'Publico'),
        ('INTERNAL', 'Interno'),
        ('CONFIDENTIAL', 'Confidencial'),
        ('RESTRICTED', 'Restringido'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
        ('RETIRED', 'Retirado'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='assets',
    )
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    owner_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_assets',
    )
    responsible_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_assets',
    )
    classification = models.CharField(max_length=50, choices=CLASSIFICATIONS, default='INTERNAL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name