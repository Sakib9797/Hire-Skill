import React from 'react';
import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--bg-primary, #f8fafc)',
      color: 'var(--text-primary, #1e293b)',
      padding: '2rem',
      textAlign: 'center',
    }}>
      <div style={{ maxWidth: 480 }}>
        <h1 style={{ fontSize: '5rem', fontWeight: 800, margin: 0, color: '#4f46e5' }}>404</h1>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.75rem' }}>
          Page Not Found
        </h2>
        <p style={{ color: 'var(--text-secondary, #64748b)', marginBottom: '1.5rem' }}>
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link
          to="/"
          style={{
            display: 'inline-block',
            padding: '10px 28px',
            borderRadius: 8,
            background: '#4f46e5',
            color: '#fff',
            fontWeight: 600,
            fontSize: '0.95rem',
            textDecoration: 'none',
          }}
        >
          Back to Home
        </Link>
      </div>
    </div>
  );
}

export default NotFound;
