import React from 'react';
import { useTheme } from '../context/ThemeContext';

const ThemeToggle = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <button 
      onClick={toggleTheme}
      className="theme-toggle"
      aria-label="Toggle theme"
      style={{
        background: isDark ? 'var(--bg-tertiary)' : 'var(--bg-tertiary)',
        border: '2px solid var(--border-color)',
        borderRadius: 'var(--border-radius-xl)',
        padding: '8px 16px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '1.25rem',
        transition: 'all var(--transition-fast)',
        color: 'var(--text-primary)',
        fontWeight: '500',
        boxShadow: 'var(--shadow-sm)'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'scale(1.05)';
        e.currentTarget.style.boxShadow = 'var(--shadow-md)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'scale(1)';
        e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
      }}
    >
      <span>{isDark ? '🌙' : '☀️'}</span>
    </button>
  );
};

export default ThemeToggle;
