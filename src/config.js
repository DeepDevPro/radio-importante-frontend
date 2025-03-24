const isDevelopment = process.env.NODE_ENV === 'development';
const API_URL = isDevelopment ? "http://localhost:8000" : "https://api.importantestudio.com";

export { API_URL };