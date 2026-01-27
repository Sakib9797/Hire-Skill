import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import Navbar from '../components/Navbar';
import userService from '../services/userService';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user, updateUser } = useAuth();
  const { toggleTheme } = useTheme();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
    phone: '',
    location: '',
    skills: [],
    interests: [],
  });
  const [newSkill, setNewSkill] = useState('');
  const [newInterest, setNewInterest] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const profileData = await userService.getProfile();
      setProfile(profileData);
      setFormData({
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        bio: profileData.profile?.bio || '',
        phone: profileData.profile?.phone || '',
        location: profileData.profile?.location || '',
        skills: profileData.profile?.skills || [],
        interests: profileData.profile?.interests || [],
      });
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const addSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData({
        ...formData,
        skills: [...formData.skills, newSkill.trim()],
      });
      setNewSkill('');
    }
  };

  const removeSkill = (skill) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((s) => s !== skill),
    });
  };

  const addInterest = () => {
    if (newInterest.trim() && !formData.interests.includes(newInterest.trim())) {
      setFormData({
        ...formData,
        interests: [...formData.interests, newInterest.trim()],
      });
      setNewInterest('');
    }
  };

  const removeInterest = (interest) => {
    setFormData({
      ...formData,
      interests: formData.interests.filter((i) => i !== interest),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const updatedUser = await userService.updateProfile(formData);
      setProfile(updatedUser);
      updateUser(updatedUser);
      setSuccess('Profile updated successfully!');
      setEditing(false);
    } catch (err) {
      setError(err.message || 'Failed to update profile');
    }
  };

  const handleThemeChange = async () => {
    const newTheme = toggleTheme();
    try {
      await userService.updateTheme(newTheme);
    } catch (err) {
      console.error('Failed to save theme preference:', err);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="dashboard-container">
          <div className="dashboard-content">
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
              Loading profile...
            </p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-content">
          <div className="dashboard-header">
            <h1>Welcome back, {profile?.first_name || user?.email}!</h1>
            <p>Manage your profile and preferences</p>
          </div>

          {error && (
            <div className="card" style={{ background: 'var(--danger-color)', color: 'white' }}>
              {error}
            </div>
          )}

          {success && (
            <div className="card" style={{ background: 'var(--success-color)', color: 'white' }}>
              {success}
            </div>
          )}

          {/* Account Info Card */}
          <div className="card">
            <div className="card-header">
              <h2>Account Information</h2>
              <span className={`badge badge-${profile?.is_active ? 'success' : 'danger'}`}>
                {profile?.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="card-body">
              <div className="info-row">
                <span className="info-label">Email</span>
                <span className="info-value">{profile?.email}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Role</span>
                <span className="info-value">
                  <span className="badge badge-primary">
                    {profile?.role?.toUpperCase()}
                  </span>
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">Member Since</span>
                <span className="info-value">
                  {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Profile Card */}
          <div className="card">
            <div className="card-header">
              <h2>Profile Details</h2>
              {!editing ? (
                <button className="btn btn-primary" onClick={() => setEditing(true)}>
                  Edit Profile
                </button>
              ) : (
                <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                  <button className="btn btn-secondary" onClick={() => setEditing(false)}>
                    Cancel
                  </button>
                  <button className="btn btn-primary" onClick={handleSubmit}>
                    Save Changes
                  </button>
                </div>
              )}
            </div>

            {editing ? (
              <form className="card-body" onSubmit={handleSubmit}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-md)' }}>
                  <div className="form-group">
                    <label htmlFor="first_name">First Name</label>
                    <input
                      type="text"
                      id="first_name"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      placeholder="Enter first name"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="last_name">Last Name</label>
                    <input
                      type="text"
                      id="last_name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      placeholder="Enter last name"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="bio">Bio</label>
                  <textarea
                    id="bio"
                    name="bio"
                    value={formData.bio}
                    onChange={handleChange}
                    placeholder="Tell us about yourself"
                    rows="4"
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-md)' }}>
                  <div className="form-group">
                    <label htmlFor="phone">Phone</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder="Enter phone number"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="location">Location</label>
                    <input
                      type="text"
                      id="location"
                      name="location"
                      value={formData.location}
                      onChange={handleChange}
                      placeholder="Enter location"
                    />
                  </div>
                </div>

                {/* Skills Section */}
                <div className="form-group">
                  <label>Skills</label>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
                    <input
                      type="text"
                      value={newSkill}
                      onChange={(e) => setNewSkill(e.target.value)}
                      placeholder="Add a skill"
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                    />
                    <button type="button" className="btn btn-primary" onClick={addSkill}>
                      Add
                    </button>
                  </div>
                  <div className="skills-list">
                    {formData.skills.map((skill) => (
                      <div key={skill} className="skill-tag">
                        {skill}
                        <button
                          type="button"
                          onClick={() => removeSkill(skill)}
                          style={{
                            marginLeft: 'var(--spacing-sm)',
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            color: 'var(--text-secondary)',
                            fontSize: '1.2rem',
                            padding: 0,
                            lineHeight: 1,
                          }}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Interests Section */}
                <div className="form-group">
                  <label>Interests</label>
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
                    <input
                      type="text"
                      value={newInterest}
                      onChange={(e) => setNewInterest(e.target.value)}
                      placeholder="Add an interest"
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addInterest())}
                    />
                    <button type="button" className="btn btn-primary" onClick={addInterest}>
                      Add
                    </button>
                  </div>
                  <div className="skills-list">
                    {formData.interests.map((interest) => (
                      <div key={interest} className="skill-tag">
                        {interest}
                        <button
                          type="button"
                          onClick={() => removeInterest(interest)}
                          style={{
                            marginLeft: 'var(--spacing-sm)',
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            color: 'var(--text-secondary)',
                            fontSize: '1.2rem',
                            padding: 0,
                            lineHeight: 1,
                          }}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </form>
            ) : (
              <div className="card-body">
                <div className="info-row">
                  <span className="info-label">Name</span>
                  <span className="info-value">
                    {profile?.first_name || profile?.last_name
                      ? `${profile.first_name || ''} ${profile.last_name || ''}`.trim()
                      : 'Not set'}
                  </span>
                </div>
                <div className="info-row">
                  <span className="info-label">Bio</span>
                  <span className="info-value">{profile?.profile?.bio || 'Not set'}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Phone</span>
                  <span className="info-value">{profile?.profile?.phone || 'Not set'}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Location</span>
                  <span className="info-value">{profile?.profile?.location || 'Not set'}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Skills</span>
                  <div className="info-value">
                    {profile?.profile?.skills?.length > 0 ? (
                      <div className="skills-list" style={{ justifyContent: 'flex-end' }}>
                        {profile.profile.skills.map((skill) => (
                          <span key={skill} className="skill-tag">
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      'No skills added'
                    )}
                  </div>
                </div>
                <div className="info-row">
                  <span className="info-label">Interests</span>
                  <div className="info-value">
                    {profile?.profile?.interests?.length > 0 ? (
                      <div className="skills-list" style={{ justifyContent: 'flex-end' }}>
                        {profile.profile.interests.map((interest) => (
                          <span key={interest} className="skill-tag">
                            {interest}
                          </span>
                        ))}
                      </div>
                    ) : (
                      'No interests added'
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
