import axios from 'axios';

/**
 * Base API URL configuration.
 * Determines the appropriate backend URL based on the environment:
 * - When running in Docker (REACT_APP_DOCKERIZED=true): Uses 'backend' service name
 * - For local development: Uses localhost
 * @constant {string}
 */
const API_BASE_URL = process.env.REACT_APP_DOCKERIZED === 'true' 
  ? 'http://backend:8000/api' 
  : 'http://localhost:8000/api';

/**
 * Axios instance configured with the base API URL.
 * This instance will be used for all API requests.
 * @type {axios.AxiosInstance}
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * API endpoints configuration object.
 * Contains all available endpoints for the application.
 * @constant {object}
 * @property {string} stations - Endpoint for station operations
 * @property {string} history - Endpoint for history records
 */
export const endpoints = {
  stations: '/stations/',
  history: '/history/',
};
