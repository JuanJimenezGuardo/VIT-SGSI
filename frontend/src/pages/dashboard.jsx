import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../context/auth-context';
import api from '../api/axios';
import { useNavigate, Link } from 'react-router-dom';

export default function Dashboard() {
    const { user, logout } = useContext(AuthContext);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                // Petición a tu backend de Django
                const response = await api.get('/projects/');
                
                // Manejamos si la respuesta viene paginada (results) o como lista simple
                const data = response.data.results ? response.data.results : response.data;
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

    if (loading) {
        return (
            <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}>
                <div className="badge">Sincronizando con el servidor...</div>
            </div>
        );
    }

    return (
        <div className="container">
            {/* Encabezado Estilo Terminal */}
            <header style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                marginBottom: '4rem',
                borderBottom: '1px solid var(--border)',
                paddingBottom: '1rem'
            }}>
                <div>
                    <h1 style={{ 
                        margin: 0, 
                        fontSize: '2.2rem', 
                        fontWeight: '800',
                        background: 'linear-gradient(to right, #38bdf8, #818cf8)', 
                        WebkitBackgroundClip: 'text', 
                        WebkitTextFillColor: 'transparent' 
                    }}>
                        CORE VIT
                    </h1>
                    <div style={{ display: 'flex', gap: '15px', marginTop: '5px' }}>
                        <code style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                            USER_AUTH_ID: {user?.user_id || 'UNKNOWN'}
                        </code>
                        <code style={{ color: 'var(--primary)', fontSize: '0.8rem' }}>
                            STATUS: EN LÍNEA
                        </code>
                    </div>
                </div>
                
                <button onClick={handleLogout} className="btn btn-danger">
                    TERMINAR SESIÓN
                </button>
            </header>

            {/* Grid de Proyectos / Módulos */}
            <h2 style={{ marginBottom: '2rem', fontSize: '1.2rem', color: 'var(--text-muted)', letterSpacing: '2px' }}>
                MÓDULOS ACTIVOS
            </h2>

            {projects.length > 0 ? (
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', 
                    gap: '2rem' 
                }}>
                    {projects.map(project => (
                        <div key={project.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <span className="badge">
                                        {project.status === 'ACTIVE' ? '● ACTIVO' : '○ PAUSADO'}
                                    </span>
                                    <div style={{ fontSize: '1.5rem', opacity: '0.7' }}>📡</div>
                                </div>
                                
                                <h3 style={{ margin: '1.5rem 0 0.5rem 0', fontSize: '1.4rem', fontWeight: '700' }}>
                                    {project.name}
                                </h3>
                                
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem', lineHeight: '1.5' }}>
                                    CLIENTE: {project.company_name}<br />
                                    ID_REF: #{project.id.toString().padStart(4, '0')}
                                </p>
                            </div>

                            <Link 
                                to={`/project/${project.id}`} 
                                className="btn btn-primary" 
                                style={{ textDecoration: 'none', textAlign: 'center' }}
                            >
                                ACCEDER AL SISTEMA
                            </Link>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ color: 'var(--text-muted)' }}>No se encontraron bases de datos de proyectos vinculadas a este perfil.</p>
                </div>
            )}

            {/* Footer Informativo */}
            <footer style={{ marginTop: '5rem', textAlign: 'center', opacity: '0.3', fontSize: '0.7rem' }}>
                <p>VIT SYSTEM v3.0 // 2026 // ENCRIPTACIÓN JWT AES-256</p>
            </footer>
        </div>
    );
}