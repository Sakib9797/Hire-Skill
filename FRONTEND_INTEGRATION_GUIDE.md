# Frontend Integration Guide - Module 3

## Quick Start

### 1. Update Document Service

Update `frontend/src/services/documentService.js` to include new endpoints:

```javascript
// Add these methods to your existing documentService

/**
 * Generate ATS-compliant resume with job description
 */
generateResume: async (data) => {
  const response = await api.post('/resume/generate', {
    target_role: data.target_role,
    job_description: data.job_description,
    template: data.template || 'ats_professional'
  });
  return response.data;
},

/**
 * Download resume as PDF
 */
downloadResumePDF: async (resumeId) => {
  const response = await api.get(`/resume/${resumeId}/download`, {
    responseType: 'blob'
  });
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `resume_${resumeId}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
},

/**
 * Get resume versions
 */
getResumeVersions: async (userId) => {
  const response = await api.get(`/resume/versions/${userId}`);
  return response.data;
}
```

### 2. Update ResumeGenerator Component

Update `frontend/src/pages/ResumeGenerator.js`:

```javascript
import React, { useState } from 'react';
import documentService from '../services/documentService';

function ResumeGenerator() {
  const [loading, setLoading] = useState(false);
  const [resume, setResume] = useState(null);
  const [formData, setFormData] = useState({
    target_role: '',
    job_description: ''
  });

  const handleGenerateResume = async () => {
    setLoading(true);
    try {
      const response = await documentService.generateResume(formData);
      setResume(response.data.resume);
      
      // Show success message
      alert(`Resume generated successfully! 
        ${response.data.resume.keywords_matched ? 
          `Match Score: ${response.data.resume.keywords_matched.match_score}%` : 
          ''}`);
    } catch (error) {
      alert('Error: ' + (error.message || 'Failed to generate resume'));
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!resume?.id) return;
    
    try {
      await documentService.downloadResumePDF(resume.id);
    } catch (error) {
      alert('Error downloading PDF: ' + error.message);
    }
  };

  return (
    <div className="resume-generator">
      <h2>Generate ATS-Compliant Resume</h2>
      
      <div className="form-group">
        <label>Target Role (Optional)</label>
        <input
          type="text"
          value={formData.target_role}
          onChange={(e) => setFormData({...formData, target_role: e.target.value})}
          placeholder="e.g., Software Engineer"
          className="form-control"
        />
        <small>Specify the role you're targeting for customization</small>
      </div>
      
      <div className="form-group">
        <label>Job Description (Optional but Recommended)</label>
        <textarea
          value={formData.job_description}
          onChange={(e) => setFormData({...formData, job_description: e.target.value})}
          placeholder="Paste the job description here. Our AI will extract keywords and optimize your resume for ATS systems."
          rows="10"
          className="form-control"
        />
        <small>
          💡 Tip: Include the job description for keyword optimization and better ATS matching!
        </small>
      </div>
      
      <button 
        onClick={handleGenerateResume} 
        disabled={loading}
        className="btn btn-primary"
      >
        {loading ? (
          <>
            <span className="spinner"></span> Generating Resume...
          </>
        ) : (
          '✨ Generate ATS-Optimized Resume'
        )}
      </button>
      
      {resume && (
        <div className="resume-result">
          <div className="result-header">
            <h3>✅ Resume Generated!</h3>
            <span className="badge ats-badge">ATS Optimized</span>
          </div>
          
          <div className="result-meta">
            <p><strong>Title:</strong> {resume.title}</p>
            <p><strong>Target Role:</strong> {resume.target_role || 'General'}</p>
            
            {resume.keywords_matched && (
              <div className="keyword-match">
                <p><strong>Keyword Match Score:</strong></p>
                <div className="match-score">
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{width: `${resume.keywords_matched.match_score}%`}}
                    ></div>
                  </div>
                  <span>{resume.keywords_matched.match_score}%</span>
                </div>
                
                {resume.keywords_matched.matched_skills?.length > 0 && (
                  <div className="matched-skills">
                    <strong>Matched Skills:</strong>
                    <div className="skill-tags">
                      {resume.keywords_matched.matched_skills.map((skill, idx) => (
                        <span key={idx} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
          
          <div className="result-actions">
            <button onClick={handleDownloadPDF} className="btn btn-success">
              📄 Download PDF
            </button>
            <button 
              onClick={() => {/* Navigate to edit */}} 
              className="btn btn-secondary"
            >
              ✏️ Edit Resume
            </button>
          </div>
          
          <div className="resume-preview">
            <h4>Resume Content Preview</h4>
            
            {/* Personal Info */}
            <div className="section">
              <h5>CONTACT INFORMATION</h5>
              <p>{resume.content.personal_info?.full_name}</p>
              <p>{resume.content.personal_info?.email} | {resume.content.personal_info?.phone}</p>
              <p>{resume.content.personal_info?.location}</p>
            </div>
            
            {/* Summary */}
            {resume.content.summary && (
              <div className="section">
                <h5>SUMMARY</h5>
                <p>{resume.content.summary}</p>
              </div>
            )}
            
            {/* Skills */}
            {resume.content.skills && (
              <div className="section">
                <h5>SKILLS</h5>
                {resume.content.skills.technical?.length > 0 && (
                  <p><strong>Technical:</strong> {resume.content.skills.technical.join(', ')}</p>
                )}
                {resume.content.skills.soft?.length > 0 && (
                  <p><strong>Soft Skills:</strong> {resume.content.skills.soft.join(', ')}</p>
                )}
                {resume.content.skills.tools?.length > 0 && (
                  <p><strong>Tools:</strong> {resume.content.skills.tools.join(', ')}</p>
                )}
              </div>
            )}
            
            {/* Work Experience */}
            {resume.content.work_experience?.length > 0 && (
              <div className="section">
                <h5>WORK EXPERIENCE</h5>
                {resume.content.work_experience.map((exp, idx) => (
                  <div key={idx} className="experience-item">
                    <p><strong>{exp.title}</strong> - {exp.company}</p>
                    <p className="duration">{exp.duration}</p>
                    <ul>
                      {exp.responsibilities?.map((resp, ridx) => (
                        <li key={ridx}>{resp}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
            
            {/* Education */}
            {resume.content.education?.length > 0 && (
              <div className="section">
                <h5>EDUCATION</h5>
                {resume.content.education.map((edu, idx) => (
                  <div key={idx}>
                    <p><strong>{edu.degree}</strong> - {edu.institution}</p>
                    <p>{edu.year}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ResumeGenerator;
```

### 3. Add Styling

Add to `frontend/src/styles/DocumentGenerator.css`:

```css
.resume-generator {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

small {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 12px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.btn-success {
  background-color: #28a745;
  color: white;
  margin-right: 10px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.resume-result {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.ats-badge {
  padding: 4px 12px;
  background-color: #28a745;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.keyword-match {
  margin-top: 15px;
  padding: 15px;
  background-color: white;
  border-radius: 4px;
}

.match-score {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.score-bar {
  flex: 1;
  height: 24px;
  background-color: #e9ecef;
  border-radius: 12px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.5s ease;
}

.matched-skills {
  margin-top: 15px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.skill-tag {
  padding: 4px 12px;
  background-color: #007bff;
  color: white;
  border-radius: 16px;
  font-size: 12px;
}

.result-actions {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.resume-preview {
  margin-top: 20px;
  padding: 20px;
  background-color: white;
  border-radius: 4px;
}

.section {
  margin-bottom: 20px;
}

.section h5 {
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 10px;
  border-bottom: 2px solid #000;
  padding-bottom: 5px;
}

.experience-item {
  margin-bottom: 15px;
}

.duration {
  color: #666;
  font-size: 14px;
  margin: 5px 0;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### 4. Usage Flow

```
1. User fills in Target Role (optional)
2. User pastes Job Description (optional but recommended)
3. Click "Generate ATS-Optimized Resume"
4. Backend:
   - Extracts keywords from job description
   - Calls LLM to generate resume
   - Validates JSON schema
   - Returns resume with match score
5. Frontend displays:
   - Resume preview
   - Keyword match score
   - Matched skills
   - Download PDF button
6. User can download PDF
```

### 5. API Error Handling

```javascript
try {
  const response = await documentService.generateResume(formData);
  // Success
} catch (error) {
  // Handle specific errors
  if (error.status === 404) {
    alert('User profile not found. Please complete your profile first.');
  } else if (error.status === 400) {
    alert('Invalid input: ' + error.message);
  } else if (error.status === 500) {
    alert('Server error. Our AI service may be temporarily unavailable.');
  } else {
    alert('Unexpected error: ' + error.message);
  }
}
```

### 6. Testing

```javascript
// Mock data for testing without backend
const mockResume = {
  id: 1,
  title: "Resume - Software Engineer",
  target_role: "Software Engineer",
  is_ats_optimized: true,
  keywords_matched: {
    match_score: 85.5,
    matched_skills: ["Python", "Django", "REST API"]
  },
  content: {
    personal_info: {
      full_name: "John Doe",
      email: "john@example.com",
      phone: "+1234567890",
      location: "San Francisco, CA"
    },
    summary: "Experienced software engineer with 5+ years of expertise...",
    skills: {
      technical: ["Python", "Django", "PostgreSQL"],
      soft: ["Problem-solving", "Communication"],
      tools: ["Git", "Docker"]
    },
    work_experience: [{
      title: "Software Engineer",
      company: "Tech Corp",
      duration: "2020-Present",
      responsibilities: [
        "Developed REST APIs",
        "Improved performance by 40%"
      ]
    }],
    education: [{
      degree: "B.S. Computer Science",
      institution: "UC Berkeley",
      year: "2019"
    }]
  }
};
```

## Next Steps

1. Update `documentService.js` with new methods
2. Update `ResumeGenerator.js` component
3. Add CSS styles
4. Test with backend API
5. Add error handling
6. Implement PDF preview (optional)
7. Add resume versioning UI (optional)

## Additional Features to Consider

- Resume comparison view
- Version history timeline
- Keyword highlighting in preview
- Real-time ATS score as user types job description
- Cover letter generation UI
- Template selection UI
- Export to multiple formats
