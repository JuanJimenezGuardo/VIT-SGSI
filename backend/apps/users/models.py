from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de Usuario personalizado que extiende AbstractUser.
    ✅ HEREDA: username, email, password, first_name, last_name, is_active, etc.
    ✅ AGREGA: role, phone con lógica específica para VIT
    """
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador VIT'),
        ('CONSULTANT', 'Consultor'),
        ('CLIENT', 'Cliente'),
    )
    
    # Campos personalizados para VIT
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username