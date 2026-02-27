import React, { useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Landing.css';

const FEATURES = [
  { icon: '🔍', title: 'Smart Job Search', desc: 'Aggregate postings from LinkedIn, Indeed, RemoteOK, and 4 more sources in one click.' },
  { icon: '🤖', title: 'AI Career Guidance', desc: 'Get personalized career recommendations powered by NLP and your unique skill profile.' },
  { icon: '✉️', title: 'Cover Letters', desc: 'Generate polished, role-specific cover letters with a single prompt.' },
  { icon: '💰', title: 'Salary Predictor', desc: 'ML-powered salary estimates based on role, experience, and location.' },
  { icon: '🎯', title: 'Interview Prep', desc: 'Custom questions and model answers tailored to any job description.' },
  { icon: '🗺️', title: 'Career Path Map', desc: 'Interactive visualization of tech career paths, transitions, and skill overlaps.' },
];

const Home = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const heroRef = useRef(null);

  useEffect(() => {
    if (user) navigate('/home', { replace: true });
  }, [user, navigate]);

  /* Parallax on mouse move */
  useEffect(() => {
    const hero = heroRef.current;
    if (!hero) return;
    const handleMove = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 20;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      hero.style.setProperty('--mx', `${x}px`);
      hero.style.setProperty('--my', `${y}px`);
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return (
    <div className="landing">
      {/* ── HERO ── */}
      <section className="ld-hero" ref={heroRef}>
        {/* floating shapes */}
        <div className="ld-shapes" aria-hidden="true">
          <div className="ld-shape ld-shape--1" />
          <div className="ld-shape ld-shape--2" />
          <div className="ld-shape ld-shape--3" />
          <div className="ld-shape ld-shape--4" />
        </div>

        <div className="ld-hero__inner">
          <span className="ld-hero__badge">AI-Powered Career Platform</span>
          <h1 className="ld-hero__title">
            Land Your Dream Job<br />
            <span className="ld-hero__gradient">With Intelligent Tools</span>
          </h1>
          <p className="ld-hero__sub">
            From smart job search to AI cover letters, salary predictions, and interview prep — HireSkill equips you with everything to accelerate your career.
          </p>
          <div className="ld-hero__btns">
            <Link to="/register" className="ld-btn ld-btn--primary">
              Get Started Free
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </Link>
            <Link to="/login" className="ld-btn ld-btn--ghost">
              Sign In
            </Link>
          </div>
        </div>

        {/* scroll indicator */}
        <div className="ld-scroll-hint">
          <div className="ld-scroll-hint__dot" />
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section className="ld-features">
        <div className="ld-features__hdr">
          <span className="ld-features__badge">Features</span>
          <h2 className="ld-features__title">Built for Job Seekers</h2>
          <p className="ld-features__sub">Everything you need to stand out, all in one place.</p>
        </div>
        <div className="ld-features__grid">
          {FEATURES.map((f, i) => (
            <div key={i} className="ld-fcard" style={{ animationDelay: `${i * 0.08}s` }}>
              <div className="ld-fcard__icon">{f.icon}</div>
              <h3 className="ld-fcard__title">{f.title}</h3>
              <p className="ld-fcard__desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="ld-cta">
        <h2 className="ld-cta__title">Ready to Transform Your Career?</h2>
        <p className="ld-cta__sub">Join HireSkill today — it's free, fast, and powered by AI.</p>
        <Link to="/register" className="ld-btn ld-btn--primary ld-btn--lg">
          Create Free Account
        </Link>
      </section>

      {/* ── FOOTER ── */}
      <footer className="ld-footer">
        <span className="ld-footer__brand">HireSkill</span>
        <span className="ld-footer__dot">·</span>
        <span>AI-powered career companion</span>
      </footer>
    </div>
  );
};

export default Home;
