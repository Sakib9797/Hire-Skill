import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import userService from '../services/userService';
import '../styles/HomePage.css';

/* ──────────────────────────────────────────────
   DATA
────────────────────────────────────────────── */
const FEATURES = [
  {
    id: 'jobs',
    icon: '🔍',
    title: 'Job Search',
    subtitle: 'Find Your Next Role',
    description: 'Browse thousands of live postings from LinkedIn, Indeed, RemoteOK, and more.',
    cta: 'Search Jobs',
    path: '/job-search',
    color: '#3b82f6',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)',
    bg: 'rgba(59,130,246,0.10)',
  },
  {
    id: 'career',
    icon: '🤖',
    title: 'Career AI',
    subtitle: 'Personalized Guidance',
    description: 'AI-powered career recommendations tailored to your skills and interests.',
    cta: 'Explore Careers',
    path: '/career-recommendations',
    color: '#8b5cf6',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
    bg: 'rgba(139,92,246,0.10)',
  },
  {
    id: 'cover',
    icon: '✉️',
    title: 'Cover Letter',
    subtitle: 'Great First Impression',
    description: 'Generate compelling, personalized cover letters powered by AI.',
    cta: 'Write Letter',
    path: '/cover-letter-generator',
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
    bg: 'rgba(245,158,11,0.10)',
  },
  {
    id: 'salary',
    icon: '💰',
    title: 'Salary Predictor',
    subtitle: 'Know Your Worth',
    description: 'Get an ML-powered salary estimate based on role, skills, and experience.',
    cta: 'Predict Salary',
    path: '/salary-predictor',
    color: '#10b981',
    gradient: 'linear-gradient(135deg, #10b981 0%, #34d399 100%)',
    bg: 'rgba(16,185,129,0.10)',
  },
  {
    id: 'interview',
    icon: '🎯',
    title: 'Interview Prep',
    subtitle: 'Ace Every Interview',
    description: 'Custom interview questions with model answers for any role.',
    cta: 'Start Prep',
    path: '/interview-prep',
    color: '#ef4444',
    gradient: 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)',
    bg: 'rgba(239,68,68,0.10)',
  },
  {
    id: 'career-path',
    icon: '🗺️',
    title: 'Career Path',
    subtitle: 'Visualize Your Journey',
    description: 'Interactive graph of career paths, skill overlaps, and transitions.',
    cta: 'Explore Paths',
    path: '/career-path',
    color: '#06b6d4',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%)',
    bg: 'rgba(6,182,212,0.10)',
  },
  {
    id: 'profile',
    icon: '👤',
    title: 'My Profile',
    subtitle: 'Manage Your Info',
    description: 'Update your skills, experience, and career interests.',
    cta: 'View Profile',
    path: '/dashboard',
    color: '#ec4899',
    gradient: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
    bg: 'rgba(236,72,153,0.10)',
  },
];

const TIPS = [
  'Tailoring your cover letter to each role increases callbacks by 50%.',
  'A resume with 20+ matching keywords sees 3× more interview calls.',
  'Remote roles often receive 200+ applications — stand out with a great ATS score.',
  'Updating your skills profile monthly improves AI match accuracy.',
  'Applying within the first 24 hours of a job posting boosts your chances.',
];

const getGreeting = () => {
  const h = new Date().getHours();
  if (h < 12) return 'Good morning';
  if (h < 17) return 'Good afternoon';
  return 'Good evening';
};

/* ──────────────────────────────────────────────
   ANIMATED BACKGROUND – Floating Orbs
────────────────────────────────────────────── */
const HeroCanvas = () => {
  const canvasRef = useRef(null);
  const orbsRef = useRef([]);
  const animRef = useRef(null);
  const mouseRef = useRef({ x: -9999, y: -9999 });

  const initOrbs = useCallback((w, h) => {
    const colors = [
      'rgba(59,130,246,0.28)',
      'rgba(139,92,246,0.22)',
      'rgba(16,185,129,0.18)',
      'rgba(236,72,153,0.16)',
      'rgba(245,158,11,0.14)',
      'rgba(6,182,212,0.18)',
    ];
    return Array.from({ length: 8 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 100 + Math.random() * 220,
      dx: (Math.random() - 0.5) * 0.35,
      dy: (Math.random() - 0.5) * 0.35,
      color: colors[i % colors.length],
    }));
  }, []);

  useEffect(() => {
    const cvs = canvasRef.current;
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    let w = (cvs.width = cvs.parentElement.offsetWidth);
    let h = (cvs.height = cvs.parentElement.offsetHeight);
    orbsRef.current = initOrbs(w, h);

    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      for (const o of orbsRef.current) {
        const ddx = o.x - mouseRef.current.x;
        const ddy = o.y - mouseRef.current.y;
        const dist = Math.sqrt(ddx * ddx + ddy * ddy) || 1;
        if (dist < 280) {
          o.x += (ddx / dist) * 0.5;
          o.y += (ddy / dist) * 0.5;
        }
        o.x += o.dx;
        o.y += o.dy;
        if (o.x < -o.r) o.x = w + o.r;
        if (o.x > w + o.r) o.x = -o.r;
        if (o.y < -o.r) o.y = h + o.r;
        if (o.y > h + o.r) o.y = -o.r;

        const grad = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
        grad.addColorStop(0, o.color);
        grad.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.fill();
      }
      animRef.current = requestAnimationFrame(draw);
    };
    draw();

    const handleResize = () => {
      w = cvs.width = cvs.parentElement.offsetWidth;
      h = cvs.height = cvs.parentElement.offsetHeight;
    };
    const handleMouse = (e) => {
      const rect = cvs.getBoundingClientRect();
      mouseRef.current = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    };

    window.addEventListener('resize', handleResize);
    cvs.addEventListener('mousemove', handleMouse);
    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener('resize', handleResize);
      cvs.removeEventListener('mousemove', handleMouse);
    };
  }, [initOrbs]);

  return <canvas ref={canvasRef} className="hp-hero-canvas" />;
};

/* ──────────────────────────────────────────────
   FEATURE CARD (IntersectionObserver reveal)
────────────────────────────────────────────── */
const FeatureCard = ({ feature, index, onClick }) => {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); obs.disconnect(); } },
      { threshold: 0.12 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`fc ${visible ? 'fc--visible' : ''}`}
      style={{ '--fc-color': feature.color, '--fc-bg': feature.bg, '--fc-grad': feature.gradient, '--fc-i': index }}
      onClick={onClick}
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      role="button"
      aria-label={`Go to ${feature.title}`}
    >
      <div className="fc__shine" />
      <div className="fc__icon">{feature.icon}</div>
      <div className="fc__body">
        <span className="fc__sub">{feature.subtitle}</span>
        <h3 className="fc__title">{feature.title}</h3>
        <p className="fc__desc">{feature.description}</p>
      </div>
      <div className="fc__foot">
        <span className="fc__cta">
          {feature.cta} <span className="fc__arrow">→</span>
        </span>
      </div>
    </div>
  );
};

/* ──────────────────────────────────────────────
   ANIMATED NUMBER
────────────────────────────────────────────── */
const AnimatedNumber = ({ target, suffix = '', duration = 1400 }) => {
  const [val, setVal] = useState(0);
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          let start = 0;
          const step = target / (duration / 16);
          const tick = () => {
            start += step;
            if (start >= target) { setVal(target); return; }
            setVal(Math.round(start));
            requestAnimationFrame(tick);
          };
          tick();
          obs.disconnect();
        }
      },
      { threshold: 0.5 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [target, duration]);

  return <span ref={ref}>{val}{suffix}</span>;
};

/* ──────────────────────────────────────────────
   MAIN PAGE
────────────────────────────────────────────── */
const HomePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [tipIdx, setTipIdx] = useState(0);
  const [tipIn, setTipIn] = useState(true);

  useEffect(() => { userService.getProfile().then(setProfile).catch(() => {}); }, []);

  useEffect(() => {
    const iv = setInterval(() => {
      setTipIn(false);
      setTimeout(() => { setTipIdx((i) => (i + 1) % TIPS.length); setTipIn(true); }, 400);
    }, 5500);
    return () => clearInterval(iv);
  }, []);

  const firstName = profile?.first_name || user?.first_name || user?.email?.split('@')[0] || 'there';
  const skillCount = profile?.profile?.skills?.length ?? 0;
  const interestCount = profile?.profile?.interests?.length ?? 0;

  return (
    <div className="homepage">
      <Navbar />

      {/* ── HERO ── */}
      <section className="hp-hero">
        <HeroCanvas />
        <div className="hp-hero__inner">
          <p className="hp-hero__greeting">{getGreeting()},</p>
          <h1 className="hp-hero__name">{firstName} <span className="hp-wave">👋</span></h1>
          <p className="hp-hero__tagline">Your AI-powered career toolkit is ready. Where will you go today?</p>
          <div className="hp-hero__btns">
            <button className="hp-btn hp-btn--fill" onClick={() => navigate('/job-search')}>
              <span>Search Jobs</span>
              <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </button>
            <button className="hp-btn hp-btn--outline" onClick={() => navigate('/career-recommendations')}>
              <span>AI Guidance</span>
            </button>
          </div>
        </div>

        <div className="hp-hero__stats">
          {[
            { icon: '🛠️', val: skillCount || '—', label: 'Skills' },
            { icon: '🎯', val: interestCount || '—', label: 'Interests' },
            { icon: '⚡', val: '7+', label: 'Sources' },
            { icon: '🤖', val: 'AI', label: 'Powered' },
          ].map((s, i) => (
            <div className="hp-stat" key={i} style={{ animationDelay: `${0.5 + i * 0.1}s` }}>
              <span className="hp-stat__icon">{s.icon}</span>
              <span className="hp-stat__val">{s.val}</span>
              <span className="hp-stat__lbl">{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── METRICS ── */}
      <section className="hp-metrics">
        <div className="hp-metrics__item">
          <span className="hp-metrics__num"><AnimatedNumber target={7} suffix="+" /></span>
          <span className="hp-metrics__lbl">Job Sources</span>
        </div>
        <div className="hp-metrics__divider" />
        <div className="hp-metrics__item">
          <span className="hp-metrics__num"><AnimatedNumber target={5} /></span>
          <span className="hp-metrics__lbl">AI Tools</span>
        </div>
        <div className="hp-metrics__divider" />
        <div className="hp-metrics__item">
          <span className="hp-metrics__num"><AnimatedNumber target={100} suffix="%" /></span>
          <span className="hp-metrics__lbl">Free</span>
        </div>
        <div className="hp-metrics__divider" />
        <div className="hp-metrics__item">
          <span className="hp-metrics__num"><AnimatedNumber target={24} suffix="/7" /></span>
          <span className="hp-metrics__lbl">Available</span>
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section className="hp-features">
        <div className="hp-section-hdr">
          <span className="hp-section-badge">Tools</span>
          <h2 className="hp-section-title">Everything You Need</h2>
          <p className="hp-section-sub">Click any card to get started instantly</p>
        </div>
        <div className="hp-grid">
          {FEATURES.map((f, i) => (
            <FeatureCard key={f.id} feature={f} index={i} onClick={() => navigate(f.path)} />
          ))}
        </div>
      </section>

      {/* ── TIP ── */}
      <section className="hp-tip-section">
        <div className={`hp-tip ${tipIn ? 'hp-tip--in' : 'hp-tip--out'}`}>
          <div className="hp-tip__icon">💡</div>
          <p className="hp-tip__text">{TIPS[tipIdx]}</p>
          <div className="hp-tip__dots">
            {TIPS.map((_, i) => (
              <span key={i} className={`hp-tip__dot ${i === tipIdx ? 'active' : ''}`} />
            ))}
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="hp-footer">
        <span className="hp-footer__brand">HireSkill</span>
        <span className="hp-footer__dot">·</span>
        <span>Your AI-powered career companion</span>
      </footer>
    </div>
  );
};

export default HomePage;
