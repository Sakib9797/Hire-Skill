import api from './api';

const careerService = {
  // Get personalized career recommendations
  getRecommendations: async (topN = 5) => {
    try {
      const response = await api.get(`/career/recommend?top_n=${topN}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get recommendations' };
    }
  },

  // Get all available careers
  getAllCareers: async () => {
    try {
      const response = await api.get('/career/careers');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get careers' };
    }
  },

  // Get specific career details
  getCareerDetails: async (roleName) => {
    try {
      const response = await api.get(`/career/careers/${encodeURIComponent(roleName)}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get career details' };
    }
  },

  // Get skill gap analysis for a specific career
  getSkillGap: async (careerRole) => {
    try {
      const response = await api.get(`/career/skill-gap/${encodeURIComponent(careerRole)}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get skill gap analysis' };
    }
  },

  // Get all available skills (for autocomplete)
  getAllSkills: async () => {
    try {
      const response = await api.get('/career/skills');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get skills' };
    }
  },
};

export default careerService;
