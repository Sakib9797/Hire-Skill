import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import salaryService from '../services/salaryService';
import '../styles/InterviewPrep.css';

const CATEGORY_COLORS = {
  'Technical Skills':    '#4f46e5',
  'Problem-Solving':     '#0891b2',
  'Problem Solving':     '#0891b2',
  'System Design':       '#059669',
  'Behavioral':          '#d97706',
  'Behavioral (STAR)':   '#d97706',
  'Teamwork':            '#7c3aed',
  'Past Experience':     '#db2777',
  'Handling Failure':    '#db2777',
  'Domain Knowledge':    '#0369a1',
  'Career Goals':        '#65a30d',
  'Leadership':          '#b45309',
  'Communication':       '#0d9488',
  'Coding & Algorithms': '#6d28d9',
  'Culture Fit':         '#e11d48',
  'General':             '#6b7280',
};

const InterviewPrep = () => {
  const [form, setForm] = useState({
    job_title: '',
    job_description: '',
    resume_text: '',
  });
  const [questions, setQuestions]     = useState([]);
  const [jobTitle, setJobTitle]       = useState('');
  const [questionSource, setQuestionSource] = useState('');
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState('');
  const [openIdx, setOpenIdx]         = useState(null);
  const [showAnswers, setShowAnswers] = useState({});

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!form.job_title && !form.job_description) {
      setError('Please enter a job title or job description.'); return;
    }
    setLoading(true); setError(''); setQuestions([]); setOpenIdx(null); setShowAnswers({}); setQuestionSource('');
    try {
      const res = await salaryService.generateInterviewQuestions({
        job_title:       form.job_title,
        job_description: form.job_description,
        resume_text:     form.resume_text,
      });
      const data = res.data || res;
      setQuestions(data.questions || []);
      setJobTitle(data.job_title || form.job_title);
      setQuestionSource(data.source || '');
    } catch (err) {
      setError(err?.data?.message || err?.message || 'Failed to generate questions. Please ensure the AI service is configured.');
    } finally {
      setLoading(false);
    }
  };

  const toggleAnswer = (i) => setShowAnswers(prev => ({ ...prev, [i]: !prev[i] }));

  const colorFor = (cat) => CATEGORY_COLORS[cat] || CATEGORY_COLORS.General;

  return (
    <>
      <Navbar />
      <div className="interview-page">
        <div className="interview-header">
          <h1>🎯 Interview Prep</h1>
          <p>AI-generated interview questions + model answers tailored to the specific role and your background.</p>
        </div>

        <div className="interview-content">
          {/* ── Form ── */}
          <form className="interview-form card" onSubmit={handleGenerate}>
            <h2>Job Details</h2>

            <div className="form-group">
              <label>Job Title *</label>
              <input
                type="text"
                placeholder="e.g. Senior Machine Learning Engineer"
                value={form.job_title}
                onChange={e => setForm(f => ({ ...f, job_title: e.target.value }))}
              />
            </div>

            <div className="form-group">
              <label>Job Description <span className="optional">(recommended)</span></label>
              <textarea
                rows={6}
                placeholder="Paste the full job description here for more targeted questions…"
                value={form.job_description}
                onChange={e => setForm(f => ({ ...f, job_description: e.target.value }))}
              />
            </div>

            <div className="form-group">
              <label>Your Resume / Key Skills <span className="optional">(optional — personalises answers)</span></label>
              <textarea
                rows={4}
                placeholder="Paste a summary of your experience, skills, or resume text…"
                value={form.resume_text}
                onChange={e => setForm(f => ({ ...f, resume_text: e.target.value }))}
              />
            </div>

            {error && <div className="alert-error">{error}</div>}

            <button type="submit" className="btn-generate" disabled={loading}>
              {loading ? '⏳ Generating Questions…' : '🎯 Generate Interview Questions'}
            </button>
          </form>

          {/* ── Questions ── */}
          {loading && (
            <div className="card loading-card">
              <div className="spinner" />
              <p>The AI is crafting your personalised questions…</p>
            </div>
          )}

          {questions.length > 0 && (
            <div className="questions-section">
              <div className="questions-header">
                <h2>📋 Interview Questions for <em>{jobTitle}</em></h2>
                <div className="questions-meta">
                  <span className="q-count">{questions.length} questions</span>
                  {questionSource && (
                    <span className={`q-source-badge ${questionSource}`}>
                      {questionSource === 'llm' ? '🤖 AI-Generated' : '📚 Expert Question Bank'}
                    </span>
                  )}
                </div>
              </div>

              <div className="questions-tip">
                💡 Tip: Click a question to expand it. Review the model answer after preparing your own.
              </div>

              <div className="questions-list">
                {questions.map((q, i) => (
                  <div key={i} className={`question-card ${openIdx === i ? 'open' : ''}`}
                    style={{ '--cat-color': colorFor(q.category) }}>
                    <button className="question-header" onClick={() => setOpenIdx(openIdx === i ? null : i)}>
                      <div className="q-left">
                        <span className="q-number">Q{q.number || i + 1}</span>
                        <span className="q-category" style={{ background: colorFor(q.category) }}>
                          {q.category || 'General'}
                        </span>
                        <span className="q-text">{q.question}</span>
                      </div>
                      <span className="q-chevron">{openIdx === i ? '▲' : '▼'}</span>
                    </button>

                    {openIdx === i && (
                      <div className="question-body">
                        {q.what_they_want && (
                          <div className="what-they-want">
                            <strong>🔍 What they're looking for:</strong>
                            <p>{q.what_they_want}</p>
                          </div>
                        )}
                        <button className="btn-show-answer" onClick={() => toggleAnswer(i)}>
                          {showAnswers[i] ? '🙈 Hide Model Answer' : '💡 Show Model Answer'}
                        </button>
                        {showAnswers[i] && q.model_answer && (
                          <div className="model-answer">
                            <strong>Model Answer:</strong>
                            <p>{q.model_answer}</p>
                          </div>
                        )}
                        {q.source && (
                          <div className="question-source">
                            <span>📖 Source: {q.source}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="prep-tips card">
                <h3>🏆 Interview Tips</h3>
                <ul>
                  <li>Use the <strong>STAR method</strong> (Situation, Task, Action, Result) for behavioral questions.</li>
                  <li>Prepare 2-3 specific examples from past projects for technical questions.</li>
                  <li>Research the company's tech stack and recent news before the interview.</li>
                  <li>Ask thoughtful questions at the end — it shows genuine interest.</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default InterviewPrep;
