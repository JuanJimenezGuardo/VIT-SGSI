import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProjectDetail from './pages/ProjectDetail'; // Importamos la nueva página de detalles

// Componente para proteger las rutas privadas
const PrivateRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  
  if (loading) return <div style={{ padding: '20px' }}>Cargando sesión...</div>;
  
  // Si hay usuario, muestra la página; si no, mándalo al login [cite: 96, 97, 218]
  return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta pública para el inicio de sesión [cite: 222, 256] */}
        <Route path="/login" element={<Login />} />
        
        {/* Ruta protegida para el panel principal [cite: 98, 256] */}
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />

        {/* Nueva ruta protegida para ver el detalle de un proyecto específico [cite: 99, 256] */}
        <Route path="/project/:id" element={
          <PrivateRoute>
            <ProjectDetail />
          </PrivateRoute>
        } />
        
        {/* Redirección automática si la ruta no existe  */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;