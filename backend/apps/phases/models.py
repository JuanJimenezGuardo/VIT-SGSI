from django.db import models
from django.core.exceptions import ValidationError
from apps.projects.models import Project

class Phase(models.Model):
    # Opciones para el estado de la fase
    PHASE_TYPE = (
        ('ASSESSMENT', 'Evaluación'),
        ('PLANNING', 'Planificación'),
        ('IMPLEMENTATION', 'Implementación'),
        ('AUDIT', 'Auditoría'),
        ('CERTIFICATION', 'Certificación'),
    )
    
    # Campos del modelo Phase
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases', verbose_name='Proyecto')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=PHASE_TYPE)
    description = models.TextField(blank=True)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    order = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} - {self.get_type_display()}'

    def clean(self):
        if self.planned_start_date and self.planned_end_date and self.planned_end_date < self.planned_start_date:
            raise ValidationError('La fecha de fin planeada no puede ser menor que la fecha de inicio planeada.')
        if self.actual_start_date and self.actual_end_date and self.actual_end_date < self.actual_start_date:
            raise ValidationError('La fecha de fin real no puede ser menor que la fecha de inicio real.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phases_phase'
        verbose_name = 'Phase'
        verbose_name_plural = 'Phases'
        constraints = [
            models.UniqueConstraint(fields=['project', 'order'], name='uniq_phase_project_order')
        ]