import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';
import { projectService } from '../services/projectService'; // <-- Importamos el servicio
// import ContactFormTester from '../components/ContactFormTester'; <-- Descomentar si vas a usar el tester del Día 5

export default function ProjectDetail() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [phases, setPhases] = useState([]);
    const [loading, setLoading] = useState(true);

    // MOCK SPRINT 2 (Temporal hasta que Osky mande la lista real de contactos)
    const mockContacts = [
        { id: 1, name: 'Ana Martínez', role: 'Líder de Proyecto', email: 'ana@empresa.com' },
        { id: 2, name: 'Carlos Ruiz', role: 'Auditor Externo', email: 'cruiz@vit.com' }
    ];

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Usamos el servicio en lugar de llamar directamente a axios
                const projectData = await projectService.getProjectById(id);
                setProject(projectData);

                const phasesData = await projectService.getProjectPhases(id);
                setPhases(phasesData);

            } catch (error) {
                console.error("Error en la sincronización:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    if (loading) return <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}><div className="badge">DESCRIPTANDO DATOS...</div></div>;
    if (!project) return <div className="container" style={{ textAlign: 'center' }}><h2 style={{ color: '#ef4444' }}>ERROR 404</h2><Link to="/dashboard" className="btn btn-primary">VOLVER</Link></div>;

    // Si Osky ya manda contactos reales, usamos esos; si no, los mockups
    const displayContacts = project.contacts && project.contacts.length > 0 ? project.contacts : mockContacts;

    return (
        <div className="container">
            <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <Link to="/dashboard" style={{ color: 'var(--primary)', textDecoration: 'none', fontSize: '0.8rem', fontWeight: 'bold', letterSpacing: '1px' }}>
                    ‹ VOLVER AL DASHBOARD_
                </Link>
                <ThemeToggle />
            </nav>

            {/* Cabecera */}
            <header className="card" style={{ borderLeft: '4px solid var(--primary)', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                        <span className="badge" style={{ marginBottom: '1rem', display: 'inline-block' }}>SISTEMA: {project.status}</span>
                        <h1 style={{ margin: 0, fontSize: '2.5rem', color: 'var(--text-main)', textShadow: '0 0 10px var(--primary-glow)' }}>{project.name}</h1>
                    </div>
                    <div style={{ textAlign: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        {/* Usamos variables del servicio: refId y clientName */}
                        <code>{project.refId}</code><br />
                        <code>CLIENTE: {project.clientName}</code>
                    </div>
                </div>
                <p style={{ marginTop: '1.5rem', color: 'var(--text-muted)', fontSize: '1.1rem', maxWidth: '800px' }}>{project.description}</p>
            </header>

            {/* Contactos */}
            <section className="card" style={{ marginBottom: '3rem', padding: '1.5rem', borderLeft: '4px solid var(--success)' }}>
                <h3 style={{ marginTop: 0, fontSize: '1rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>👥 CONTACTOS ASIGNADOS</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
                    {displayContacts.map(contact => (
                        <div key={contact.id} style={{ padding: '10px', background: 'var(--bg-body)', borderRadius: '8px', border: '1px solid var(--border)' }}>
                            <div style={{ fontWeight: 'bold', color: 'var(--text-main)' }}>{contact.name}</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--primary)', marginBottom: '4px' }}>{contact.role}</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>✉️ {contact.email}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Fases */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '2rem' }}><h2 style={{ margin: 0, fontSize: '1.2rem', letterSpacing: '2px', color: 'var(--accent)' }}>SECUENCIA DE FASES</h2><div style={{ flex: 1, height: '1px', background: 'var(--border)' }}></div></div>

            {phases.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {phases.map((phase, index) => (
                        <div key={phase.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '15px', padding: '1.5rem' }}>
                            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                                <div style={{ width: '40px', height: '40px', borderRadius: '50%', border: '2px solid var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: 'var(--primary)', boxShadow: '0 0 10px var(--primary-glow)', flexShrink: 0 }}>
                                    {index + 1}
                                </div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                        <div>
                                            <h3 style={{ margin: 0, color: 'var(--text-main)' }}>{phase.name}</h3>
                                            <span style={{ fontSize: '0.7rem', color: 'var(--primary)', fontWeight: 'bold' }}>[{phase.type}]</span>
                                        </div>
                                        <div style={{ textAlign: 'right', fontSize: '0.75rem', background: 'var(--bg-body)', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border)' }}>
                                            {/* VARIABLES REALES DEL SERVICIO */}
                                            <div style={{ color: 'var(--text-muted)' }}>📅 Plan: <strong>{phase.plannedStart || 'No definido'}</strong></div>
                                            <div style={{ color: phase.hasStarted ? 'var(--success)' : 'var(--text-muted)' }}>✅ Real: <strong>{phase.actualStart || 'Pendiente'}</strong></div>
                                        </div>
                                    </div>
                                    <p style={{ margin: '10px 0 0 0', color: 'var(--text-muted)', fontSize: '0.9rem' }}>{phase.description}</p>
                                </div>
                            </div>
                            <div style={{ display: 'flex', gap: '10px', marginTop: '10px', borderTop: '1px dashed var(--border)', paddingTop: '15px' }}>
                                <button className="btn" style={{ backgroundColor: 'rgba(56, 189, 248, 0.1)', border: '1px solid var(--primary)', color: 'var(--primary)', fontSize: '0.7rem' }}>VER TAREAS_</button>
                                {/* CONTADORES REALES DEL SERVICIO */}
                                <button className="btn" style={{ backgroundColor: 'transparent', border: '1px solid var(--border)', color: 'var(--text-main)', fontSize: '0.7rem', display: 'flex', alignItems: 'center', gap: '5px' }}>📝 NOTAS ({phase.notesCount})</button>
                                <button className="btn" style={{ backgroundColor: 'transparent', border: '1px solid var(--border)', color: 'var(--text-main)', fontSize: '0.7rem', display: 'flex', alignItems: 'center', gap: '5px' }}>📎 DOCS ({phase.docsCount})</button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="card" style={{ textAlign: 'center', opacity: 0.5 }}><p style={{ color: 'var(--text-muted)' }}>No hay secuencias de fases cargadas.</p></div>
            )}
            
            {/* <ContactFormTester projectId={project.id} /> <-- Tester Día 5 */}
            
            <footer style={{ marginTop: '4rem', textAlign: 'center', opacity: 0.2, fontSize: '0.7rem' }}>PROYECTO VIT // ACCESO NIVEL 1 // {new Date().getFullYear()}</footer>
        </div>
    );
}