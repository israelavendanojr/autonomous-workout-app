// app/(auth)/register.tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '../../src/context/AuthContext';

const RegisterScreen: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleRegister = async () => {
    const { username, email, first_name, last_name, password, password_confirm } = formData;

    if (!username || !email || !first_name || !last_name || !password || !password_confirm) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    if (password !== password_confirm) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }

    if (password.length < 6) {
      Alert.alert('Error', 'Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    const result = await register(formData);
    setLoading(false);

    if (!result.success) {
      const errorMessage = typeof result.error === 'object'
        ? Object.values(result.error).flat().join('\n')
        : result.error;
      Alert.alert('Registration Failed', errorMessage);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-gray-50"
    >
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <View className="flex-1 justify-center px-8 py-8">
          <View className="bg-white rounded-xl p-8 shadow-lg">
            <Text className="text-3xl font-bold text-center mb-8 text-gray-800">
              Create Account
            </Text>

            {[{ label: 'Username', key: 'username' },
              { label: 'Email', key: 'email', keyboardType: 'email-address' },
              { label: 'First Name', key: 'first_name' },
              { label: 'Last Name', key: 'last_name' },
              { label: 'Password', key: 'password', secure: true },
              { label: 'Confirm Password', key: 'password_confirm', secure: true }
            ].map(({ label, key, keyboardType, secure }) => (
              <View className="mb-4" key={key}>
                <Text className="text-gray-700 mb-2 font-medium">{label}</Text>
                <TextInput
                  className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
                  placeholder={`Enter your ${label.toLowerCase()}`}
                  value={formData[key as keyof typeof formData]}
                  onChangeText={(value) => handleInputChange(key, value)}
                  autoCapitalize={secure ? 'none' : 'words'}
                  autoCorrect={false}
                  keyboardType={keyboardType as any}
                  secureTextEntry={!!secure}
                />
              </View>
            ))}

            <TouchableOpacity
              className={`bg-blue-600 rounded-lg py-4 mb-4 ${loading ? 'opacity-50' : ''}`}
              onPress={handleRegister}
              disabled={loading}
            >
              <Text className="text-white text-center font-semibold text-lg">
                {loading ? 'Creating Account...' : 'Create Account'}
              </Text>
            </TouchableOpacity>

            <View className="flex-row justify-center mt-4">
              <Text className="text-gray-600">Already have an account? </Text>
              <TouchableOpacity onPress={() => router.push('/login')}>
                <Text className="text-blue-600 font-semibold">Sign In</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

export default RegisterScreen;
