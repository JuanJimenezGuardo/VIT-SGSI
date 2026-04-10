import axios from 'axios';

// Creamos la instancia base [cite: 368]
const api = axios.create({
  baseURL: '/api',
});

// Interceptor de PETICIONES: Agrega el token si existe [cite: 369, 370]
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// NUEVO - Interceptor de RESPUESTAS: Captura los errores globalmente para el Día 4
api.interceptors.response.use(
  (response) => {
    // Si todo sale bien (200, 201, 204), simplemente devuelve la respuesta
    return response;
  },
  (error) => {
    // Si el backend nos manda un error, lo atrapamos aquí
    if (error.response) {
      const status = error.response.status;

      if (status === 400) {
        console.warn('⚠️ [API 400] Error de validación en los datos enviados:', error.response.data);
      } else if (status === 401) {
        console.error('🔒 [API 401] Sesión expirada o no autorizada.');
        // Aquí podrías agregar lógica para forzar un logout automático
      } else if (status === 403) {
        console.error('⛔ [API 403] No tienes permisos para esta acción.');
      } else if (status >= 500) {
        console.error('🔥 [API 500] Error interno del servidor backend.');
      }
    } else if (error.request) {
      console.error('🔌 [API ERROR] No hubo respuesta del servidor. ¿Está encendido Django?');
    }
    
    return Promise.reject(error);
  }
);

export default api; // [cite: 371]