import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';
import { projectService } from '../services/projectService'; // <-- Importamos el servicio

export default function Dashboard() {
    const { user, logout } = useContext(AuthContext);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                // Ahora usamos el servicio limpio
                const data = await projectService.getAllProjects();
                setProjects(data);
            } catch (error) {
                console.error("Error al cargar módulos de proyectos:", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchProjects();
        }
    }, [user]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (loading) return (
        <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}>
            <div className="badge">Sincronizando con el servidor...</div>
        </div>
    );

    return (
        <div className="container">
            {/* Encabezado */}
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
                <div>
                    <h1 style={{ margin: 0, fontSize: '2.2rem', fontWeight: '800', background: 'linear-gradient(to right, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                        CORE VIT
                    </h1>
                    <div style={{ display: 'flex', gap: '15px', marginTop: '5px' }}>
                        <code style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>USER_AUTH_ID: {user?.user_id || 'UNKNOWN'}</code>
                        <code style={{ color: 'var(--primary)', fontSize: '0.8rem' }}>STATUS: EN LÍNEA</code>
                    </div>
                </div>
                
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <ThemeToggle />
                    <button onClick={handleLogout} className="btn btn-danger">TERMINAR SESIÓN</button>
                </div>
            </header>

            <h2 style={{ marginBottom: '2rem', fontSize: '1.2rem', color: 'var(--text-muted)', letterSpacing: '2px' }}>MÓDULOS ACTIVOS</h2>

            {projects.length > 0 ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '2rem' }}>
                    {projects.map(project => (
                        <div key={project.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    {/* Usamos el mapeo isActive */}
                                    <span className="badge">{project.isActive ? '● ACTIVO' : '○ PAUSADO'}</span>
                                    <div style={{ fontSize: '1.5rem', opacity: '0.7' }}>📡</div>
                                </div>
                                <h3 style={{ margin: '1.5rem 0 0.5rem 0', fontSize: '1.4rem', fontWeight: '700' }}>{project.name}</h3>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem', lineHeight: '1.5' }}>
                                    {/* Usamos el mapeo clientName */}
                                    CLIENTE: {project.clientName}<br />
                                    ID_REF: #{project.id.toString().padStart(4, '0')}
                                </p>
                            </div>
                            <Link to={`/project/${project.id}`} className="btn btn-primary" style={{ textDecoration: 'none', textAlign: 'center' }}>
                                ACCEDER AL SISTEMA
                            </Link>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}><p style={{ color: 'var(--text-muted)' }}>No se encontraron bases de datos.</p></div>
            )}
            <footer style={{ marginTop: '5rem', textAlign: 'center', opacity: '0.3', fontSize: '0.7rem' }}><p>VIT SYSTEM v3.0 // 2026</p></footer>
        </div>
    );
}