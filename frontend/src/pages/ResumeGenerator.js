import React, { useState, useRef } from 'react';
import Navbar from '../components/Navbar';
import documentService from '../services/documentService';
import '../styles/ATSChecker.css';

const ROLE_SUGGESTIONS = [
  'Software Engineer', 'Data Scientist', 'AI Engineer', 'Product Manager',
  'UX Designer', 'DevOps Engineer', 'Data Analyst', 'Frontend Developer',
  'Backend Developer', 'Cybersecurity Analyst',
];

const ScoreDial = ({ score }) => {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color =
    score >= 80 ? '#10b981' :
    score >= 60 ? '#3b82f6' :
    score >= 40 ? '#f59e0b' : '#ef4444';
  return (
    <div className="score-dial-wrapper">
      <svg width="180" height="180" viewBox="0 0 180 180">
        <circle cx="90" cy="90" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="14" />
        <circle
          cx="90" cy="90" r={radius} fill="none"
          stroke={color} strokeWidth="14"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 90 90)"
          style={{ transition: 'stroke-dashoffset 1.2s ease' }}
        />
        <text x="90" y="85" textAnchor="middle" fontSize="30" fontWeight="700" fill={color}>{score}</text>
        <text x="90" y="108" textAnchor="middle" fontSize="13" fill="#6b7280">/ 100</text>
      </svg>
      <p className="score-label" style={{ color }}>
        {score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : score >= 40 ? 'Fair' : 'Poor'}
      </p>
    </div>
  );
};

const ResumeGenerator = () => {
  const fileInputRef = useRef(null);
  const resultsRef  = useRef(null);
  const [file,       setFile]       = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [loading,    setLoading]    = useState(false);
  const [error,      setError]      = useState('');
  const [result,     setResult]     = useState(null);
  const [activeTab,  setActiveTab]  = useState('overview');
  const [showRoleDrop, setShowRoleDrop] = useState(false);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    if (!f.name.toLowerCase().endsWith('.pdf')) { setError('Only PDF files are supported.'); return; }
    setFile(f); setError(''); setResult(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f && f.name.toLowerCase().endsWith('.pdf')) { setFile(f); setError(''); setResult(null); }
    else setError('Please drop a PDF file.');
  };

  const handleCheck = async () => {
    if (!file) { setError('Please upload your resume PDF first.'); return; }
    setLoading(true); setError(''); setResult(null);
    try {
      const data = await documentService.checkATSResume(file, targetRole);
      setResult(data.data || data);
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    } catch (err) {
      setError(err.message || 'Failed to analyse resume. Please try again.');
    } finally { setLoading(false); }
  };

  const priorityBadge = (p) =>
    p === 'high' ? 'badge-high' : p === 'medium' ? 'badge-medium' : 'badge-low';
  const priorityColor = (p) =>
    p === 'high' ? '#ef4444' : p === 'medium' ? '#f59e0b' : '#6b7280';

  return (
    <>
      <Navbar />
      <div className="ats-checker-page">

        {/* Hero */}
        <div className="checker-hero">
          <h1>ATS Resume Checker</h1>
          <p>Instantly analyse your resume for ATS compatibility, get a score, and see exactly how to improve it.</p>
        </div>

        {/* Upload Card */}
        <div className="checker-card upload-card">
          <h2>Upload Your Resume</h2>

          <div
            className={`drop-zone ${file ? 'has-file' : ''}`}
            onClick={() => fileInputRef.current.click()}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
          >
            <input type="file" accept=".pdf" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileChange} />
            {file ? (
              <>
                <span className="file-icon">ðŸ“„</span>
                <p className="file-name">{file.name}</p>
                <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
                <button className="remove-file-btn" onClick={(e) => { e.stopPropagation(); setFile(null); setResult(null); }}>Remove</button>
              </>
            ) : (
              <>
                <span className="upload-icon">â˜ï¸</span>
                <p>Drag &amp; drop your PDF here, or <span className="browse-link">browse</span></p>
                <p className="upload-hint">PDF only Â· Max 5 MB</p>
              </>
            )}
          </div>

          {/* Role selector */}
          <div className="role-selector">
            <label>Target Role <span className="optional">(optional but recommended)</span></label>
            <div className="role-input-wrapper">
              <input
                type="text"
                placeholder="e.g. Software Engineer, Data Scientistâ€¦"
                value={targetRole}
                onChange={(e) => { setTargetRole(e.target.value); setShowRoleDrop(true); }}
                onFocus={() => setShowRoleDrop(true)}
                onBlur={() => setTimeout(() => setShowRoleDrop(false), 150)}
              />
              {showRoleDrop && (
                <ul className="role-dropdown">
                  {ROLE_SUGGESTIONS.filter(r => r.toLowerCase().includes(targetRole.toLowerCase())).map(r => (
                    <li key={r} onMouseDown={() => { setTargetRole(r); setShowRoleDrop(false); }}>{r}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          {error && <div className="checker-error">{error}</div>}

          <button className="check-btn" onClick={handleCheck} disabled={loading || !file}>
            {loading ? <><span className="spinner" /> Analysingâ€¦</> : 'ðŸ” Check My Resume'}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="checker-results" ref={resultsRef}>

            {/* Score Banner */}
            <div className="score-banner">
              <ScoreDial score={result.score} />
              <div className="score-summary">
                <h2>ATS Score: {result.score} / 100</h2>
                <p>
                  {result.score >= 80 ? 'Your resume is well-optimised for ATS systems. Minor tweaks can take it further.'
                   : result.score >= 60 ? 'Your resume passes basic ATS checks but has room for improvement.'
                   : result.score >= 40 ? 'Your resume has several ATS issues that need attention.'
                   : 'Your resume is likely being filtered out by ATS. Significant changes needed.'}
                </p>
                <div className="score-meta">
                  <span>ðŸ“„ {result.filename}</span>
                  <span>ðŸ“ {result.word_count} words</span>
                  {result.keyword_analysis?.role && <span>ðŸŽ¯ {result.keyword_analysis.role}</span>}
                </div>
              </div>
            </div>

            {/* Tabs */}
            <div className="result-tabs">
              {['overview', 'problems', 'keywords', 'recommendations'].map(tab => (
                <button key={tab} className={activeTab === tab ? 'active' : ''} onClick={() => setActiveTab(tab)}>
                  {tab === 'overview' ? 'ðŸ“Š Overview'
                   : tab === 'problems' ? `âš ï¸ Issues (${result.problems.length})`
                   : tab === 'keywords' ? 'ðŸ”‘ Keywords'
                   : 'ðŸ’¡ Recommendations'}
                </button>
              ))}
            </div>

            <div className="tab-content">

              {/* Overview */}
              {activeTab === 'overview' && (
                <div className="checks-grid">
                  <h3>Format &amp; Content Checks</h3>
                  <div className="checks-list">
                    {[...result.passed_checks, ...result.failed_checks]
                      .sort((a, b) => b.weight - a.weight)
                      .map((c) => {
                        const passed = result.passed_checks.some(p => p.key === c.key);
                        return (
                          <div key={c.key} className={`check-row ${passed ? 'pass' : 'fail'}`}>
                            <span className="check-icon">{passed ? 'âœ…' : 'âŒ'}</span>
                            <span className="check-label">{c.label}</span>
                            <span className="check-weight">+{c.weight} pts</span>
                          </div>
                        );
                      })}
                  </div>
                </div>
              )}

              {/* Problems */}
              {activeTab === 'problems' && (
                <div className="problems-list">
                  <h3>Issues Found</h3>
                  {result.problems.length === 0 ? (
                    <p className="all-good">ðŸŽ‰ No major issues found!</p>
                  ) : result.problems.map((p, i) => (
                    <div key={i} className="problem-item">
                      <span className="problem-icon">âš ï¸</span>
                      <p>{p}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Keywords */}
              {activeTab === 'keywords' && (
                <div className="keywords-panel">
                  {!result.keyword_analysis?.role ? (
                    <p className="no-role-msg">Enter a target role above to see keyword analysis.</p>
                  ) : (
                    <>
                      <div className="kw-stats">
                        <div className="kw-stat"><span className="kw-num matched">{result.keyword_analysis.matched.length}</span><span>Matched</span></div>
                        <div className="kw-stat"><span className="kw-num missing">{result.keyword_analysis.missing.length}</span><span>Missing</span></div>
                        <div className="kw-stat"><span className="kw-num total">{result.keyword_analysis.total_role_kws}</span><span>Total for role</span></div>
                      </div>
                      {result.keyword_analysis.matched.length > 0 && (
                        <div className="kw-section">
                          <h4>âœ… Matched Keywords</h4>
                          <div className="kw-tags">{result.keyword_analysis.matched.map(k => <span key={k} className="kw-tag kw-matched">{k}</span>)}</div>
                        </div>
                      )}
                      {result.keyword_analysis.missing.length > 0 && (
                        <div className="kw-section">
                          <h4>âŒ Missing Keywords</h4>
                          <div className="kw-tags">{result.keyword_analysis.missing.map(k => <span key={k} className="kw-tag kw-missing">{k}</span>)}</div>
                          <p className="kw-hint">Add these keywords naturally in your skills, experience, or summary.</p>
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}

              {/* Recommendations */}
              {activeTab === 'recommendations' && (
                <div className="recommendations-panel">
                  <h3>How to Improve Your Resume</h3>
                  {result.recommendations.length > 0 && (
                    <div className="recs-section">
                      <h4>ðŸ”§ Fixes &amp; Improvements</h4>
                      {result.recommendations.map((r, i) => (
                        <div key={i} className="rec-item">
                          <span className={`rec-badge ${priorityBadge(r.priority)}`} style={{ borderColor: priorityColor(r.priority), color: priorityColor(r.priority) }}>{r.priority}</span>
                          <p>{r.text}</p>
                        </div>
                      ))}
                    </div>
                  )}
                  {result.role_additions?.length > 0 && (
                    <div className="recs-section">
                      <h4>ðŸŽ¯ Role-Specific Additions {targetRole && `for "${targetRole}"`}</h4>
                      {result.role_additions.map((a, i) => (
                        <div key={i} className="rec-item">
                          <span className="rec-badge" style={{ borderColor: '#3b82f6', color: '#3b82f6' }}>tip</span>
                          <p>{a}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default ResumeGenerator;
