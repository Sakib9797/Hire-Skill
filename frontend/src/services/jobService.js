import api from './api';

const jobService = {
  /**
   * Initialize job database
   */
  initializeJobs: async () => {
    const response = await api.post('/jobs/initialize', {});
    return response.data;
  },

  /**
   * Get matched jobs for user
   */
  getMatchedJobs: async (filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.role) params.append('role', filters.role);
    if (filters.location) params.append('location', filters.location);
    if (filters.experience_level) params.append('experience_level', filters.experience_level);
    if (filters.work_type) params.append('work_type', filters.work_type);
    if (filters.job_type) params.append('job_type', filters.job_type);
    if (filters.limit) params.append('limit', filters.limit);
    
    const response = await api.get(`/jobs/match?${params.toString()}`);
    return response.data;
  },

  /**
   * Search jobs (live from APIs)
   */
  searchJobs: async (query, filters = {}, limit = 50, offset = 0) => {
    const params = new URLSearchParams();

    if (query)                        params.append('q', query);
    if (filters.location)             params.append('location', filters.location);
    if (filters.experience_level)     params.append('experience_level', filters.experience_level);
    if (filters.work_type)            params.append('work_type', filters.work_type);
    if (filters.job_type)             params.append('job_type', filters.job_type);
    if (filters.source)               params.append('source', filters.source);
    if (filters.min_salary)           params.append('min_salary', filters.min_salary);
    params.append('limit', limit);
    params.append('offset', offset);

    const response = await api.get(`/jobs/search?${params.toString()}`);
    return response.data;
  },

  /**
   * Get specific job
   */
  getJob: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  /**
   * Save a live-scraped job (upserts job to DB then creates saved record)
   */
  saveExternalJob: async (jobData) => {
    const response = await api.post('/jobs/save-external', jobData);
    return response.data;
  },

  /**
   * Save DB job for later
   */
  saveJob: async (jobId) => {
    const response = await api.post(`/jobs/${jobId}/save`, {});
    return response.data;
  },

  /**
   * Apply to job
   */
  applyToJob: async (jobId, data = {}) => {
    const response = await api.post(`/jobs/${jobId}/apply`, data);
    return response.data;
  },

  /**
   * Get user applications
   */
  getUserApplications: async (status = null) => {
    const params = status ? `?status=${status}` : '';
    const response = await api.get(`/jobs/applications${params}`);
    return response.data;
  },

  /**
   * Get match explanation
   */
  getMatchExplanation: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}/match-explanation`);
    return response.data;
  }
};

export default jobService;
