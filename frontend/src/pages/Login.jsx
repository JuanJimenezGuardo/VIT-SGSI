import { useState, useContext } from 'react';
import { AuthContext } from '../context/auth-context';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSubmitting(true);
        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            setError(err?.message || 'Error al iniciar sesión');
        } finally {
            setSubmitting(false);
        }
    };

    // En tu return de Login.jsx
return (
    <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center' }}>
        <div className="card" style={{ width: '90%', maxWidth: '380px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛰️</div>
            <h2 style={{ marginBottom: '0.5rem', letterSpacing: '1px' }}>ACCESO VIT</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem' }}>Introduce tus credenciales de comando</p>
            
            <form onSubmit={handleSubmit} style={{ textAlign: 'left' }} autoComplete="off">
                <div style={{ marginBottom: '1.2rem' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>USUARIO</label>
                    <input type="text" name="vit_username" autoComplete="new-username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="tu_usuario" required />
                </div>
                <div style={{ marginBottom: '2rem' }}>
                    <label style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>CONTRASEÑA</label>
                    <input type="password" name="vit_password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required />
                </div>
                {error && (
                    <p style={{ color: '#ff7b7b', fontSize: '0.85rem', marginBottom: '1rem' }}>
                        {error}
                    </p>
                )}
                <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={submitting}>
                    {submitting ? 'VALIDANDO...' : 'INICIAR SECUENCIA'}
                </button>
            </form>
        </div>
    </div>
);
}