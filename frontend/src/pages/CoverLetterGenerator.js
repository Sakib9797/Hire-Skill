import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import documentService from '../services/documentService';
import '../styles/DocumentGenerator.css';

const CoverLetterGenerator = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [coverLetters, setCoverLetters] = useState([]);
  const [tones, setTones] = useState({});
  const [selectedLetter, setSelectedLetter] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [generationType, setGenerationType] = useState('standard'); // 'standard' or 'custom'

  // Form state
  const [formData, setFormData] = useState({
    company_name: '',
    job_title: '',
    job_description: '',
    tone: 'professional',
    custom_prompt: ''
  });

  useEffect(() => {
    loadTones();
    loadCoverLetters();
  }, []);

  const loadTones = async () => {
    try {
      const response = await documentService.getTones();
      setTones(response.data.tones);
    } catch (err) {
      console.error('Error loading tones:', err);
    }
  };

  const loadCoverLetters = async () => {
    try {
      const response = await documentService.getCoverLetters();
      setCoverLetters(response.data.cover_letters || []);
    } catch (err) {
      console.error('Error loading cover letters:', err);
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      let response;
      
      if (generationType === 'custom') {
        if (!formData.custom_prompt) {
          setError('Custom prompt is required');
          setLoading(false);
          return;
        }
        
        response = await documentService.generateCustomCoverLetter({
          custom_prompt: formData.custom_prompt,
          company_name: formData.company_name || undefined,
          job_title: formData.job_title || undefined,
          tone: formData.tone
        });
      } else {
        if (!formData.company_name || !formData.job_title) {
          setError('Company name and job title are required');
          setLoading(false);
          return;
        }
        
        response = await documentService.generateCoverLetter({
          company_name: formData.company_name,
          job_title: formData.job_title,
          job_description: formData.job_description,
          tone: formData.tone
        });
      }
      
      setSuccess('Cover letter generated successfully!');
      setSelectedLetter(response.data.cover_letter);
      setShowPreview(true);
      loadCoverLetters(); // Reload list
      
      // Reset form
      setFormData({
        company_name: '',
        job_title: '',
        job_description: '',
        tone: 'professional',
        custom_prompt: ''
      });
    } catch (err) {
      console.error('Error generating cover letter:', err);
      setError(err.message || 'Failed to generate cover letter. Please complete your profile first.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewLetter = async (letterId) => {
    try {
      const response = await documentService.getCoverLetter(letterId);
      setSelectedLetter(response.data.cover_letter);
      setShowPreview(true);
    } catch (err) {
      setError('Failed to load cover letter');
    }
  };

  const handleDeleteLetter = async (letterId) => {
    if (!window.confirm('Are you sure you want to delete this cover letter?')) {
      return;
    }

    try {
      await documentService.deleteCoverLetter(letterId);
      setSuccess('Cover letter deleted successfully');
      loadCoverLetters();
      if (selectedLetter?.id === letterId) {
        setSelectedLetter(null);
        setShowPreview(false);
      }
    } catch (err) {
      setError('Failed to delete cover letter');
    }
  };

  const handleCopyToClipboard = () => {
    if (!selectedLetter) return;
    
    navigator.clipboard.writeText(selectedLetter.content);
    setSuccess('Cover letter copied to clipboard!');
    setTimeout(() => setSuccess(''), 3000);
  };

  const handleDownloadText = () => {
    if (!selectedLetter) return;
    
    const blob = new Blob([selectedLetter.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `cover-letter-${selectedLetter.id}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <>
      <Navbar />
      <div className="document-generator-container">
        <div className="generator-layout">
          {/* Left Panel - Generator Form */}
          <div className="generator-panel">
            <div className="panel-header">
              <h1>✉️ Cover Letter Generator</h1>
              <p>Create personalized cover letters for job applications</p>
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

            {/* Generation Type Toggle */}
            <div className="generation-type-toggle">
              <button
                className={generationType === 'standard' ? 'active' : ''}
                onClick={() => setGenerationType('standard')}
              >
                📝 Standard
              </button>
              <button
                className={generationType === 'custom' ? 'active' : ''}
                onClick={() => setGenerationType('custom')}
              >
                🎨 Custom Prompt
              </button>
            </div>

            <form onSubmit={handleGenerate} className="generator-form">
              {generationType === 'standard' ? (
                <>
                  <div className="form-group">
                    <label>Company Name *</label>
                    <input
                      type="text"
                      placeholder="e.g., Google, Microsoft"
                      value={formData.company_name}
                      onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Job Title *</label>
                    <input
                      type="text"
                      placeholder="e.g., Software Engineer, Product Manager"
                      value={formData.job_title}
                      onChange={(e) => setFormData({...formData, job_title: e.target.value})}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Job Description (Optional)</label>
                    <textarea
                      placeholder="Paste job description or key requirements..."
                      value={formData.job_description}
                      onChange={(e) => setFormData({...formData, job_description: e.target.value})}
                      rows="4"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="form-group">
                    <label>Custom Instructions *</label>
                    <textarea
                      placeholder="e.g., Emphasize my Python and leadership skills, mention my startup experience..."
                      value={formData.custom_prompt}
                      onChange={(e) => setFormData({...formData, custom_prompt: e.target.value})}
                      rows="4"
                      required
                    />
                    <small>Describe what you want to emphasize in your cover letter</small>
                  </div>

                  <div className="form-group">
                    <label>Company Name (Optional)</label>
                    <input
                      type="text"
                      placeholder="e.g., Google"
                      value={formData.company_name}
                      onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                    />
                  </div>

                  <div className="form-group">
                    <label>Job Title (Optional)</label>
                    <input
                      type="text"
                      placeholder="e.g., Senior Developer"
                      value={formData.job_title}
                      onChange={(e) => setFormData({...formData, job_title: e.target.value})}
                    />
                  </div>
                </>
              )}

              <div className="form-group">
                <label>Tone</label>
                <select
                  value={formData.tone}
                  onChange={(e) => setFormData({...formData, tone: e.target.value})}
                >
                  {Object.keys(tones).map(key => (
                    <option key={key} value={key}>
                      {key.charAt(0).toUpperCase() + key.slice(1)} - {tones[key]?.style}
                    </option>
                  ))}
                </select>
              </div>

              <button type="submit" className="btn-generate" disabled={loading}>
                {loading ? '⏳ Generating...' : '✨ Generate Cover Letter'}
              </button>
            </form>

            {/* Saved Cover Letters List */}
            <div className="saved-documents">
              <h3>📂 Your Cover Letters ({coverLetters.length})</h3>
              {coverLetters.length === 0 ? (
                <p className="no-documents">No cover letters yet. Generate your first one!</p>
              ) : (
                <div className="document-list">
                  {coverLetters.map(letter => (
                    <div key={letter.id} className="document-item">
                      <div className="document-info">
                        <strong>{letter.title}</strong>
                        <small>
                          {new Date(letter.created_at).toLocaleDateString()} • 
                          {letter.tone} • 
                          Version {letter.version}
                        </small>
                      </div>
                      <div className="document-actions">
                        <button 
                          onClick={() => handleViewLetter(letter.id)}
                          className="btn-icon"
                          title="View"
                        >
                          👁️
                        </button>
                        <button 
                          onClick={() => handleDeleteLetter(letter.id)}
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
            {showPreview && selectedLetter ? (
              <div className="cover-letter-preview">
                <div className="preview-header">
                  <h2>{selectedLetter.title}</h2>
                  <div className="preview-actions">
                    <button onClick={handleCopyToClipboard} className="btn-download">
                      📋 Copy
                    </button>
                    <button onClick={handleDownloadText} className="btn-download">
                      📥 Download
                    </button>
                    <button onClick={() => setShowPreview(false)} className="btn-close-preview">
                      ✕ Close
                    </button>
                  </div>
                </div>

                <div className="cover-letter-content">
                  <div className="letter-metadata">
                    {selectedLetter.company_name && (
                      <span><strong>Company:</strong> {selectedLetter.company_name}</span>
                    )}
                    {selectedLetter.job_title && (
                      <span><strong>Position:</strong> {selectedLetter.job_title}</span>
                    )}
                    <span><strong>Tone:</strong> {selectedLetter.tone}</span>
                  </div>
                  
                  <div className="letter-text">
                    {selectedLetter.content.split('\n').map((paragraph, index) => (
                      <p key={index}>{paragraph}</p>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="preview-placeholder">
                <div className="placeholder-content">
                  <span className="placeholder-icon">✉️</span>
                  <h3>Cover Letter Preview</h3>
                  <p>Generate or select a cover letter to see the preview</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default CoverLetterGenerator;
