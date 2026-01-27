import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import '../styles/Dashboard.css';

const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getInitials = () => {
    if (user?.first_name && user?.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
    }
    return user?.email?.[0]?.toUpperCase() || 'U';
  };

  return (
    <nav className="navbar">
      <a href="/dashboard" className="navbar-brand">
        HireSkill
      </a>
      
      <div className="navbar-links">
        <button 
          className="nav-link" 
          onClick={() => navigate('/dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className="nav-link" 
          onClick={() => navigate('/career-recommendations')}
        >
          🤖 Career AI
        </button>
      </div>
      
      <div className="navbar-menu">
        <button
          className="theme-toggle"
          onClick={toggleTheme}
          aria-label="Toggle theme"
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
        
        <div className="navbar-user">
          <div className="user-avatar" title={user?.email}>
            {getInitials()}
          </div>
          <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>
            {user?.first_name || user?.email}
          </span>
        </div>
        
        <button className="btn btn-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
