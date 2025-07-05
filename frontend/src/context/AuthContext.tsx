// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

type AuthContextType = {
  user: any;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: async () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (email: string, password: string) => {
    const res = await axios.post('http://localhost:8000/api/auth/login/', { email, password });
    await AsyncStorage.setItem('token', res.data.access);
    setUser(res.data.user); // if your backend returns user
  };

  const register = async (email: string, password: string) => {
    await axios.post('http://localhost:8000/api/auth/register/', { email, password });
    await login(email, password);
  };

  const logout = async () => {
    await AsyncStorage.removeItem('token');
    setUser(null);
  };

  useEffect(() => {
    const bootstrap = async () => {
      const token = await AsyncStorage.getItem('token');
      if (token) {
        try {
          const res = await axios.get('http://localhost:8000/api/auth/user/', {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUser(res.data);
        } catch {
          await AsyncStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    bootstrap();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
