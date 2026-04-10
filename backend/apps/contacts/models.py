from django.db import models

from apps.companies.models import Company
from apps.users.models import User


class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_profile',
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_notes = models.TextField(blank=True)   

    class Meta:
        db_table = 'contacts_contact'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['company', 'email'], name='uniq_contact_company_email')
        ]

    def __str__(self):
        return f'{self.full_name} ({self.company.name})'
