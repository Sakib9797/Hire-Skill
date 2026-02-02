import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const jobService = {
  /**
   * Initialize job database
   */
  initializeJobs: async () => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/jobs/initialize`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Get matched jobs for user
   */
  getMatchedJobs: async (filters = {}) => {
    const token = localStorage.getItem('token');
    const params = new URLSearchParams();
    
    if (filters.role) params.append('role', filters.role);
    if (filters.location) params.append('location', filters.location);
    if (filters.experience_level) params.append('experience_level', filters.experience_level);
    if (filters.work_type) params.append('work_type', filters.work_type);
    if (filters.job_type) params.append('job_type', filters.job_type);
    if (filters.limit) params.append('limit', filters.limit);
    
    const response = await axios.get(
      `${API_URL}/jobs/match?${params.toString()}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Search jobs
   */
  searchJobs: async (query, filters = {}, limit = 50, offset = 0) => {
    const params = new URLSearchParams();
    
    if (query) params.append('q', query);
    if (filters.location) params.append('location', filters.location);
    if (filters.experience_level) params.append('experience_level', filters.experience_level);
    if (filters.work_type) params.append('work_type', filters.work_type);
    if (filters.job_type) params.append('job_type', filters.job_type);
    if (filters.min_salary) params.append('min_salary', filters.min_salary);
    params.append('limit', limit);
    params.append('offset', offset);
    
    const response = await axios.get(`${API_URL}/jobs/search?${params.toString()}`);
    return response.data;
  },

  /**
   * Get specific job
   */
  getJob: async (jobId) => {
    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    
    const response = await axios.get(`${API_URL}/jobs/${jobId}`, { headers });
    return response.data;
  },

  /**
   * Save job for later
   */
  saveJob: async (jobId) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/jobs/${jobId}/save`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Apply to job
   */
  applyToJob: async (jobId, data = {}) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/jobs/${jobId}/apply`,
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Get user applications
   */
  getUserApplications: async (status = null) => {
    const token = localStorage.getItem('token');
    const params = status ? `?status=${status}` : '';
    
    const response = await axios.get(
      `${API_URL}/jobs/applications${params}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  },

  /**
   * Get match explanation
   */
  getMatchExplanation: async (jobId) => {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/jobs/${jobId}/match-explanation`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  }
};

export default jobService;
