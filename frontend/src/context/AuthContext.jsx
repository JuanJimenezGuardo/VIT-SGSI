import { useState } from 'react';
import api from '../api/axios';
import { jwtDecode } from 'jwt-decode';
import { AuthContext } from './auth-context';

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const token = localStorage.getItem('access');
        if (!token) return null;

        try {
            return jwtDecode(token);
        } catch {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            return null;
        }
    });

    const logout = () => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        setUser(null);
    };

    const loading = false;

    const login = async (username, password) => {
        try {
            const response = await api.post('/token/', { username, password });
            const { access, refresh } = response.data;

            localStorage.setItem('access', access);
            localStorage.setItem('refresh', refresh);

            const decoded = jwtDecode(access);
            setUser(decoded);
        } catch (error) {
            if (error?.response?.status === 401) {
                throw new Error('Credenciales inválidas');
            }
            throw new Error('No hay conexión con el servidor backend (puerto 8000)');
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};