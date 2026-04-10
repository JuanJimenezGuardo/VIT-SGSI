from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project, ProjectUser
from apps.phases.models import Phase
from apps.tasks.models import Task
from apps.users.models import AuditLog
import json


@receiver(post_save, sender=Project)
def log_project_save(sender, instance, created, **kwargs):
    """
    Signal para registrar creacion y actualizacion de proyectos en AuditLog.
    """
    action = 'CREATE' if created else 'UPDATE'
    user = instance.created_by  # Usuario que creo el proyecto
    
    changes = {
        'name': instance.name,
        'company': instance.company.name,
        'status': instance.status,
        'planned_start_date': str(instance.planned_start_date),
    }
    
    AuditLog.objects.create(
        user=user,
        action=action,
        entity_type='Project',
        entity_id=instance.id,
        changes=changes
    )


@receiver(post_delete, sender=Project)
def log_project_delete(sender, instance, **kwargs):
    """
    Signal para registrar eliminacion de proyectos en AuditLog.
    """
    user = instance.created_by
    
    AuditLog.objects.create(
        user=user,
        action='DELETE',
        entity_type='Project',
        entity_id=instance.id,
        changes={'name': instance.name, 'company': instance.company.name}
    )


@receiver(post_save, sender=Phase)
def log_phase_save(sender, instance, created, **kwargs):
    """
    Signal para registrar creacion y actualizacion de fases en AuditLog.
    """
    action = 'CREATE' if created else 'UPDATE'
    user = instance.project.created_by  # Usuario del proyecto asociado
    
    changes = {
        'name': instance.name,
        'type': instance.type,
        'project': instance.project.name,
        'planned_start_date': str(instance.planned_start_date),
    }
    
    AuditLog.objects.create(
        user=user,
        action=action,
        entity_type='Phase',
        entity_id=instance.id,
        changes=changes
    )


@receiver(post_delete, sender=Phase)
def log_phase_delete(sender, instance, **kwargs):
    """
    Signal para registrar eliminacion de fases en AuditLog.
    """
    user = instance.project.created_by
    
    AuditLog.objects.create(
        user=user,
        action='DELETE',
        entity_type='Phase',
        entity_id=instance.id,
        changes={'name': instance.name, 'project': instance.project.name}
    )


@receiver(post_save, sender=Task)
def log_task_save(sender, instance, created, **kwargs):
    """
    Signal para registrar creacion y actualizacion de tareas en AuditLog.
    """
    action = 'CREATE' if created else 'UPDATE'
    user = instance.assigned_to or instance.phase.project.created_by
    
    changes = {
        'name': instance.name,
        'phase': instance.phase.name,
        'status': instance.status,
        'priority': instance.priority,
        'assigned_to': instance.assigned_to.username if instance.assigned_to else None,
    }
    
    AuditLog.objects.create(
        user=user,
        action=action,
        entity_type='Task',
        entity_id=instance.id,
        changes=changes
    )


@receiver(post_delete, sender=Task)
def log_task_delete(sender, instance, **kwargs):
    """
    Signal para registrar eliminacion de tareas en AuditLog.
    """
    user = instance.assigned_to or instance.phase.project.created_by
    
    AuditLog.objects.create(
        user=user,
        action='DELETE',
        entity_type='Task',
        entity_id=instance.id,
        changes={'name': instance.name, 'phase': instance.phase.name}
    )


@receiver(post_save, sender=ProjectUser)
def log_projectuser_save(sender, instance, created, **kwargs):
    """
    Signal para registrar asignacion y actualizacion de usuarios a proyectos.
    """
    action = 'CREATE' if created else 'UPDATE'
    user = instance.project.created_by
    
    changes = {
        'user': instance.user.username,
        'project': instance.project.name,
        'role': instance.role,
    }
    
    AuditLog.objects.create(
        user=user,
        action=action,
        entity_type='ProjectUser',
        entity_id=instance.id,
        changes=changes
    )


@receiver(post_delete, sender=ProjectUser)
def log_projectuser_delete(sender, instance, **kwargs):
    """
    Signal para registrar eliminacion de asignaciones de usuarios a proyectos.
    """
    user = instance.project.created_by
    
    AuditLog.objects.create(
        user=user,
        action='DELETE',
        entity_type='ProjectUser',
        entity_id=instance.id,
        changes={'user': instance.user.username, 'project': instance.project.name}
    )
