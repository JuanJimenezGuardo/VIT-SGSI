import { useState } from 'react';
import api from '../api/axios';

export default function ContactFormTester({ projectId }) {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        role: 'LEAD'
    });
    const [log, setLog] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleTestSubmit = async (e) => {
        e.preventDefault();
        setLog('Enviando petición POST...');

        try {
            // 1. Intentamos crear el contacto (Osky debe tener listo /api/contacts/)
            const contactRes = await api.post('/contacts/', {
                name: formData.name,
                email: formData.email,
                phone: formData.phone
            });
            
            const newContactId = contactRes.data.id;
            setLog(prev => prev + `\n✅ Contacto creado con ID: ${newContactId}`);

            // 2. Intentamos vincularlo al proyecto
            const linkRes = await api.post('/project-contacts/', {
                project: projectId,
                contact: newContactId,
                role: formData.role
            });

            setLog(prev => prev + `\n✅ Contacto vinculado exitosamente!`);

        } catch (error) {
            // Aquí capturamos si Osky nos manda un 400, 401, 403 o 500
            if (error.response) {
                setLog(prev => prev + `\n❌ ERROR ${error.response.status}: ${JSON.stringify(error.response.data, null, 2)}`);
            } else {
                setLog(prev => prev + `\n❌ ERROR DE RED: El servidor no responde.`);
            }
        }
    };

    // Botones para autocompletar datos "malos" y probar validaciones
    const fillBadData = () => {
        setFormData({ name: '', email: 'correo-invalido', phone: '123', role: 'ROL_INVENTADO' });
    };

    return (
        <div className="card" style={{ border: '1px dashed var(--primary)', marginTop: '2rem' }}>
            <h3 style={{ color: 'var(--accent)', marginTop: 0 }}>🧪 Tester de API (Día 5)</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Usa este formulario para enviar payloads al backend y probar las validaciones de Osky.
            </p>

            <form onSubmit={handleTestSubmit} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '1rem' }}>
                <input type="text" name="name" placeholder="Nombre" value={formData.name} onChange={handleChange} style={{ flex: 1, minWidth: '150px' }} />
                <input type="text" name="email" placeholder="Email" value={formData.email} onChange={handleChange} style={{ flex: 1, minWidth: '150px' }} />
                <select name="role" value={formData.role} onChange={handleChange} style={{ flex: 1, minWidth: '150px' }}>
                    <option value="LEAD">Líder (LEAD)</option>
                    <option value="AUDITOR">Auditor (AUDITOR)</option>
                    <option value="ROL_INVENTADO">Rol Inválido (Para testear 400)</option>
                </select>
                <button type="submit" className="btn btn-primary">ENVIAR PAYLOAD</button>
            </form>

            <button onClick={fillBadData} className="btn" style={{ fontSize: '0.7rem', background: 'var(--bg-body)', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                💥 Llenar con datos inválidos (Test 400)
            </button>

            <pre style={{ background: '#000', color: '#0f0', padding: '10px', borderRadius: '5px', fontSize: '0.8rem', minHeight: '80px', whiteSpace: 'pre-wrap' }}>
                {log || '> Esperando acción...'}
            </pre>
        </div>
    );
}