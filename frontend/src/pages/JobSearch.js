import React, { useState, useEffect, useCallback } from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import jobService from '../services/jobService';
import '../styles/JobSearch.css';

// --- Helpers ------------------------------------------------------------------
const timeAgo = (dateStr) => {
  if (!dateStr) return '';
  const diff = Date.now() - new Date(dateStr).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 2)   return 'just now';
  if (m < 60)  return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24)  return `${h}h ago`;
  const d = Math.floor(h / 24);
  if (d < 30)  return `${d}d ago`;
  return `${Math.floor(d / 30)}mo ago`;
};

const formatSalary = (min, max) => {
  if (!min && !max) return null;
  const f = (n) => n >= 1000 ? `$${(n / 1000).toFixed(0)}k` : `$${n}`;
  if (min && max) return `${f(min)}  ${f(max)}`;
  if (min) return `${f(min)}+`;
  return f(max);
};

const SOURCE_COLORS = {
  LinkedIn:    '#0077b5',
  Indeed:      '#2164f3',
  Glassdoor:   '#0caa41',
  Adzuna:      '#ef4a23',
  RemoteOK:    '#0d0d0d',
  'The Muse':  '#5c5ce5',
  ZipRecruiter:'#00c2a8',
  Monster:     '#6d1e9e',
  JSearch:     '#ff6b35',
};

const SOURCE_ICONS = {
  LinkedIn: '', Indeed: '', Glassdoor: '', Adzuna: '',
  RemoteOK: '', 'The Muse': '', ZipRecruiter: '', Monster: '', JSearch: '',
};

const SOURCE_TABS = ['All', 'LinkedIn', 'Indeed', 'RemoteOK', 'The Muse', 'Adzuna'];

const ScoreBadge = ({ score }) => {
  if (!score) return null;
  const color = score >= 80 ? '#10b981' : score >= 60 ? '#3b82f6' : score >= 40 ? '#f59e0b' : '#6b7280';
  return (
    <span className="match-score" style={{ background: color }}>
      {Math.round(score)}% Match
    </span>
  );
};

// --- Component ----------------------------------------------------------------
const JobSearch = () => {
  useAuth(); // auth context available if needed
  const [jobs, setJobs]           = useState([]);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState('');
  const [toast, setToast]         = useState('');
  const [searchMode, setSearchMode] = useState('search');   // 'matched' | 'search'
  const [selectedJob, setSelectedJob] = useState(null);
  const [activeSource, setActiveSource] = useState('All'); // source tab

  const [filters, setFilters] = useState({
    role: '', location: '', experience_level: '', work_type: '', job_type: '',
  });
  const [searchQuery, setSearchQuery] = useState('');

  const showToast = (msg) => { setToast(msg); setTimeout(() => setToast(''), 3200); };

  // --- Data loading -----------------------------------------------------------
  const loadMatchedJobs = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const data = await jobService.getMatchedJobs(filters);
      setJobs(data.jobs || []);
      if (!data.jobs?.length) setError('No matching jobs found. Try adjusting your filters.');
    } catch (err) {
      setError('Could not load matched jobs. Check your profile is complete.');
    } finally { setLoading(false); }
  }, [filters]);

  const handleSearch = useCallback(async () => {
    setLoading(true); setError(''); setSearchMode('search');
    try {
      const sourceParam = activeSource !== 'All' ? activeSource : '';
      const data = await jobService.searchJobs(searchQuery, { ...filters, source: sourceParam });
      setJobs(data.jobs || []);
      if (!data.jobs?.length) setError('No jobs found. Try a different search term or remove filters.');
    } catch (err) {
      setError('Search failed. The job APIs may be temporarily unavailable.');
    } finally { setLoading(false); }
  }, [searchQuery, filters, activeSource]);

  // Run search on mount
  useEffect(() => { handleSearch(); }, []); // eslint-disable-line

  // Re-run when source tab changes
  useEffect(() => { if (!loading) handleSearch(); }, [activeSource]); // eslint-disable-line

  const handleFilterChange = (field, value) =>
    setFilters((prev) => ({ ...prev, [field]: value }));

  // --- Actions ----------------------------------------------------------------
  const handleViewJob = (job) => setSelectedJob(job);

  const openOriginalPosting = (job, e) => {
    e?.stopPropagation();
    if (job.source_url) {
      window.open(job.source_url, '_blank', 'noopener,noreferrer');
    } else {
      showToast('No external link available for this job.');
    }
  };

  const handleSaveJob = async (job, e) => {
    e?.stopPropagation();
    try {
      await jobService.saveExternalJob(job);
      showToast('Job saved to your list!');
    } catch (err) {
      showToast(err.response?.data?.error || 'Could not save job — please log in.');
    }
  };

  // --- Filtered job list ------------------------------------------------------
  const visibleJobs = activeSource === 'All'
    ? jobs
    : jobs.filter((j) => (j.source || '').toLowerCase() === activeSource.toLowerCase());

  // --- Render -----------------------------------------------------------------
  return (
    <>
      <Navbar />
      <div className="job-search-container">

        {/* Header */}
        <div className="job-search-header">
          <h1>Live Job Search</h1>
          <p>Real-time postings from LinkedIn, Indeed, RemoteOK, The Muse &amp; more</p>
        </div>

        {/* Mode toggle */}
        <div className="mode-toggle">
          <button className={searchMode === 'matched' ? 'active' : ''}
                  onClick={() => { setSearchMode('matched'); loadMatchedJobs(); }}>
            ✨ Matched For Me
          </button>
          <button className={searchMode === 'search' ? 'active' : ''}
                  onClick={() => setSearchMode('search')}>
            🔎 Search All Jobs
          </button>
        </div>

        {/* Search bar */}
        <div className="search-section">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search title, skill, or company…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button onClick={handleSearch} className="search-btn" disabled={loading}>
              {loading ? '…' : 'Search'}
            </button>
          </div>

          {/* Filters */}
          <div className="filters-section">
            <div className="filter-group">
              <label>Role</label>
              <input type="text" placeholder="e.g. Software Engineer"
                     value={filters.role}
                     onChange={(e) => handleFilterChange('role', e.target.value)} />
            </div>
            <div className="filter-group">
              <label>Location</label>
              <select value={filters.location} onChange={(e) => handleFilterChange('location', e.target.value)}>
                <option value="">Any Location</option>
                <option value="Remote">Remote</option>
                <option value="San Francisco">San Francisco</option>
                <option value="New York">New York</option>
                <option value="Seattle">Seattle</option>
                <option value="Austin">Austin</option>
                <option value="London">London</option>
                <option value="Berlin">Berlin</option>
              </select>
            </div>
            <div className="filter-group">
              <label>Experience</label>
              <select value={filters.experience_level}
                      onChange={(e) => handleFilterChange('experience_level', e.target.value)}>
                <option value="">Any Level</option>
                <option value="Entry">Entry Level</option>
                <option value="Mid">Mid Level</option>
                <option value="Senior">Senior Level</option>
                <option value="Lead">Lead / Staff</option>
              </select>
            </div>
            <div className="filter-group">
              <label>Work Type</label>
              <select value={filters.work_type}
                      onChange={(e) => handleFilterChange('work_type', e.target.value)}>
                <option value="">Any Type</option>
                <option value="Remote">Remote</option>
                <option value="Hybrid">Hybrid</option>
                <option value="On-site">On-site</option>
              </select>
            </div>
            <button onClick={handleSearch} className="apply-filters-btn" disabled={loading}>
              Apply Filters
            </button>
          </div>
        </div>

        {/* Source tabs */}
        <div className="source-tabs">
          {SOURCE_TABS.map((src) => (
            <button
              key={src}
              className={`source-tab ${activeSource === src ? 'active' : ''}`}
              style={activeSource === src && src !== 'All'
                ? { borderColor: SOURCE_COLORS[src], color: SOURCE_COLORS[src] }
                : {}}
              onClick={() => setActiveSource(src)}
            >
              {src !== 'All' && SOURCE_ICONS[src]} {src}
            </button>
          ))}
        </div>

        {/* Messages */}
        {error && <div className="error-message">{error}</div>}

        {/* Loading / Grid */}
        {loading ? (
          <div className="loading-spinner">
            <span className="spinner-ring" />
            Fetching live jobs…
          </div>
        ) : (
          <>
            <p className="results-count">
              {visibleJobs.length} job{visibleJobs.length !== 1 ? 's' : ''} found
              {activeSource !== 'All' && ` on ${activeSource}`}
            </p>
            <div className="jobs-grid">
              {visibleJobs.map((job) => (
                <JobCard
                  key={job.id}
                  job={job}
                  onView={handleViewJob}
                  onOpen={openOriginalPosting}
                  onSave={handleSaveJob}
                />
              ))}
            </div>
          </>
        )}

        {/* Job detail modal */}
        {selectedJob && (
          <JobModal
            job={selectedJob}
            onClose={() => setSelectedJob(null)}
            onOpen={openOriginalPosting}
            onSave={handleSaveJob}
          />
        )}

        {/* Toast */}
        {toast && <div className="toast">{toast}</div>}
      </div>
    </>
  );
};

// --- Sub-components -----------------------------------------------------------
const JobCard = ({ job, onView, onOpen, onSave }) => {
  const salary  = formatSalary(job.salary_min, job.salary_max) || job.salary;
  const srcColor = SOURCE_COLORS[job.source] || '#6b7280';

  return (
    <div className="job-card" onClick={() => onView(job)}>
      <div className="job-card-header">
        {job.company_logo ? (
          <img src={job.company_logo} alt={job.company} className="company-logo"
               onError={(e) => { e.target.style.display = 'none'; }} />
        ) : (
          <div className="company-logo-placeholder">{(job.company || '?')[0].toUpperCase()}</div>
        )}
        <div className="job-card-title-section">
          <h3>{job.title}</h3>
          <p className="company-name">{job.company}</p>
        </div>
        <ScoreBadge score={job.match_score} />
      </div>

      <div className="job-card-details">
        <span className="job-detail"> {job.location}</span>
        <span className="job-detail"> {job.work_type}</span>
        {salary && <span className="job-detail"> {salary}</span>}
        {job.posted_date && <span className="job-detail posted-time"> {timeAgo(job.posted_date)}</span>}
      </div>

      {job.skills_required?.length > 0 && (
        <div className="job-skills">
          {job.skills_required.slice(0, 4).map((s, i) => (
            <span key={i} className="skill-badge">{s}</span>
          ))}
          {job.skills_required.length > 4 && (
            <span className="skill-badge skill-more">+{job.skills_required.length - 4}</span>
          )}
        </div>
      )}

      <div className="job-card-footer">
        <span className="source-badge" style={{ color: srcColor, borderColor: srcColor }}>
          {SOURCE_ICONS[job.source] || ''} {job.source || 'External'}
        </span>
        <div className="card-actions">
          <button className="save-btn" title="Save job"
                  onClick={(e) => onSave(job, e)}>
             Save
          </button>
          <button className="view-btn" style={{ background: srcColor }}
                  onClick={(e) => onOpen(job, e)}>
            View 
          </button>
        </div>
      </div>
    </div>
  );
};

const JobModal = ({ job, onClose, onOpen, onSave }) => {
  const salary   = formatSalary(job.salary_min, job.salary_max) || job.salary;
  const srcColor = SOURCE_COLORS[job.source] || '#6b7280';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>

        <div className="modal-header">
          {job.company_logo ? (
            <img src={job.company_logo} alt={job.company} className="company-logo-large"
                 onError={(e) => { e.target.style.display = 'none'; }} />
          ) : (
            <div className="company-logo-placeholder large">
              {(job.company || '?')[0].toUpperCase()}
            </div>
          )}
          <div>
            <h2>{job.title}</h2>
            <p className="company-name-large">{job.company}</p>
          </div>
        </div>

        <div className="modal-details">
          <span> {job.location}</span>
          <span> {job.work_type}</span>
          {job.job_type && <span> {job.job_type}</span>}
          {job.experience_level && <span> {job.experience_level}</span>}
          {salary && <span> {salary}</span>}
          {job.posted_date && <span> Posted {timeAgo(job.posted_date)}</span>}
        </div>

        {job.match_score && (
          <div className="match-score-section">
            <ScoreBadge score={job.match_score} />
            <span style={{ marginLeft: 8, color: '#6b7280' }}>profile match</span>
          </div>
        )}

        {job.description && (
          <div className="modal-section">
            <h3>About the Role</h3>
            <p className="job-description">{job.description}</p>
          </div>
        )}

        {job.responsibilities?.length > 0 && (
          <div className="modal-section">
            <h3>Responsibilities</h3>
            <ul>{job.responsibilities.map((r, i) => <li key={i}>{r}</li>)}</ul>
          </div>
        )}

        {job.requirements?.length > 0 && (
          <div className="modal-section">
            <h3>Requirements</h3>
            <ul>{job.requirements.map((r, i) => <li key={i}>{r}</li>)}</ul>
          </div>
        )}

        {job.skills_required?.length > 0 && (
          <div className="modal-section">
            <h3>Required Skills</h3>
            <div className="job-skills">
              {job.skills_required.map((s, i) => (
                <span key={i} className="skill-badge">{s}</span>
              ))}
            </div>
          </div>
        )}

        {job.benefits?.length > 0 && (
          <div className="modal-section">
            <h3>Benefits</h3>
            <ul>{job.benefits.map((b, i) => <li key={i}>{b}</li>)}</ul>
          </div>
        )}

        <div className="modal-actions">
          <button className="save-btn-large" onClick={(e) => onSave(job, e)}>
             Save Job
          </button>
          <button className="view-btn-large" style={{ background: srcColor }}
                  onClick={(e) => onOpen(job, e)}>
            {SOURCE_ICONS[job.source] || ''} View on {job.source || 'Job Site'} 
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobSearch;