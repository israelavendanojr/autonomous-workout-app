// app/(tabs)/home.tsx
import React from 'react';
import { View, Text, TouchableOpacity, Alert } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

const HomeScreen: React.FC = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', onPress: logout, style: 'destructive' },
    ]);
  };

  return (
    <View className="flex-1 bg-gray-50">
      <View className="flex-1 justify-center px-8">
        <View className="bg-white rounded-xl p-8 shadow-lg">
          <Text className="text-3xl font-bold text-center mb-8 text-gray-800">
            Welcome!
          </Text>

          <View className="mb-6">
            <Text className="text-lg text-gray-700 mb-2">
              <Text className="font-semibold">Name:</Text> {user?.first_name} {user?.last_name}
            </Text>
            <Text className="text-lg text-gray-700 mb-2">
              <Text className="font-semibold">Username:</Text> {user?.username}
            </Text>
            <Text className="text-lg text-gray-700 mb-2">
              <Text className="font-semibold">Email:</Text> {user?.email}
            </Text>
          </View>

          <TouchableOpacity
            className="bg-red-600 rounded-lg py-4"
            onPress={handleLogout}
          >
            <Text className="text-white text-center font-semibold text-lg">
              Logout
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

export default HomeScreen;
