import { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Credenciales inválidas');
        }
    };

    return (
        <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            
            {/* Botón flotante en la esquina superior derecha */}
            <div style={{ position: 'absolute', top: '20px', right: '20px' }}>
                <ThemeToggle />
            </div>

            <div className="card" style={{ width: '90%', maxWidth: '380px', textAlign: 'center' }}>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛰️</div>
                <h2 style={{ marginBottom: '0.5rem', letterSpacing: '1px' }}>ACCESO VIT</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem' }}>
                    Introduce tus credenciales de comando
                </p>
                
                {error && (
                    <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', padding: '10px', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.85rem' }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ textAlign: 'left' }}>
                    <div style={{ marginBottom: '1.2rem' }}>
                        <label style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>USUARIO</label>
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Tu_Usuario" required />
                    </div>
                    <div style={{ marginBottom: '2rem' }}>
                        <label style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>CONTRASEÑA</label>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>INICIAR SECUENCIA</button>
                </form>
            </div>
        </div>
    );
}