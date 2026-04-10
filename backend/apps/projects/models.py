from django.db import models
from django.core.exceptions import ValidationError
from apps.companies.models import Company
from apps.users.models import User
from apps.contacts.models import Contact

# Choices para Project
PROJECT_STATUS_CHOICES = (
    ('PLANNING', 'Planeación'),
    ('IN_PROGRESS', 'En progreso'),
    ('COMPLETED', 'Completado'),
    ('ON_HOLD', 'En pausa'),
)

# Modelo Project
class Project(models.Model):
    """Proyecto ISO 27001 para una empresa"""
    name = models.CharField(max_length=255, verbose_name='Nombre del proyecto')
    description = models.TextField(blank=True, verbose_name='Descripción')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects', verbose_name='Empresa')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='PLANNING', verbose_name='Estado')
    planned_start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de inicio planeada')
    planned_end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin planeada')
    actual_start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de inicio real')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created', verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    def __str__(self):
        return f'{self.name} - {self.company.name}'

    def clean(self):
        if self.planned_start_date and self.planned_end_date and self.planned_end_date < self.planned_start_date:
            raise ValidationError('La fecha de fin planeada no puede ser menor que la fecha de inicio planeada.')
        if self.actual_start_date and self.actual_end_date and self.actual_end_date < self.actual_start_date:
            raise ValidationError('La fecha de fin real no puede ser menor que la fecha de inicio real.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'projects_project'
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-created_at']


# Choices para ProjectUser
PROJECT_ROLE_CHOICES = (
    ('ADMIN', 'Administrador del Proyecto'),
    ('CONSULTANT', 'Consultor'),
    ('CLIENT', 'Cliente'),
    ('VIEWER', 'Observador'),
)


class ProjectUser(models.Model):
    """
    Relación entre usuarios y proyectos con roles específicos.
    Permite que un usuario tenga diferentes roles en diferentes proyectos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_users', verbose_name='Proyecto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_assignments', verbose_name='Usuario')
    role = models.CharField(max_length=20, choices=PROJECT_ROLE_CHOICES, default='CLIENT', verbose_name='Rol en el proyecto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        db_table = 'projects_projectuser'
        verbose_name = 'Usuario de Proyecto'
        verbose_name_plural = 'Usuarios de Proyectos'
        # Un usuario solo puede tener un rol por proyecto (sin duplicados)
        unique_together = ['project', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.project.name} ({self.get_role_display()})'


class ProjectContact(models.Model):
    """Relacion entre proyecto y contactos de la empresa participante."""

    CONTACT_ROLE_CHOICES = (
        ('PROJECT_MANAGER', 'Gestor Proyecto'),
        ('CISO', 'CISO'),
        ('IT_MANAGER', 'Gerente TI'),
        ('CONSULTANT', 'Consultor'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_contacts', verbose_name='Proyecto')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='project_contacts', verbose_name='Contacto')
    contact_role = models.CharField(max_length=30, choices=CONTACT_ROLE_CHOICES, verbose_name='Rol del contacto')
    is_primary = models.BooleanField(default=False, verbose_name='Es contacto principal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    work_notes = models.TextField(blank=True)   


    class Meta:
        db_table = 'projects_projectcontact'
        verbose_name = 'Contacto de Proyecto'
        verbose_name_plural = 'Contactos de Proyecto'
        unique_together = ['project', 'contact']
        ordering = ['-created_at']

    def clean(self):
        if self.contact_id and self.project_id and self.contact.company_id != self.project.company_id:
            raise ValidationError('El contacto debe pertenecer a la misma empresa del proyecto.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.contact.full_name} - {self.project.name}'