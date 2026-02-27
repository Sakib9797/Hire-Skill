import api from './api';

const documentService = {
  // =============== RESUME SERVICES ===============

  // Get all resumes
  getResumes: async (currentOnly = false) => {
    try {
      const response = await api.get(`/documents/resume?current_only=${currentOnly}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get resumes' };
    }
  },

  // Get specific resume
  getResume: async (resumeId) => {
    try {
      const response = await api.get(`/documents/resume/${resumeId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get resume' };
    }
  },

  // Update resume (creates new version)
  updateResume: async (resumeId, updates) => {
    try {
      const response = await api.put(`/documents/resume/${resumeId}`, updates);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update resume' };
    }
  },

  // Delete resume
  deleteResume: async (resumeId) => {
    try {
      const response = await api.delete(`/documents/resume/${resumeId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to delete resume' };
    }
  },

  // =============== COVER LETTER SERVICES ===============
  
  // Generate cover letter
  generateCoverLetter: async (data) => {
    try {
      const response = await api.post('/documents/cover-letter/generate', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to generate cover letter' };
    }
  },

  // Generate custom cover letter
  generateCustomCoverLetter: async (data) => {
    try {
      const response = await api.post('/documents/cover-letter/generate-custom', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to generate custom cover letter' };
    }
  },

  // Get all cover letters
  getCoverLetters: async (currentOnly = false) => {
    try {
      const response = await api.get(`/documents/cover-letter?current_only=${currentOnly}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get cover letters' };
    }
  },

  // Get specific cover letter
  getCoverLetter: async (coverLetterId) => {
    try {
      const response = await api.get(`/documents/cover-letter/${coverLetterId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get cover letter' };
    }
  },

  // Delete cover letter
  deleteCoverLetter: async (coverLetterId) => {
    try {
      const response = await api.delete(`/documents/cover-letter/${coverLetterId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to delete cover letter' };
    }
  },

  // =============== ATS & CV SERVICES ===============

  // Check ATS compatibility of an uploaded resume
  checkATSResume: async (resumeFile, targetRole = '') => {
    try {
      const formData = new FormData();
      formData.append('resume_file', resumeFile);
      if (targetRole) formData.append('target_role', targetRole);
      const response = await api.post('/documents/resume/check-ats', formData, {
        headers: { 'Content-Type': undefined },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to check resume' };
    }
  },

  // =============== UTILITY SERVICES ===============

  // Get cover letter tones
  getTones: async () => {
    try {
      const response = await api.get('/documents/tones');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get tones' };
    }
  },
};

export default documentService;
