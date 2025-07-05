import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

export default function RegisterScreen() {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      await register(email, password);
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <View className="flex-1 justify-center items-center bg-white px-4">
      <Text className="text-2xl font-bold mb-6">Register</Text>
      <TextInput
        className="border w-full px-4 py-2 mb-4 rounded"
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        className="border w-full px-4 py-2 mb-4 rounded"
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <TouchableOpacity
        className="bg-blue-500 px-4 py-2 rounded w-full"
        onPress={handleRegister}
      >
        <Text className="text-white text-center">Register</Text>
      </TouchableOpacity>
    </View>
  );
}
