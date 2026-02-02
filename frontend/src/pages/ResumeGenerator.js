import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import documentService from '../services/documentService';
import '../styles/DocumentGenerator.css';

const ResumeGenerator = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [resumes, setResumes] = useState([]);
  const [templates, setTemplates] = useState({});
  const [selectedResume, setSelectedResume] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [cvFile, setCvFile] = useState(null);
  const [useATSMode, setUseATSMode] = useState(false);
  const [roleRecommendations, setRoleRecommendations] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    target_role: '',
    template: 'professional'
  });

  useEffect(() => {
    loadTemplates();
    loadResumes();
  }, []);

  // Load role recommendations when target_role changes
  useEffect(() => {
    if (formData.target_role && formData.target_role.length > 2) {
      loadRoleRecommendations(formData.target_role);
    } else {
      setRoleRecommendations(null);
    }
  }, [formData.target_role]);

  const loadTemplates = async () => {
    try {
      const response = await documentService.getTemplates();
      setTemplates(response.data.templates);
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const loadResumes = async () => {
    try {
      const response = await documentService.getResumes();
      setResumes(response.data.resumes || []);
    } catch (err) {
      console.error('Error loading resumes:', err);
    }
  };

  const loadRoleRecommendations = async (role) => {
    try {
      const response = await documentService.getRoleRecommendations(role);
      setRoleRecommendations(response.data);
    } catch (err) {
      console.error('Error loading recommendations:', err);
      setRoleRecommendations(null);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Please upload a PDF file');
        return;
      }
      setCvFile(file);
      setError('');
    }
  };

  const handleRemoveFile = () => {
    setCvFile(null);
    document.getElementById('cv-file-input').value = '';
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      let response;
      
      if (useATSMode || cvFile) {
        // Generate ATS resume (with or without CV upload)
        response = await documentService.generateATSResume(formData, cvFile);
        setSuccess('ATS-optimized resume generated successfully!');
      } else {
        // Standard resume generation
        response = await documentService.generateResume(formData);
        setSuccess('Resume generated successfully!');
      }
      
      setSelectedResume(response.data.resume);
      setShowPreview(true);
      loadResumes(); // Reload list
      
      // Reset form
      setCvFile(null);
      if (document.getElementById('cv-file-input')) {
        document.getElementById('cv-file-input').value = '';
      }
      
    } catch (err) {
      console.error('Error generating resume:', err);
      setError(err.message || 'Failed to generate resume. Please complete your profile first.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewResume = async (resumeId) => {
    try {
      const response = await documentService.getResume(resumeId);
      setSelectedResume(response.data.resume);
      setShowPreview(true);
    } catch (err) {
      setError('Failed to load resume');
    }
  };

  const handleDeleteResume = async (resumeId) => {
    if (!window.confirm('Are you sure you want to delete this resume?')) {
      return;
    }

    try {
      await documentService.deleteResume(resumeId);
      setSuccess('Resume deleted successfully');
      loadResumes();
      if (selectedResume?.id === resumeId) {
        setSelectedResume(null);
        setShowPreview(false);
      }
    } catch (err) {
      setError('Failed to delete resume');
    }
  };

  const handleDownloadJSON = () => {
    if (!selectedResume) return;
    
    const dataStr = JSON.stringify(selectedResume.content, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `resume-${selectedResume.id}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const renderResumePreview = () => {
    if (!selectedResume || !selectedResume.content) return null;

    const content = selectedResume.content;
    const contact = content.contact || {};
    const sections = content.sections || {};
    const metadata = content.metadata || {};
    const isATSResume = metadata.ats_optimized || selectedResume.template_name?.includes('ats');

    return (
      <div className="resume-preview">
        <div className="preview-header">
          <h2>
            {selectedResume.title}
            {isATSResume && <span className="badge-ats" style={{marginLeft: '10px'}}>ATS</span>}
          </h2>
          <div className="preview-actions">
            <button onClick={handleDownloadJSON} className="btn-download">
              📥 Download JSON
            </button>
            <button onClick={() => setShowPreview(false)} className="btn-close-preview">
              ✕ Close
            </button>
          </div>
        </div>

        <div className={`resume-content ${isATSResume ? 'ats-resume' : ''}`}>
          {/* Contact Section */}
          <div className="resume-section">
            <h3>{contact.full_name}</h3>
            <div className="contact-info">
              {isATSResume ? (
                <>
                  {contact.email && <span>{contact.email}</span>}
                  {contact.phone && <span>{contact.phone}</span>}
                  {contact.location && <span>{contact.location}</span>}
                  {contact.linkedin && <span>{contact.linkedin}</span>}
                  {contact.github && <span>{contact.github}</span>}
                </>
              ) : (
                <>
                  {contact.email && <span>📧 {contact.email}</span>}
                  {contact.phone && <span>📱 {contact.phone}</span>}
                  {contact.location && <span>📍 {contact.location}</span>}
                  {contact.linkedin && <span>💼 {contact.linkedin}</span>}
                  {contact.github && <span>💻 {contact.github}</span>}
                </>
              )}
            </div>
          </div>

          {/* Summary */}
          {sections.summary && (
            <div className="resume-section">
              <h4>Professional Summary</h4>
              <p>{sections.summary}</p>
            </div>
          )}

          {/* Executive Summary */}
          {sections.executive_summary && (
            <div className="resume-section">
              <h4>Executive Summary</h4>
              <p>{sections.executive_summary}</p>
            </div>
          )}

          {/* Skills */}
          {sections.skills && (
            <div className="resume-section">
              <h4>{isATSResume ? 'CORE COMPETENCIES' : 'Skills'}</h4>
              {isATSResume ? (
                // ATS Format: Simple comma-separated list
                <div className="skill-tags">
                  {[
                    ...(sections.skills.technical || []),
                    ...(sections.skills.tools || []),
                    ...(sections.skills.soft || []),
                    ...(sections.skills.other || [])
                  ].map((skill, i) => (
                    <span key={i} className="skill-tag">{skill}</span>
                  ))}
                </div>
              ) : (
                // Standard Format: Categorized with visual tags
                <div className="skills-grid">
                  {sections.skills.technical && sections.skills.technical.length > 0 && (
                    <div className="skill-category">
                      <strong>Technical:</strong>
                      <div className="skill-tags">
                        {sections.skills.technical.map((skill, i) => (
                          <span key={i} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {sections.skills.soft && sections.skills.soft.length > 0 && (
                    <div className="skill-category">
                      <strong>Soft Skills:</strong>
                      <div className="skill-tags">
                        {sections.skills.soft.map((skill, i) => (
                          <span key={i} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {sections.skills.other && sections.skills.other.length > 0 && (
                    <div className="skill-category">
                      <strong>Other:</strong>
                      <div className="skill-tags">
                        {sections.skills.other.map((skill, i) => (
                          <span key={i} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Experience */}
          {sections.experience && sections.experience.length > 0 && (
            <div className="resume-section">
              <h4>{isATSResume ? 'PROFESSIONAL EXPERIENCE' : 'Work Experience'}</h4>
              {sections.experience.map((exp, i) => (
                <div key={i} className="experience-item">
                  <div className="exp-header">
                    <strong>{exp.title}</strong>
                    <span className="company-name">{exp.company}</span>
                  </div>
                  {exp.location && <div className="exp-location">{exp.location}</div>}
                  {(exp.period || exp.duration) && (
                    <div className="exp-duration">{exp.period || exp.duration}</div>
                  )}
                  {exp.description && Array.isArray(exp.description) && exp.description.length > 0 && (
                    <ul className="exp-bullets">
                      {exp.description.map((desc, j) => (
                        <li key={j}>{desc}</li>
                      ))}
                    </ul>
                  )}
                  {exp.achievements && exp.achievements.length > 0 && (
                    <div className="achievements">
                      <strong>Key Achievements:</strong>
                      <ul>
                        {exp.achievements.map((achievement, j) => (
                          <li key={j}>{achievement}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Education */}
          {sections.education && sections.education.length > 0 && (
            <div className="resume-section">
              <h4>{isATSResume ? 'EDUCATION' : 'Education'}</h4>
              {sections.education.map((edu, i) => (
                <div key={i} className="education-item">
                  <div className="edu-header">
                    <strong>{edu.degree}</strong>
                    {edu.year && <span className="edu-year">{edu.year}</span>}
                  </div>
                  <div className="edu-institution">{edu.institution}</div>
                  {edu.location && <div className="edu-location">{edu.location}</div>}
                  {edu.gpa && <div className="edu-gpa">GPA: {edu.gpa}</div>}
                  {edu.honors && <div className="edu-honors">{edu.honors}</div>}
                  {edu.details && <div className="edu-details">{edu.details}</div>}
                </div>
              ))}
            </div>
          )}

          {/* Projects */}
          {sections.projects && sections.projects.length > 0 && (
            <div className="resume-section">
              <h4>Projects</h4>
              {sections.projects.map((proj, i) => (
                <div key={i} className="project-item">
                  <strong>{proj.name}</strong>
                  <p>{proj.description}</p>
                  {proj.technologies && proj.technologies.length > 0 && (
                    <div className="skill-tags">
                      {proj.technologies.map((tech, j) => (
                        <span key={j} className="skill-tag">{tech}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Key Achievements */}
          {sections.key_achievements && sections.key_achievements.length > 0 && (
            <div className="resume-section">
              <h4>Key Achievements</h4>
              <ul>
                {sections.key_achievements.map((achievement, i) => (
                  <li key={i}>{achievement}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Certifications */}
          {sections.certifications && sections.certifications.length > 0 && (
            <div className="resume-section">
              <h4>Certifications</h4>
              {sections.certifications.map((cert, i) => (
                <div key={i} className="cert-item">
                  <strong>{cert.name}</strong>
                  {cert.issuer && <span> - {cert.issuer}</span>}
                  {cert.date && <span> ({cert.date})</span>}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <>
      <Navbar />
      <div className="document-generator-container">
        <div className="generator-layout">
          {/* Left Panel - Generator Form */}
          <div className="generator-panel">
            <div className="panel-header">
              <h1>📄 Resume Generator</h1>
              <p>Generate professional resumes from your profile</p>
            </div>

            {error && (
              <div className="alert alert-error">
                ⚠️ {error}
              </div>
            )}

            {success && (
              <div className="alert alert-success">
                ✅ {success}
              </div>
            )}

            <form onSubmit={handleGenerate} className="generator-form">
              <div className="form-group">
                <label>Target Role (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g., Software Engineer, Data Scientist"
                  value={formData.target_role}
                  onChange={(e) => setFormData({...formData, target_role: e.target.value})}
                />
                <small>Leave empty for general resume</small>
              </div>

              {/* Role-based recommendations */}
              {roleRecommendations && roleRecommendations.recommended && (
                <div className="recommendation-box">
                  <h4>💡 Recommendation for {formData.target_role}</h4>
                  <p>{roleRecommendations.recommended.reason}</p>
                  <div className="recommended-template">
                    <strong>Suggested Template:</strong> {roleRecommendations.recommended.template}
                  </div>
                  {roleRecommendations.recommended.keywords && (
                    <div className="keywords">
                      <strong>Key skills to highlight:</strong>
                      <div className="skill-tags">
                        {roleRecommendations.recommended.keywords.slice(0, 5).map((keyword, i) => (
                          <span key={i} className="skill-tag">{keyword}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* CV Upload Section */}
              <div className="form-group cv-upload-section">
                <label>
                  📎 Upload Your CV (Optional)
                  <span className="badge-ats">ATS</span>
                </label>
                <p className="help-text">
                  Upload a PDF resume to extract information and generate an ATS-optimized version
                </p>
                
                {!cvFile ? (
                  <div className="file-upload-area">
                    <input
                      type="file"
                      id="cv-file-input"
                      accept=".pdf"
                      onChange={handleFileSelect}
                      style={{ display: 'none' }}
                    />
                    <label htmlFor="cv-file-input" className="file-upload-label">
                      <span className="upload-icon">📄</span>
                      <span>Click to upload PDF</span>
                    </label>
                  </div>
                ) : (
                  <div className="file-selected">
                    <span className="file-icon">📄</span>
                    <span className="file-name">{cvFile.name}</span>
                    <button
                      type="button"
                      onClick={handleRemoveFile}
                      className="btn-remove-file"
                    >
                      ✕
                    </button>
                  </div>
                )}
              </div>

              {/* ATS Mode Toggle */}
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={useATSMode}
                    onChange={(e) => setUseATSMode(e.target.checked)}
                  />
                  <span>Generate ATS-Optimized Resume</span>
                  <span className="badge-ats">ATS</span>
                </label>
                <small>
                  Applicant Tracking System friendly format with keyword optimization
                </small>
              </div>

              <div className="form-group">
                <label>Template</label>
                <select
                  value={formData.template}
                  onChange={(e) => setFormData({...formData, template: e.target.value})}
                  disabled={useATSMode || cvFile}
                >
                  {Object.keys(templates).map(key => (
                    <option key={key} value={key}>
                      {key.charAt(0).toUpperCase() + key.slice(1)} - {templates[key]?.style}
                    </option>
                  ))}
                </select>
                {(useATSMode || cvFile) && (
                  <small className="template-override">
                    Template will be automatically selected based on role
                  </small>
                )}
              </div>

              <button type="submit" className="btn-generate" disabled={loading}>
                {loading ? '⏳ Generating...' : cvFile || useATSMode ? '✨ Generate ATS Resume' : '✨ Generate Resume'}
              </button>
            </form>

            {/* Saved Resumes List */}
            <div className="saved-documents">
              <h3>📂 Your Resumes ({resumes.length})</h3>
              {resumes.length === 0 ? (
                <p className="no-documents">No resumes yet. Generate your first one!</p>
              ) : (
                <div className="document-list">
                  {resumes.map(resume => (
                    <div key={resume.id} className="document-item">
                      <div className="document-info">
                        <strong>{resume.title}</strong>
                        <small>
                          {new Date(resume.created_at).toLocaleDateString()} • 
                          Version {resume.version} • 
                          {resume.template_name}
                        </small>
                      </div>
                      <div className="document-actions">
                        <button 
                          onClick={() => handleViewResume(resume.id)}
                          className="btn-icon"
                          title="View"
                        >
                          👁️
                        </button>
                        <button 
                          onClick={() => handleDeleteResume(resume.id)}
                          className="btn-icon btn-danger"
                          title="Delete"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Panel - Preview */}
          <div className="preview-panel">
            {showPreview && selectedResume ? (
              renderResumePreview()
            ) : (
              <div className="preview-placeholder">
                <div className="placeholder-content">
                  <span className="placeholder-icon">📄</span>
                  <h3>Resume Preview</h3>
                  <p>Generate or select a resume to see the preview</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default ResumeGenerator;
