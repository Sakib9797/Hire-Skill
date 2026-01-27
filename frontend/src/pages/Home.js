import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%)',
      padding: 'var(--spacing-xl)',
      textAlign: 'center',
      color: 'white'
    }}>
      <h1 style={{ fontSize: '3.5rem', marginBottom: 'var(--spacing-md)', fontWeight: 700 }}>
        Welcome to HireSkill
      </h1>
      <p style={{ fontSize: '1.5rem', marginBottom: 'var(--spacing-2xl)', maxWidth: '600px', opacity: 0.9 }}>
        Connect talented professionals with amazing opportunities. Build your profile, showcase your skills, and find your dream job.
      </p>
      <div style={{ display: 'flex', gap: 'var(--spacing-lg)' }}>
        <Link to="/register" className="btn btn-primary" style={{
          background: 'white',
          color: 'var(--primary-color)',
          fontSize: '1.1rem',
          padding: '1rem 2rem'
        }}>
          Get Started
        </Link>
        <Link to="/login" className="btn btn-secondary" style={{
          background: 'transparent',
          color: 'white',
          border: '2px solid white',
          fontSize: '1.1rem',
          padding: '1rem 2rem'
        }}>
          Sign In
        </Link>
      </div>
      
      <div style={{
        marginTop: 'var(--spacing-2xl)',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: 'var(--spacing-xl)',
        maxWidth: '900px',
        width: '100%'
      }}>
        <div style={{
          background: 'rgba(255, 255, 255, 0.1)',
          padding: 'var(--spacing-xl)',
          borderRadius: 'var(--radius-lg)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: 'var(--spacing-md)' }}>🔐</div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: 'var(--spacing-sm)' }}>Secure Authentication</h3>
          <p style={{ opacity: 0.9 }}>JWT-based authentication with password encryption</p>
        </div>
        
        <div style={{
          background: 'rgba(255, 255, 255, 0.1)',
          padding: 'var(--spacing-xl)',
          borderRadius: 'var(--radius-lg)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: 'var(--spacing-md)' }}>👤</div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: 'var(--spacing-sm)' }}>Rich Profiles</h3>
          <p style={{ opacity: 0.9 }}>Showcase your skills, experience, and interests</p>
        </div>
        
        <div style={{
          background: 'rgba(255, 255, 255, 0.1)',
          padding: 'var(--spacing-xl)',
          borderRadius: 'var(--radius-lg)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: 'var(--spacing-md)' }}>🎨</div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: 'var(--spacing-sm)' }}>Custom Themes</h3>
          <p style={{ opacity: 0.9 }}>Switch between light and dark modes</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
