from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, ProjectUser, ProjectContact
from .serializers import ProjectSerializer, ProjectUserSerializer, ProjectContactSerializer
from apps.users.permissions import IsConsultantOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de proyectos.
    Consultores y Admin pueden crear/editar proyectos.
    Filtrado dinámico: Admin ve todos, Consultant/Client solo sus asignados.
    """
    queryset = Project.objects.all()  # Base queryset para router (se sobrescribe en get_queryset)
    serializer_class = ProjectSerializer
    permission_classes = [IsConsultantOrReadOnly]
    
    def get_queryset(self):
        """
        Filtrar proyectos según rol del usuario:
        - ADMIN: ve todos los proyectos
        - CONSULTANT/CLIENT: solo proyectos donde está asignado (vía ProjectUser)
        """
        user = self.request.user
        
        if user.role == 'ADMIN':
            return Project.objects.all()
        else:
            # Filtrar por proyectos donde el usuario está asignado
            return Project.objects.filter(project_users__user=user).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """
        Endpoint: GET /api/projects/{id}/users/
        Retorna lista de usuarios asignados al proyecto.
        """
        project = self.get_object()
        project_users = ProjectUser.objects.filter(project=project).select_related('user')
        serializer = ProjectUserSerializer(project_users, many=True)
        return Response(serializer.data)


class ProjectUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para asignación de usuarios a proyectos.
    Consultores y Admin pueden asignar usuarios a proyectos.
    Todos los autenticados pueden ver asignaciones.
    """
    queryset = ProjectUser.objects.select_related('project', 'user')
    serializer_class = ProjectUserSerializer
    permission_classes = [IsConsultantOrReadOnly]


class ProjectContactViewSet(viewsets.ModelViewSet):
    queryset = ProjectContact.objects.select_related('project', 'contact')
    serializer_class = ProjectContactSerializer
    permission_classes = [IsConsultantOrReadOnly]