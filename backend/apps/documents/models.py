from django.core.exceptions import ValidationError
from django.db import models

from apps.phases.models import Phase
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User


class Document(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Borrador'),
        ('IN_REVIEW', 'En revision'),
        ('APPROVED', 'Aprobado'),
    )

    DOC_TYPE_CHOICES = (
        ('ISO_CONTROL_EVIDENCE', 'Evidencia control'),
        ('POLICY', 'Politica'),
        ('PROCEDURE', 'Procedimiento'),
        ('REPORT', 'Informe'),
        ('OTHER', 'Otro'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    file = models.FileField(upload_to='documents/')
    version = models.CharField(max_length=20, default='1.0')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_documents')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    planned_date = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'documents_document'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-created_at']

    def clean(self):
        if self.status == 'APPROVED' and (not self.approved_by_id or not self.approved_at):
            raise ValidationError('Un documento aprobado requiere aprobado_por y aprobado_en.')

        if self.phase_id and self.phase.project_id != self.project_id:
            raise ValidationError('La fase debe pertenecer al mismo proyecto del documento.')

        if self.task_id:
            if self.task.phase.project_id != self.project_id:
                raise ValidationError('La tarea debe pertenecer al mismo proyecto del documento.')
            if self.phase_id and self.task.phase_id != self.phase_id:
                raise ValidationError('La tarea debe pertenecer a la fase indicada en el documento.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.project.name})'
