import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import userService from '../services/userService';
import '../styles/HomePage.css';

const FEATURES = [
  {
    id: 'jobs',
    icon: '🔍',
    title: 'Job Search',
    subtitle: 'Find Your Next Role',
    description: 'Browse thousands of live job postings from LinkedIn, Indeed, RemoteOK, and more — all in one place.',
    cta: 'Search Jobs',
    path: '/job-search',
    color: '#0066cc',
    gradient: 'linear-gradient(135deg, #0066cc 0%, #0099ff 100%)',
    bg: '#e6f2ff',
    stats: 'Live from 4 sources',
  },
  {
    id: 'career',
    icon: '🤖',
    title: 'Career AI',
    subtitle: 'Get Personalized Guidance',
    description: 'AI-powered career recommendations tailored to your skills, experience, and interests.',
    cta: 'Explore Careers',
    path: '/career-recommendations',
    color: '#7c3aed',
    gradient: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
    bg: '#f3e8ff',
    stats: 'Powered by NLP',
  },
  {
    id: 'cover',
    icon: '✉️',
    title: 'Cover Letter',
    subtitle: 'Make a Great First Impression',
    description: 'Generate a compelling, personalized cover letter powered by AI for any job you apply to.',
    cta: 'Write Cover Letter',
    path: '/cover-letter-generator',
    color: '#d97706',
    gradient: 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
    bg: '#fef3c7',
    stats: 'AI-generated',
  },
  {
    id: 'profile',
    icon: '👤',
    title: 'My Profile',
    subtitle: 'Manage Your Information',
    description: 'Update your skills, experience, location, and career interests to get better recommendations.',
    cta: 'View Profile',
    path: '/dashboard',
    color: '#0891b2',
    gradient: 'linear-gradient(135deg, #0891b2 0%, #06b6d4 100%)',
    bg: '#cffafe',
    stats: 'Always up to date',
  },
  {
    id: 'salary',
    icon: '💰',
    title: 'Salary Predictor',
    subtitle: 'Know Your Market Worth',
    description: 'Get an AI-powered salary estimate based on your role, skills, experience, and location type.',
    cta: 'Predict Salary',
    path: '/salary-predictor',
    color: '#16a34a',
    gradient: 'linear-gradient(135deg, #16a34a 0%, #22c55e 100%)',
    bg: '#dcfce7',
    stats: 'ML-powered model',
  },
  {
    id: 'interview',
    icon: '🎯',
    title: 'Interview Prep',
    subtitle: 'Ace Your Next Interview',
    description: 'Generate custom interview questions with model answers tailored to any role and job description.',
    cta: 'Prepare Now',
    path: '/interview-prep',
    color: '#b45309',
    gradient: 'linear-gradient(135deg, #b45309 0%, #f59e0b 100%)',
    bg: '#fef9c3',
    stats: 'AI question bank',
  },
  {
    id: 'career-path',
    icon: '🗺️',
    title: 'Career Path',
    subtitle: 'Visualize Your Journey',
    description: 'Explore an interactive graph of tech career paths, skill overlaps, and role transitions.',
    cta: 'Explore Paths',
    path: '/career-path',
    color: '#7c3aed',
    gradient: 'linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%)',
    bg: '#ede9fe',
    stats: 'Interactive graph',
  },
];

const TIPS = [
  'A resume with 20+ matching keywords sees 3× more interview calls.',
  'Tailoring your cover letter to each role increases callbacks by 50%.',
  'Remote roles often receive 200+ applications — stand out with a great ATS score.',
  'Updating your skills profile monthly improves AI match accuracy significantly.',
  'Applying within the first 24 hours of a job posting boosts your chances.',
];

const getGreeting = () => {
  const h = new Date().getHours();
  if (h < 12) return 'Good morning';
  if (h < 17) return 'Good afternoon';
  return 'Good evening';
};

const FeatureCard = ({ feature, index, onClick }) => {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      className={`feature-card feature-card--${feature.id}`}
      style={{ '--card-color': feature.color, '--card-bg': feature.bg, '--card-gradient': feature.gradient, animationDelay: `${index * 0.08}s` }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={onClick}
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick()}
      role="button"
      aria-label={`Navigate to ${feature.title}`}
    >
      <div className="feature-card__glow" />
      <div className="feature-card__icon-wrap">
        <span className="feature-card__icon">{feature.icon}</span>
      </div>
      <div className="feature-card__body">
        <p className="feature-card__subtitle">{feature.subtitle}</p>
        <h3 className="feature-card__title">{feature.title}</h3>
        <p className="feature-card__desc">{feature.description}</p>
        <div className="feature-card__footer">
          <span className="feature-card__stats-pill">{feature.stats}</span>
          <button className="feature-card__cta">
            {feature.cta}
            <span className="feature-card__arrow">{hovered ? '→' : '›'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

const StatBubble = ({ icon, value, label, delay }) => (
  <div className="stat-bubble" style={{ animationDelay: delay }}>
    <span className="stat-bubble__icon">{icon}</span>
    <span className="stat-bubble__value">{value}</span>
    <span className="stat-bubble__label">{label}</span>
  </div>
);

const HomePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [tipIndex, setTipIndex] = useState(0);
  const [tipVisible, setTipVisible] = useState(true);

  useEffect(() => {
    userService.getProfile().then(setProfile).catch(() => {});
  }, []);

  // Rotate tips every 6 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setTipVisible(false);
      setTimeout(() => {
        setTipIndex(i => (i + 1) % TIPS.length);
        setTipVisible(true);
      }, 400);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const firstName = profile?.first_name || user?.first_name || user?.email?.split('@')[0] || 'there';
  const skillCount = profile?.profile?.skills?.length ?? 0;
  const interestCount = profile?.profile?.interests?.length ?? 0;

  return (
    <div className="homepage">
      <Navbar />

      {/* ── Hero ── */}
      <section className="hp-hero">
        <div className="hp-hero__particles">
          {[...Array(18)].map((_, i) => (
            <span key={i} className="particle" style={{ '--i': i }} />
          ))}
        </div>
        <div className="hp-hero__content">
          <p className="hp-hero__greeting">{getGreeting()},</p>
          <h1 className="hp-hero__name">{firstName} 👋</h1>
          <p className="hp-hero__tagline">
            Your career toolkit is ready. Where do you want to go today?
          </p>
          <div className="hp-hero__actions">
            <button className="hp-btn hp-btn--primary" onClick={() => navigate('/job-search')}>
              🔍 Search Jobs Now
            </button>
            <button className="hp-btn hp-btn--ghost" onClick={() => navigate('/career-recommendations')}>
              🤖 Get AI Guidance
            </button>
          </div>
        </div>

        {/* Floating stat pills */}
        <div className="hp-hero__stats">
          <StatBubble icon="🛠️" value={skillCount || '—'} label="Skills Listed" delay="0s" />
          <StatBubble icon="🎯" value={interestCount || '—'} label="Interests" delay="0.1s" />
          <StatBubble icon="⚡" value="Live" label="Job Feeds" delay="0.2s" />
          <StatBubble icon="🤖" value="AI" label="Powered" delay="0.3s" />
        </div>
      </section>

      {/* ── Feature Cards ── */}
      <section className="hp-features">
        <div className="hp-section-header">
          <h2 className="hp-section-title">Everything You Need</h2>
          <p className="hp-section-sub">Pick a tool and get started in seconds</p>
        </div>
        <div className="hp-features__grid">
          {FEATURES.map((f, i) => (
            <FeatureCard
              key={f.id}
              feature={f}
              index={i}
              onClick={() => navigate(f.path)}
            />
          ))}
        </div>
      </section>

      {/* ── Quick Actions strip ── */}
      <section className="hp-quickbar">
        <p className="hp-quickbar__label">Quick actions</p>
        <div className="hp-quickbar__pills">
          {FEATURES.map(f => (
            <button
              key={f.id}
              className="hp-pill"
              style={{ '--pill-color': f.color }}
              onClick={() => navigate(f.path)}
            >
              {f.icon} {f.cta}
            </button>
          ))}
        </div>
      </section>

      {/* ── Tip Banner ── */}
      <section className="hp-tip">
        <div className={`hp-tip__inner ${tipVisible ? 'hp-tip--in' : 'hp-tip--out'}`}>
          <span className="hp-tip__icon">💡</span>
          <p className="hp-tip__text">{TIPS[tipIndex]}</p>
          <div className="hp-tip__dots">
            {TIPS.map((_, i) => (
              <span key={i} className={`hp-tip__dot ${i === tipIndex ? 'active' : ''}`} />
            ))}
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="hp-footer">
        <span className="hp-footer__brand">HireSkill</span>
        <span className="hp-footer__sep">·</span>
        <span className="hp-footer__copy">Your AI-powered career companion</span>
      </footer>
    </div>
  );
};

export default HomePage;
