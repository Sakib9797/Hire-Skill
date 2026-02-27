import api from './api';

const salaryService = {
  // Predict salary
  predictSalary: async (payload) => {
    const response = await api.post('/salary/predict', payload);
    return response.data;
  },

  // Get all available roles
  getRoles: async () => {
    const response = await api.get('/salary/roles');
    return response.data;
  },

  // Get skills list
  getSkills: async () => {
    const response = await api.get('/salary/skills');
    return response.data;
  },

  // Generate interview prep questions
  generateInterviewQuestions: async (payload) => {
    const response = await api.post('/documents/interview-prep', payload);
    return response.data;
  },

  // Get career path graph
  getCareerPathGraph: async (fromRole = '', toRole = '') => {
    const params = new URLSearchParams();
    if (fromRole) params.append('from', fromRole);
    if (toRole)   params.append('to', toRole);
    const response = await api.get(`/career/path-graph?${params.toString()}`);
    return response.data;
  },
};

export default salaryService;
