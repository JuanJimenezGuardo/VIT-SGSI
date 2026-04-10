import { createContext, useState, useEffect } from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    // Busca si ya hay un tema guardado, si no, usa 'dark' por defecto
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

    // Cada vez que el tema cambia, inyecta el atributo en el HTML y guárdalo
    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};