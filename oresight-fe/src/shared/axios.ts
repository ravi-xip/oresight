// This file provides a version of the axios library that automatically injects our CSRF token into requests
import originalAxios from 'axios';

// Logic to inject CSRF token into requests.
const getCsrfToken = (): string | null => {
  const tokenElement = document.querySelector('[name="csrf-token"]');
  return tokenElement ? tokenElement.getAttribute('content') : null;
};

// Create a version of axios that automatically injects our CSRF token into requests.
export const axiosSimple = originalAxios.create({
    headers: {
        'X-CSRF-Token': getCsrfToken() || 'no-csrf-token',
    },
});
