import { Tabs } from 'expo-router';
import React from 'react';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
  screenOptions={{
    headerShown: false,
  }}
>
  <Tabs.Screen
    name="home"
    options={{
      title: 'Home',
      tabBarIcon: ({ color }) => (
        <Ionicons name="home-outline" size={24} color={color} />
      ),
    }}
  />
</Tabs>

  );
}
