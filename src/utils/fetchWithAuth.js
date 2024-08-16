// src/utils/fetchWithAuth.js

export const fetchWithAuth = async (url, options = {}) => {
    const token = localStorage.getItem('token'); // Assuming the token is stored in localStorage
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
  
    if (!response.ok) {
      if (response.status === 401) {
        // Handle unauthorized access, e.g., redirect to login
        // You can also log out the user or refresh the token here
      }
      throw new Error('Request failed');
    }
  
    return response;
  };
  