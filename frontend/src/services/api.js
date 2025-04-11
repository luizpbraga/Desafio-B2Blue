import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_DOCKERIZED === 'true' ? 'http://backend:8000/api' : 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const endpoints = {
  stations: '/stations/',
  history: '/history/',
};
