// app/(auth)/login.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { router } from 'expo-router';
import { useAuth } from '../../src/context/AuthContext';

const LoginScreen: React.FC = () => {
  const { login } = useAuth();

  const [form, setForm] = useState({
    email: '',
    password: '',
  });

  const handleChange = (key: keyof typeof form, value: string) => {
    setForm({ ...form, [key]: value });
  };

  const handleLogin = async () => {
    try {
      await login(form);
      router.replace('/home');
    } catch (error: any) {
      Alert.alert('Login Failed', error.message || 'Something went wrong.');
    }
  };

  return (
    <View className="flex-1 justify-center px-8 bg-gray-50">
      <View className="bg-white rounded-xl p-8 shadow-md">
        <Text className="text-3xl font-bold text-center mb-8 text-gray-800">
          Login
        </Text>

        <TextInput
          className="border border-gray-300 rounded-lg px-4 py-3 mb-4"
          placeholder="Email"
          keyboardType="email-address"
          autoCapitalize="none"
          value={form.email}
          onChangeText={(text) => handleChange('email', text)}
        />

        <TextInput
          className="border border-gray-300 rounded-lg px-4 py-3 mb-6"
          placeholder="Password"
          secureTextEntry
          autoCapitalize="none"
          value={form.password}
          onChangeText={(text) => handleChange('password', text)}
        />

        <TouchableOpacity
          className="bg-blue-600 rounded-lg py-4 mb-4"
          onPress={handleLogin}
        >
          <Text className="text-white text-center font-semibold text-lg">
            Sign In
          </Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push('/register')}>
          <Text className="text-center text-gray-600">
            Don't have an account?{' '}
            <Text className="text-blue-600 font-semibold">Register</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default LoginScreen;
