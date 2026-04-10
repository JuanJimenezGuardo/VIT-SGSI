import { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';

export default function ThemeToggle() {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <button 
            onClick={toggleTheme}
            style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border)',
                color: 'var(--text-main)',
                padding: '8px 12px',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: 'bold',
                transition: 'all 0.2s ease',
                boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
            }}
        >
            {theme === 'dark' ? '☀️ ' : '🌙 '}
        </button>
    );
}