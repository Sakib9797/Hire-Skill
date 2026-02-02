import api from './api';

const documentService = {
  // =============== RESUME SERVICES ===============
  
  // Generate new resume
  generateResume: async (data) => {
    try {
      const response = await api.post('/documents/resume/generate', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to generate resume' };
    }
  },

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
  
  // Parse CV file
  parseCVFile: async (file) => {
    try {
      const formData = new FormData();
      formData.append('cv_file', file);
      
      const response = await api.post('/documents/parse-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to parse CV file' };
    }
  },

  // Generate ATS-optimized resume
  generateATSResume: async (data, cvFile = null) => {
    try {
      if (cvFile) {
        // Upload with file
        const formData = new FormData();
        formData.append('cv_file', cvFile);
        if (data.target_role) {
          formData.append('target_role', data.target_role);
        }
        
        const response = await api.post('/documents/resume/generate-ats', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        return response.data;
      } else {
        // JSON request without file
        const response = await api.post('/documents/resume/generate-ats', data);
        return response.data;
      }
    } catch (error) {
      throw error.response?.data || { message: 'Failed to generate ATS resume' };
    }
  },

  // Get role-based template recommendations
  getRoleRecommendations: async (role) => {
    try {
      const response = await api.get(`/documents/role-recommendations?role=${encodeURIComponent(role)}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get role recommendations' };
    }
  },

  // =============== UTILITY SERVICES ===============
  
  // Get resume templates
  getTemplates: async () => {
    try {
      const response = await api.get('/documents/templates');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get templates' };
    }
  },

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
