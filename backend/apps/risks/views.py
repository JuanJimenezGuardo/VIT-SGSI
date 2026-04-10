import os
import threading

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Risk, Job
from .serializers import RiskSerializer
from .services import execute_recalc_job
from apps.projects.models import Project

class RiskViewSet(viewsets.ModelViewSet):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _is_assigned_to_project(self, user, project: Project) -> bool:
        return project.project_users.filter(user=user).exists()

    def _can_view_project(self, user, project: Project) -> bool:
        if not hasattr(user, 'role'):
            return False
        if user.role == 'ADMIN':
            return True
        if user.role in ['CONSULTANT', 'CLIENT']:
            return self._is_assigned_to_project(user, project)
        return False

    def _can_trigger_job(self, user, project: Project) -> bool:
        if not hasattr(user, 'role'):
            return False
        if user.role == 'ADMIN':
            return True
        if user.role == 'CONSULTANT':
            return self._is_assigned_to_project(user, project)
        return False

    def _can_modify_project(self, user, project: Project) -> bool:
        if not hasattr(user, 'role'):
            return False
        if user.role == 'ADMIN':
            return True
        if user.role == 'CONSULTANT':
            return self._is_assigned_to_project(user, project)
        return False

    def get_queryset(self):
        # 1. Filtro base: no mostrar eliminados lógicamente (soft-delete)
        qs = Risk.objects.filter(is_archived=False).select_related('project', 'owner')
        
        # 2. Filtrar por project_id en query params (ej: /api/projects/1/risks/ o /api/risks/?project_id=1)
        project_id = self.request.query_params.get('project_id')
        if project_id:
            qs = qs.filter(project_id=project_id)

        # 3. Validar rol del usuario contra valores reales del modelo User
        user = self.request.user
        
        if hasattr(user, 'role'):
            if user.role == 'ADMIN':
                return qs
            elif user.role in ['CONSULTANT', 'CLIENT']:
                # CONSULTANT y CLIENT solo ven riesgos de proyectos asignados
                return qs.filter(project__project_users__user=user).distinct()
                
        return qs.none() # Si no tiene rol o no coincide, no ve nada por seguridad

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if not self._can_modify_project(self.request.user, project):
            raise PermissionDenied("No tienes permisos para crear riesgos en este proyecto.")
        serializer.save()

    def perform_update(self, serializer):
        project = serializer.instance.project
        if not self._can_modify_project(self.request.user, project):
            raise PermissionDenied("No tienes permisos para editar riesgos en este proyecto.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self._can_modify_project(self.request.user, instance.project):
            raise PermissionDenied("No tienes permisos para eliminar riesgos en este proyecto.")
        # Soft-delete: en lugar de borrar de la BD, lo marcamos como archivado
        instance.is_archived = True
        instance.save()

    # --- ENDPOINTS CUSTOM DE JOBS PARALELOS ---

    @action(detail=False, methods=['post'], url_path=r'(?P<project_id>\d+)/trigger-recalc')
    def trigger_recalc(self, request, project_id=None):
        project = get_object_or_404(Project, pk=project_id)

        # Validación de permisos: solo ADMIN o CONSULTANT asignado
        if not self._can_trigger_job(request.user, project):
            return Response({"detail": "No tienes permisos para disparar el cálculo."}, status=status.HTTP_403_FORBIDDEN)

        # Crear el registro del Job en estado PENDING
        job = Job.objects.create(project=project, status='PENDING')

        workers_input = request.data.get('workers', request.query_params.get('workers', 4))
        try:
            workers = int(workers_input)
        except (TypeError, ValueError):
            workers = 4
        max_workers = os.cpu_count() or 4
        workers = max(1, min(workers, max_workers))

        sync_raw = request.data.get('sync', request.query_params.get('sync', 'false'))
        sync_mode = str(sync_raw).strip().lower() in {'1', 'true', 'yes'}

        if sync_mode:
            execute_recalc_job(job.job_id, worker_count=workers)
            job.refresh_from_db()
        else:
            threading.Thread(
                target=execute_recalc_job,
                kwargs={'job_id': job.job_id, 'worker_count': workers},
                daemon=True,
            ).start()

        return Response({
            "job_id": job.job_id,
            "status": job.status,
            "created_at": job.created_at,
            "mode": "sync" if sync_mode else "async",
            "workers": workers,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path=r'job-status/(?P<job_id>[^/.]+)')
    def job_status(self, request, job_id=None):
        job = get_object_or_404(Job, pk=job_id)

        if not self._can_view_project(request.user, job.project):
            return Response({"detail": "No tienes acceso a este job."}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            "job_id": job.job_id,
            "status": job.status,
            "progress": job.progress,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "tseq_ms": job.tseq_ms,
            "tpar_ms": job.tpar_ms,
            "speedup": job.speedup,
            "result": job.result
        }, status=status.HTTP_200_OK)