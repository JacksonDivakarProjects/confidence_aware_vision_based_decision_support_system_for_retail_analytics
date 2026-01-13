import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-icon">📊</div>
          <div className="brand-text">
            <span className="brand-title">RetailMetrics</span>
            <span className="brand-subtitle">Analytics Platform</span>
          </div>
        </div>

        <div className="navbar-links">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            <span className="nav-icon">📈</span>
            Dashboard
          </Link>
          <Link 
            to="/recommendations" 
            className={`nav-link ${location.pathname === '/recommendations' ? 'active' : ''}`}
          >
            <span className="nav-icon">🤖</span>
            AI Assistant
          </Link>
        </div>

        <div className="navbar-actions">
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
