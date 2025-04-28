const config = {
  development: {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  },
  production: {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.bookmark.ai',
  },
  test: {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  },
};

const env = import.meta.env.MODE || 'development';
export const apiBaseUrl = config[env].apiBaseUrl;

export default config[env]; 