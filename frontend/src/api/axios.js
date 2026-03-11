import axios from 'axios';

// Creamos la instancia base. 
// Gracias a tu proxy, '/api' se redirige a tu Django en el puerto 8000.
const api = axios.create({
  baseURL: '/api',
});

// Interceptor: Antes de que cualquier petición salga hacia Django, 
// este código revisa si hay un token guardado y lo añade al encabezado.
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

export default api;