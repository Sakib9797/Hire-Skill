import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
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
            <h1 style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>😵</h1>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.75rem' }}>
              Something went wrong
            </h2>
            <p style={{ color: 'var(--text-secondary, #64748b)', marginBottom: '1.5rem' }}>
              An unexpected error occurred. Please refresh the page or try again later.
            </p>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: '10px 28px',
                borderRadius: 8,
                border: 'none',
                background: '#4f46e5',
                color: '#fff',
                fontWeight: 600,
                fontSize: '0.95rem',
                cursor: 'pointer',
              }}
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
