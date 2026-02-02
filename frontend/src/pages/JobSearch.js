import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import jobService from '../services/jobService';
import '../styles/JobSearch.css';

const JobSearch = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchMode, setSearchMode] = useState('matched'); // 'matched' or 'search'
  const [selectedJob, setSelectedJob] = useState(null);
  const [showJobModal, setShowJobModal] = useState(false);
  
  // Filters
  const [filters, setFilters] = useState({
    role: '',
    location: '',
    experience_level: '',
    work_type: '',
    job_type: '',
    limit: 20
  });
  
  const [searchQuery, setSearchQuery] = useState('');
  
  // Load matched jobs on mount
  useEffect(() => {
    if (searchMode === 'matched') {
      loadMatchedJobs();
    }
  }, [searchMode]);
  
  const loadMatchedJobs = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await jobService.getMatchedJobs(filters);
      setJobs(data.jobs || []);
      if (data.jobs && data.jobs.length === 0) {
        setError('No matching jobs found. Try adjusting your filters.');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load matched jobs');
      console.error('Error loading matched jobs:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setSearchMode('search');
    
    try {
      const data = await jobService.searchJobs(searchQuery, filters);
      setJobs(data.jobs || []);
      if (data.jobs && data.jobs.length === 0) {
        setError('No jobs found matching your search.');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to search jobs');
      console.error('Error searching jobs:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };
  
  const handleApplyFilters = () => {
    if (searchMode === 'matched') {
      loadMatchedJobs();
    } else {
      handleSearch();
    }
  };
  
  const handleJobClick = async (job) => {
    setSelectedJob(job);
    setShowJobModal(true);
  };
  
  const handleSaveJob = async (jobId) => {
    try {
      await jobService.saveJob(jobId);
      setSuccess('Job saved successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save job');
    }
  };
  
  const handleApplyToJob = async (jobId) => {
    try {
      await jobService.applyToJob(jobId);
      setSuccess('Application submitted successfully!');
      setTimeout(() => setSuccess(''), 3000);
      setShowJobModal(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to apply to job');
    }
  };
  
  const formatSalary = (min, max) => {
    if (!min && !max) return 'Not specified';
    const formatNum = (num) => {
      if (num >= 1000) return `$${(num / 1000).toFixed(0)}k`;
      return `$${num}`;
    };
    if (min && max) return `${formatNum(min)} - ${formatNum(max)}`;
    if (min) return `${formatNum(min)}+`;
    return formatNum(max);
  };
  
  const getMatchScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#6b7280';
  };
  
  return (
    <div className="job-search-container">
      <div className="job-search-header">
        <h1>🔍 Job Search & Matching</h1>
        <p>Find your perfect job opportunity</p>
      </div>
      
      {/* Mode Toggle */}
      <div className="mode-toggle">
        <button
          className={searchMode === 'matched' ? 'active' : ''}
          onClick={() => setSearchMode('matched')}
        >
          ✨ Matched For You
        </button>
        <button
          className={searchMode === 'search' ? 'active' : ''}
          onClick={() => setSearchMode('search')}
        >
          🔎 Search All Jobs
        </button>
      </div>
      
      {/* Search Bar */}
      <div className="search-section">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search by title, company, or keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch} className="search-btn">
            Search
          </button>
        </div>
        
        {/* Filters */}
        <div className="filters-section">
          <div className="filter-group">
            <label>Role</label>
            <input
              type="text"
              placeholder="e.g., Software Engineer"
              value={filters.role}
              onChange={(e) => handleFilterChange('role', e.target.value)}
            />
          </div>
          
          <div className="filter-group">
            <label>Location</label>
            <select
              value={filters.location}
              onChange={(e) => handleFilterChange('location', e.target.value)}
            >
              <option value="">Any Location</option>
              <option value="Remote">Remote</option>
              <option value="San Francisco">San Francisco, CA</option>
              <option value="New York">New York, NY</option>
              <option value="Seattle">Seattle, WA</option>
              <option value="Austin">Austin, TX</option>
              <option value="Boston">Boston, MA</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Experience</label>
            <select
              value={filters.experience_level}
              onChange={(e) => handleFilterChange('experience_level', e.target.value)}
            >
              <option value="">Any Level</option>
              <option value="Entry">Entry Level</option>
              <option value="Mid">Mid Level</option>
              <option value="Senior">Senior Level</option>
              <option value="Lead">Lead</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Work Type</label>
            <select
              value={filters.work_type}
              onChange={(e) => handleFilterChange('work_type', e.target.value)}
            >
              <option value="">Any Type</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="On-site">On-site</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Job Type</label>
            <select
              value={filters.job_type}
              onChange={(e) => handleFilterChange('job_type', e.target.value)}
            >
              <option value="">Any Type</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
            </select>
          </div>
          
          <button onClick={handleApplyFilters} className="apply-filters-btn">
            Apply Filters
          </button>
        </div>
      </div>
      
      {/* Messages */}
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      {/* Job Listings */}
      {loading ? (
        <div className="loading-spinner">Loading jobs...</div>
      ) : (
        <div className="jobs-grid">
          {jobs.map((job) => (
            <div key={job.id} className="job-card" onClick={() => handleJobClick(job)}>
              <div className="job-card-header">
                {job.company_logo && (
                  <img src={job.company_logo} alt={job.company} className="company-logo" />
                )}
                <div className="job-card-title-section">
                  <h3>{job.title}</h3>
                  <p className="company-name">{job.company}</p>
                </div>
                {job.match_score && (
                  <div 
                    className="match-score"
                    style={{ backgroundColor: getMatchScoreColor(job.match_score) }}
                  >
                    {job.match_score}% Match
                  </div>
                )}
              </div>
              
              <div className="job-card-details">
                <span className="job-detail">📍 {job.location}</span>
                <span className="job-detail">💼 {job.experience_level}</span>
                <span className="job-detail">🏢 {job.work_type}</span>
                <span className="job-detail">💰 {formatSalary(job.salary_min, job.salary_max)}</span>
              </div>
              
              <div className="job-skills">
                {job.skills_required && job.skills_required.slice(0, 5).map((skill, idx) => (
                  <span key={idx} className="skill-badge">{skill}</span>
                ))}
                {job.skills_required && job.skills_required.length > 5 && (
                  <span className="skill-badge">+{job.skills_required.length - 5} more</span>
                )}
              </div>
              
              <div className="job-card-footer">
                <button 
                  className="save-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSaveJob(job.id);
                  }}
                >
                  💾 Save
                </button>
                <button 
                  className="apply-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleApplyToJob(job.id);
                  }}
                >
                  Apply Now
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Job Detail Modal */}
      {showJobModal && selectedJob && (
        <div className="modal-overlay" onClick={() => setShowJobModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowJobModal(false)}>×</button>
            
            <div className="modal-header">
              {selectedJob.company_logo && (
                <img src={selectedJob.company_logo} alt={selectedJob.company} className="company-logo-large" />
              )}
              <div>
                <h2>{selectedJob.title}</h2>
                <p className="company-name-large">{selectedJob.company}</p>
              </div>
            </div>
            
            <div className="modal-details">
              <span>📍 {selectedJob.location}</span>
              <span>💼 {selectedJob.experience_level}</span>
              <span>🏢 {selectedJob.work_type}</span>
              <span>🕒 {selectedJob.job_type}</span>
              <span>💰 {formatSalary(selectedJob.salary_min, selectedJob.salary_max)}</span>
            </div>
            
            {selectedJob.match_score && (
              <div className="match-score-section">
                <strong>Match Score:</strong>
                <div 
                  className="match-score-large"
                  style={{ backgroundColor: getMatchScoreColor(selectedJob.match_score) }}
                >
                  {selectedJob.match_score}% Match
                </div>
              </div>
            )}
            
            <div className="modal-section">
              <h3>About the Role</h3>
              <p className="job-description">{selectedJob.description}</p>
            </div>
            
            {selectedJob.responsibilities && selectedJob.responsibilities.length > 0 && (
              <div className="modal-section">
                <h3>Responsibilities</h3>
                <ul>
                  {selectedJob.responsibilities.map((resp, idx) => (
                    <li key={idx}>{resp}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {selectedJob.requirements && selectedJob.requirements.length > 0 && (
              <div className="modal-section">
                <h3>Requirements</h3>
                <ul>
                  {selectedJob.requirements.map((req, idx) => (
                    <li key={idx}>{req}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {selectedJob.skills_required && selectedJob.skills_required.length > 0 && (
              <div className="modal-section">
                <h3>Required Skills</h3>
                <div className="job-skills">
                  {selectedJob.skills_required.map((skill, idx) => (
                    <span key={idx} className="skill-badge">{skill}</span>
                  ))}
                </div>
              </div>
            )}
            
            {selectedJob.benefits && selectedJob.benefits.length > 0 && (
              <div className="modal-section">
                <h3>Benefits</h3>
                <ul>
                  {selectedJob.benefits.map((benefit, idx) => (
                    <li key={idx}>{benefit}</li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="modal-actions">
              <button onClick={() => handleSaveJob(selectedJob.id)} className="save-btn-large">
                💾 Save Job
              </button>
              <button onClick={() => handleApplyToJob(selectedJob.id)} className="apply-btn-large">
                Apply Now
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobSearch;
