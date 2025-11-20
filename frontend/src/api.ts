const API_BASE_URL = 'http://localhost:4243';

/**
 * Lightweight wrapper around fetch that prefixes the backend base URL.
 * `path` should always start with a leading `/`, e.g. `/maps` or `/auth/login`.
 */
export const apiFetch = (path: string, options?: RequestInit) => {
    return fetch(`${API_BASE_URL}${path}`, options);
};
