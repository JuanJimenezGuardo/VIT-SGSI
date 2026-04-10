import api from '../api/axios';

export const projectService = {
    // 1. Obtener lista de proyectos (Para el Dashboard)
    getAllProjects: async () => {
        const response = await api.get('/projects/');
        const data = response.data.results ? response.data.results : response.data;
        
        // Mapeo: Asegurar nombres consistentes para la UI (camelCase)
        return data.map(project => ({
            id: project.id,
            name: project.name,
            clientName: project.company_name, // Estandarizamos
            status: project.status,
            isActive: project.status === 'ACTIVE' || project.status === 'IN_PROGRESS',
        }));
    },

    // 2. Obtener detalle de un proyecto
    getProjectById: async (id) => {
        const response = await api.get(`/projects/${id}/`);
        const project = response.data;

        // Mapeo: Estructura limpia y segura
        return {
            id: project.id,
            name: project.name,
            description: project.description,
            clientName: project.company_name,
            status: project.status,
            refId: `PROJ-${project.id.toString().padStart(3, '0')}`,
            contacts: project.contacts || [], // Evita errores si viene nulo
        };
    },

    // 3. Obtener fases de un proyecto
    getProjectPhases: async (projectId) => {
        const response = await api.get('/phases/');
        const allPhases = response.data.results ? response.data.results : response.data;
        
        const projectPhases = allPhases.filter(p => p.project === parseInt(projectId));

        // Mapeo: Transformar datos crudos
        return projectPhases.map(phase => ({
            id: phase.id,
            name: phase.name,
            type: phase.type,
            description: phase.description,
            plannedStart: phase.planned_start_date,
            actualStart: phase.actual_start_date,
            hasStarted: !!phase.actual_start_date,
            notesCount: phase.notes_count || 0,
            docsCount: phase.documents_count || 0,
        }));
    }
};