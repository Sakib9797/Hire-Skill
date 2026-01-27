import api from './api';

const userService = {
  // Get user profile
  getProfile: async () => {
    try {
      const response = await api.get('/users/profile');
      return response.data.data.user;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get profile' };
    }
  },

  // Update user profile
  updateProfile: async (profileData) => {
    try {
      const response = await api.put('/users/profile', profileData);
      const user = response.data.data.user;
      localStorage.setItem('user', JSON.stringify(user));
      return user;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update profile' };
    }
  },

  // Update theme preference
  updateTheme: async (theme) => {
    try {
      const response = await api.put('/users/profile/theme', { theme });
      return response.data.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update theme' };
    }
  },

  // Get all users (admin only)
  getAllUsers: async (page = 1, perPage = 10, role = null) => {
    try {
      const params = { page, per_page: perPage };
      if (role) params.role = role;
      
      const response = await api.get('/users/', { params });
      return response.data.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get users' };
    }
  },
};

export default userService;
