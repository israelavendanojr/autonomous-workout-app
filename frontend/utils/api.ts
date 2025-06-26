import axios from "axios";
import Constants from "expo-constants";
import * as SecureStore from "expo-secure-store";
import { ACCESS_TOKEN } from "./constants"; // adjust import path as needed

const apiUrl = Constants.expoConfig?.extra?.API_URL;

const api = axios.create({
  baseURL: apiUrl,
});

// Add Authorization header to each request
api.interceptors.request.use(
  async (config) => {
    const token = await SecureStore.getItemAsync(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
