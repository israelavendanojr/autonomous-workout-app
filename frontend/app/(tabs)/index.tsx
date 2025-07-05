import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

export default function HomeScreen() {
  const { user, logout } = useAuth();

  return (
    <View className="flex-1 justify-center items-center bg-white px-4">
      <Text className="text-2xl font-bold mb-4">Welcome, {user?.email}!</Text>
      <TouchableOpacity
        className="bg-red-500 px-4 py-2 rounded"
        onPress={logout}
      >
        <Text className="text-white">Logout</Text>
      </TouchableOpacity>
    </View>
  );
}
