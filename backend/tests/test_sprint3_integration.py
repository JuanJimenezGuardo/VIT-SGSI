from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.companies.models import Company
from apps.risks.models import Risk, Job
from django.utils import timezone

User = get_user_model()

class Sprint3IntegrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 1. Crear empresa base
        cls.company = Company.objects.create(name="ACME")
        
        # 2. Crear usuario Admin
        cls.admin_user = User.objects.create_user(
            username="admin_sprint3",
            email="osky_test@test.com",
            password="password123",
            role="ADMIN"
        )
        
        # 3. Crear proyecto con campos reales del modelo Project
        cls.project = Project.objects.create(
            name="Proyecto Prueba Sprint 3",
            company=cls.company,
            planned_start_date=timezone.now().date(),
            created_by=cls.admin_user,
        )

    def test_1_login_obtiene_token(self):
        # Usamos login del sistema para verificar que las credenciales son válidas
        login_exitoso = self.client.login(email='osky_test@test.com', password='password123')
        
        # Si tu proyecto usa Username en lugar de Email para el login interno:
        if not login_exitoso:
            login_exitoso = self.client.login(username='admin_sprint3', password='password123')
            
        self.assertTrue(login_exitoso, "El login falló con las credenciales creadas en setUpTestData")
    def test_2_token_valido_accede_proyectos(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_3_sin_token_recibe_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_4_crear_riesgo_rechaza_datos_invalidos(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "project": self.project.id,
            "name": "",
            "probability": 10,
            "impact": 5,
            "treatment_strategy": "Mitigate"
        }
        response = self.client.post('/api/risks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_5_crear_riesgo_valido_guarda_en_bd(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "project": self.project.id,
            "name": "Riesgo de Seguridad Critico",
            "probability": 4,
            "impact": 5,
            "treatment_strategy": "Mitigate",
            "owner": self.admin_user.id
        }
        response = self.client.post('/api/risks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Risk.objects.count(), 1)

    def test_6_listar_riesgos_filtra_por_proyecto(self):
        self.client.force_authenticate(user=self.admin_user)
        Risk.objects.create(
            project=self.project, 
            name="Riesgo Existente", 
            probability=3, 
            impact=3, 
            treatment_strategy="Accept"
        )
        response = self.client.get(f'/api/risks/?project_id={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_7_consultar_job_status_devuelve_estado_correcto(self):
        self.client.force_authenticate(user=self.admin_user)
        job = Job.objects.create(project=self.project, status='RUNNING', progress=45)
        response = self.client.get(f'/api/risks/job-status/{job.job_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'RUNNING')