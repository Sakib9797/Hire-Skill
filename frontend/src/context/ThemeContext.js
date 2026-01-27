import React, { createContext, useState, useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';

const ThemeContext = createContext(null);

export const ThemeProvider = ({ children }) => {
  const { user } = useAuth();
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Load theme from user profile or localStorage
    const savedTheme = user?.profile?.theme_preference || localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, [user]);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    return newTheme;
  };

  const value = {
    theme,
    toggleTheme,
    isDark: theme === 'dark',
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
