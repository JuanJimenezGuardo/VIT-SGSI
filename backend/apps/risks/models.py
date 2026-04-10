import uuid
from django.db import models
from django.conf import settings
from apps.projects.models import Project

class Risk(models.Model):
    TREATMENT_CHOICES = [
        ('Accept', 'Accept'),
        ('Mitigate', 'Mitigate'),
        ('Transfer', 'Transfer'),
        ('Avoid', 'Avoid'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='risks')
    asset_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    probability = models.IntegerField()
    impact = models.IntegerField()
    treatment_strategy = models.CharField(max_length=20, choices=TREATMENT_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project', 'name', 'asset_id')

class Job(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('RUNNING', 'RUNNING'),
        ('SUCCESS', 'SUCCESS'),
        ('FAILED', 'FAILED'),
    ]
    
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    tseq_ms = models.FloatField(null=True, blank=True)
    tpar_ms = models.FloatField(null=True, blank=True)
    speedup = models.FloatField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Job {self.job_id} - {self.status}"