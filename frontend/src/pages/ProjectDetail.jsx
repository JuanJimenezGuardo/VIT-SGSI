import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/axios';

export default function ProjectDetail() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [phases, setPhases] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProjectData = async () => {
            try {
                // 1. Obtener detalles del proyecto
                const projectRes = await api.get(`/projects/${id}/`);
                setProject(projectRes.data);

                // 2. Obtener y filtrar fases vinculadas a este proyecto
                const phasesRes = await api.get(`/phases/`);
                const allPhases = phasesRes.data.results ? phasesRes.data.results : phasesRes.data;
                
                const projectPhases = allPhases.filter(p => p.project === parseInt(id));
                setPhases(projectPhases);

            } catch (error) {
                console.error("Error en la sincronización de datos:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchProjectData();
    }, [id]);

    if (loading) return (
        <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}>
            <div className="badge">DESCRIPTANDO DATOS DEL PROYECTO...</div>
        </div>
    );

    if (!project) return (
        <div className="container" style={{ textAlign: 'center' }}>
            <h2 style={{ color: '#ef4444' }}>ERROR 404: MÓDULO NO ENCONTRADO</h2>
            <Link to="/dashboard" className="btn btn-primary">VOLVER AL PANEL</Link>
        </div>
    );

    return (
        <div className="container">
            {/* Navegación Superior */}
            <nav style={{ marginBottom: '2rem' }}>
                <Link to="/dashboard" style={{ 
                    color: 'var(--primary)', 
                    textDecoration: 'none', 
                    fontSize: '0.8rem', 
                    fontWeight: 'bold',
                    letterSpacing: '1px'
                }}>
                    ‹ VOLVER AL DASHBOARD_
                </Link>
            </nav>

            {/* Cabecera del Proyecto */}
            <header className="card" style={{ 
                borderLeft: '4px solid var(--primary)', 
                marginBottom: '3rem',
                background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                        <span className="badge" style={{ marginBottom: '1rem', display: 'inline-block' }}>
                            SISTEMA: {project.status}
                        </span>
                        <h1 style={{ 
                            margin: 0, 
                            fontSize: '2.5rem', 
                            color: 'white',
                            textShadow: '0 0 10px var(--primary-glow)' 
                        }}>
                            {project.name}
                        </h1>
                    </div>
                    <div style={{ textAlign: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        <code>REF_ID: PROJ-{project.id.toString().padStart(3, '0')}</code><br />
                        <code>CLIENTE: {project.company_name}</code>
                    </div>
                </div>
                <p style={{ marginTop: '1.5rem', color: 'var(--text-muted)', fontSize: '1.1rem', maxWidth: '800px' }}>
                    {project.description}
                </p>
            </header>

            {/* Sección de Fases */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '2rem' }}>
                <h2 style={{ margin: 0, fontSize: '1.2rem', letterSpacing: '2px', color: 'var(--accent)' }}>
                    SECUENCIA DE FASES
                </h2>
                <div style={{ flex: 1, height: '1px', background: 'var(--border)' }}></div>
            </div>

            {phases.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {phases.map((phase, index) => (
                        <div key={phase.id} className="card" style={{ 
                            display: 'flex', 
                            gap: '20px', 
                            alignItems: 'center',
                            padding: '1rem 2rem'
                        }}>
                            {/* Indicador de número de fase */}
                            <div style={{ 
                                width: '40px', 
                                height: '40px', 
                                borderRadius: '50%', 
                                border: '2px solid var(--primary)', 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'center',
                                fontWeight: 'bold',
                                color: 'var(--primary)',
                                boxShadow: '0 0 10px var(--primary-glow)'
                            }}>
                                {index + 1}
                            </div>

                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <h3 style={{ margin: 0, color: 'white' }}>{phase.name}</h3>
                                    <span style={{ fontSize: '0.7rem', color: 'var(--primary)', fontWeight: 'bold' }}>
                                        [{phase.type}]
                                    </span>
                                </div>
                                <p style={{ margin: '5px 0 0 0', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                                    {phase.description}
                                </p>
                            </div>

                            {/* Acceso a Tareas */}
                            <button className="btn" style={{ 
                                backgroundColor: 'rgba(56, 189, 248, 0.1)', 
                                border: '1px solid var(--primary)',
                                color: 'var(--primary)',
                                fontSize: '0.7rem'
                            }}>
                                VER TAREAS_
                            </button>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="card" style={{ textAlign: 'center', opacity: 0.5 }}>
                    <p>No hay secuencias de fases cargadas para este módulo.</p>
                </div>
            )}
            
            <footer style={{ marginTop: '4rem', textAlign: 'center', opacity: 0.2, fontSize: '0.7rem' }}>
                PROYECTO VIT // ACCESO NIVEL 1 // {new Date().getFullYear()}
            </footer>
        </div>
    );
}