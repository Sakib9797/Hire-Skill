import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import careerService from '../services/careerService';
import '../styles/CareerRecommendations.css';

const CareerRecommendations = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [loadingSkillGap, setLoadingSkillGap] = useState(false);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await careerService.getRecommendations(5);
      
      if (response.data && response.data.recommendations) {
        setRecommendations(response.data.recommendations);
      } else {
        setError('No recommendations available. Please add skills to your profile.');
      }
    } catch (err) {
      console.error('Error loading recommendations:', err);
      if (err.error && typeof err.error === 'object' && err.error.message) {
        setError(err.error.message);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Failed to load career recommendations. Please add skills to your profile.');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadSkillGap = async (careerRole) => {
    try {
      setLoadingSkillGap(true);
      const response = await careerService.getSkillGap(careerRole);
      setSkillGap(response.data);
      setSelectedCareer(careerRole);
    } catch (err) {
      console.error('Error loading skill gap:', err);
      alert('Failed to load skill gap analysis');
    } finally {
      setLoadingSkillGap(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return '#28a745';
    if (score >= 50) return '#ffc107';
    return '#dc3545';
  };

  const getGrowthBadgeClass = (rate) => {
    const rateMap = {
      'Very High': 'badge-very-high',
      'High': 'badge-high',
      'Medium': 'badge-medium',
      'Low': 'badge-low'
    };
    return rateMap[rate] || 'badge-medium';
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="career-container">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Loading AI-powered career recommendations...</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="career-container">
        <div className="career-header">
          <h1>🤖 AI Career Recommendations</h1>
          <p>Personalized career paths based on your skills and interests</p>
          <button 
            className="btn-refresh" 
            onClick={loadRecommendations}
            disabled={loading}
          >
            🔄 Refresh Recommendations
          </button>
        </div>

        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button 
              className="btn-link"
              onClick={() => navigate('/dashboard')}
            >
              Go to Profile to Add Skills
            </button>
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="recommendations-list">
            {recommendations.map((career, index) => (
              <div key={index} className="career-card">
                <div className="career-card-header">
                  <div>
                    <h3>{career.role}</h3>
                    <span className="category-badge">{career.category}</span>
                    <span className={`growth-badge ${getGrowthBadgeClass(career.growth_rate)}`}>
                      {career.growth_rate} Growth
                    </span>
                  </div>
                  <div className="career-scores">
                    <div className="score-item">
                      <div 
                        className="score-circle"
                        style={{ borderColor: getScoreColor(career.similarity_score) }}
                      >
                        <span style={{ color: getScoreColor(career.similarity_score) }}>
                          {career.similarity_score.toFixed(0)}%
                        </span>
                      </div>
                      <small>Match Score</small>
                    </div>
                    <div className="score-item">
                      <div 
                        className="score-circle"
                        style={{ borderColor: getScoreColor(career.skill_match_percentage) }}
                      >
                        <span style={{ color: getScoreColor(career.skill_match_percentage) }}>
                          {career.skill_match_percentage.toFixed(0)}%
                        </span>
                      </div>
                      <small>Skills Match</small>
                    </div>
                  </div>
                </div>

                <p className="career-description">{career.description}</p>

                <div className="career-info">
                  <div className="info-item">
                    <strong>💰 Salary Range:</strong>
                    <span>{career.average_salary}</span>
                  </div>
                </div>

                <div className="career-reasoning">
                  <strong>💡 Why this career?</strong>
                  <p>{career.reasoning}</p>
                </div>

                <div className="skill-summary">
                  <div className="skill-group">
                    <strong>✅ Skills You Have:</strong>
                    <div className="skill-tags">
                      {career.skill_gaps.matched_required.slice(0, 5).map((skill, i) => (
                        <span key={i} className="skill-tag matched">{skill}</span>
                      ))}
                      {career.skill_gaps.matched_required.length > 5 && (
                        <span className="skill-tag">+{career.skill_gaps.matched_required.length - 5} more</span>
                      )}
                    </div>
                  </div>

                  {career.skill_gaps.missing_required.length > 0 && (
                    <div className="skill-group">
                      <strong>📚 Skills to Learn:</strong>
                      <div className="skill-tags">
                        {career.skill_gaps.missing_required.slice(0, 5).map((skill, i) => (
                          <span key={i} className="skill-tag missing">{skill}</span>
                        ))}
                        {career.skill_gaps.missing_required.length > 5 && (
                          <span className="skill-tag">+{career.skill_gaps.missing_required.length - 5} more</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <button
                  className="btn-detail"
                  onClick={() => loadSkillGap(career.role)}
                  disabled={loadingSkillGap}
                >
                  {loadingSkillGap && selectedCareer === career.role 
                    ? '⏳ Loading...' 
                    : '🗺️ View Learning Roadmap'
                  }
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Skill Gap Modal */}
        {skillGap && (
          <div className="modal-overlay" onClick={() => setSkillGap(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>🗺️ Learning Roadmap: {skillGap.career}</h2>
                <button className="btn-close" onClick={() => setSkillGap(null)}>✕</button>
              </div>

              <div className="modal-body">
                <div className="roadmap-summary">
                  <div className="summary-item">
                    <strong>Current Match:</strong>
                    <span className="highlight">{skillGap.current_match}</span>
                  </div>
                  <div className="summary-item">
                    <strong>Time to Ready:</strong>
                    <span className="highlight">{skillGap.estimated_time_to_ready}</span>
                  </div>
                </div>

                {skillGap.skills_you_have && skillGap.skills_you_have.length > 0 && (
                  <div className="roadmap-section">
                    <h3>✅ Skills You Already Have</h3>
                    <div className="skill-tags">
                      {skillGap.skills_you_have.map((skill, i) => (
                        <span key={i} className="skill-tag matched">{skill}</span>
                      ))}
                    </div>
                  </div>
                )}

                {skillGap.learning_path && skillGap.learning_path.length > 0 && (
                  <div className="roadmap-section">
                    <h3>📚 Your Learning Path</h3>
                    {skillGap.learning_path.map((phase, index) => (
                      <div key={index} className="learning-phase">
                        <div className="phase-header">
                          <h4>{phase.phase}</h4>
                          <span className={`priority-badge priority-${phase.priority.toLowerCase()}`}>
                            {phase.priority} Priority
                          </span>
                          <span className="timeline-badge">{phase.timeline}</span>
                        </div>
                        <div className="skill-tags">
                          {phase.skills.map((skill, i) => (
                            <span key={i} className="skill-tag learn">{skill}</span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {skillGap.bonus_skills && skillGap.bonus_skills.length > 0 && (
                  <div className="roadmap-section">
                    <h3>⭐ Bonus Skills (Optional)</h3>
                    <div className="skill-tags">
                      {skillGap.bonus_skills.map((skill, i) => (
                        <span key={i} className="skill-tag optional">{skill}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="modal-footer">
                <button className="btn-primary" onClick={() => navigate('/dashboard')}>
                  Update My Skills
                </button>
                <button className="btn-secondary" onClick={() => setSkillGap(null)}>
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default CareerRecommendations;
