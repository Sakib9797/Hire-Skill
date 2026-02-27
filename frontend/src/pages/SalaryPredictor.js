import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import salaryService from '../services/salaryService';
import '../styles/SalaryPredictor.css';

const EXPERIENCE_LEVELS = ['entry', 'junior', 'mid', 'senior', 'lead', 'staff', 'principal'];
const LOCATION_TYPES = ['remote', 'hybrid', 'onsite'];

const COMMON_SKILLS = [
  'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'SQL', 'PostgreSQL',
  'MongoDB', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Machine Learning',
  'TensorFlow', 'PyTorch', 'Scikit-learn', 'Deep Learning', 'NLP', 'Data Analysis',
  'Pandas', 'NumPy', 'Git', 'CI/CD', 'REST API', 'GraphQL', 'Linux', 'Terraform',
  'Redis', 'Kafka', 'Spark', 'Airflow', 'Java', 'Go', 'Rust', 'C++', 'Swift', 'Kotlin',
];

const fmt = (n) => n?.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

const SalaryPredictor = () => {
  const [roles, setRoles] = useState([]);
  const [form, setForm] = useState({
    role: 'Machine Learning Engineer',
    experience_level: 'mid',
    experience_years: 3,
    location_type: 'remote',
    skills: [],
    skillInput: '',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [skillSuggestions, setSkillSuggestions] = useState([]);

  useEffect(() => {
    salaryService.getRoles()
      .then(r => setRoles((r.data?.roles || r.roles || []).map(x => x.role)))
      .catch(() => {});
  }, []);

  const handleSkillInput = (val) => {
    setForm(f => ({ ...f, skillInput: val }));
    if (val.length > 0) {
      setSkillSuggestions(
        COMMON_SKILLS.filter(s => s.toLowerCase().includes(val.toLowerCase()) && !form.skills.includes(s)).slice(0, 6)
      );
    } else {
      setSkillSuggestions([]);
    }
  };

  const addSkill = (skill) => {
    if (skill && !form.skills.includes(skill)) {
      setForm(f => ({ ...f, skills: [...f.skills, skill], skillInput: '' }));
    }
    setSkillSuggestions([]);
  };

  const removeSkill = (skill) => setForm(f => ({ ...f, skills: f.skills.filter(s => s !== skill) }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.role) { setError('Please select a role.'); return; }
    setLoading(true); setError(''); setResult(null);
    try {
      const res = await salaryService.predictSalary({
        role: form.role,
        experience_level: form.experience_level,
        experience_years: Number(form.experience_years),
        skills: form.skills,
        location_type: form.location_type,
      });
      setResult(res.data || res);
    } catch (err) {
      setError(err?.message || err?.error || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const percentile = result?.market_percentile || 0;
  const barWidth = `${Math.min(percentile, 100)}%`;

  return (
    <>
      <Navbar />
      <div className="salary-page">
        <div className="salary-header">
          <h1>💰 Salary Predictor</h1>
          <p>ML-powered salary estimation. Enter your role, experience, and skills to see what you should earn.</p>
        </div>

        <div className="salary-content">
          {/* ── Form ── */}
          <form className="salary-form card" onSubmit={handleSubmit}>
            <h2>Your Profile</h2>

            <div className="form-group">
              <label>Role *</label>
              <select value={form.role} onChange={e => setForm(f => ({ ...f, role: e.target.value }))}>
                <option value="">-- Select a Role --</option>
                {(roles.length ? roles : ['Machine Learning Engineer', 'Data Scientist', 'Full Stack Developer', 'Backend Developer', 'Frontend Developer']).map(r => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Experience Level</label>
                <select value={form.experience_level} onChange={e => setForm(f => ({ ...f, experience_level: e.target.value }))}>
                  {EXPERIENCE_LEVELS.map(l => <option key={l} value={l}>{l.charAt(0).toUpperCase() + l.slice(1)}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Years of Experience</label>
                <input type="number" min="0" max="30" value={form.experience_years}
                  onChange={e => setForm(f => ({ ...f, experience_years: e.target.value }))} />
              </div>
              <div className="form-group">
                <label>Work Type</label>
                <select value={form.location_type} onChange={e => setForm(f => ({ ...f, location_type: e.target.value }))}>
                  {LOCATION_TYPES.map(l => <option key={l} value={l}>{l.charAt(0).toUpperCase() + l.slice(1)}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group skill-input-group">
              <label>Skills ({form.skills.length} added)</label>
              <div className="skill-input-wrap">
                <input
                  type="text"
                  placeholder="Type a skill and press Enter or pick a suggestion…"
                  value={form.skillInput}
                  onChange={e => handleSkillInput(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addSkill(form.skillInput.trim()); } }}
                />
                {skillSuggestions.length > 0 && (
                  <ul className="skill-suggestions">
                    {skillSuggestions.map(s => <li key={s} onClick={() => addSkill(s)}>{s}</li>)}
                  </ul>
                )}
              </div>
              <div className="skill-chips">
                {form.skills.map(s => (
                  <span key={s} className="chip">{s} <button type="button" onClick={() => removeSkill(s)}>×</button></span>
                ))}
              </div>
              <div className="quick-skills">
                <span>Quick add:</span>
                {COMMON_SKILLS.slice(0, 10).map(s => (
                  !form.skills.includes(s) && (
                    <button key={s} type="button" className="btn-quick" onClick={() => addSkill(s)}>{s}</button>
                  )
                ))}
              </div>
            </div>

            {error && <div className="alert-error">{error}</div>}

            <button type="submit" className="btn-predict" disabled={loading}>
              {loading ? '⏳ Calculating…' : '💰 Predict My Salary'}
            </button>
          </form>

          {/* ── Result ── */}
          {result && (
            <div className="salary-result card">
              <h2>Your Salary Estimate</h2>
              <div className="predicted-salary">{fmt(result.predicted_salary)}</div>
              <p className="salary-subtitle">per year · {result.role} · {result.experience_level} · {result.location_type}</p>

              <div className="salary-range-bar">
                <span className="range-label">{fmt(result.market_range?.min)}</span>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: barWidth }} />
                  <div className="bar-marker" style={{ left: barWidth }}>
                    <div className="marker-tooltip">{percentile}th percentile</div>
                  </div>
                </div>
                <span className="range-label">{fmt(result.market_range?.max)}</span>
              </div>

              <div className="range-cards">
                <div className="range-card low">
                  <div className="rc-label">Conservative</div>
                  <div className="rc-value">{fmt(result.salary_range?.min)}</div>
                </div>
                <div className="range-card mid">
                  <div className="rc-label">Expected</div>
                  <div className="rc-value">{fmt(result.predicted_salary)}</div>
                </div>
                <div className="range-card high">
                  <div className="rc-label">Optimistic</div>
                  <div className="rc-value">{fmt(result.salary_range?.max)}</div>
                </div>
              </div>

              {result.top_skills_for_raise?.length > 0 && (
                <div className="boost-section">
                  <h3>🚀 Skills That Could Boost Your Salary</h3>
                  <div className="skill-chips">
                    {result.top_skills_for_raise.map(s => <span key={s} className="chip chip-boost">{s}</span>)}
                  </div>
                </div>
              )}

              {result.insights?.length > 0 && (
                <div className="insights-section">
                  <h3>💡 Salary Insights</h3>
                  <ul className="insight-list">
                    {result.insights.map((tip, i) => <li key={i}>{tip}</li>)}
                  </ul>
                </div>
              )}

              <div className="meta-info">
                <span>Market percentile: <strong>{percentile}th</strong></span>
                <span>Skills matched: <strong>{result.num_skills_matched}</strong></span>
                <span>Category: <strong>{result.category}</strong></span>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default SalaryPredictor;
