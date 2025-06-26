// app/(auth)/protected.tsx
import { useEffect, useState } from "react";
import { Redirect, Stack } from "expo-router";
import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";
import api from "@/lib/api"; // or wherever you placed it
import { ACCESS_TOKEN, REFRESH_TOKEN } from "@/lib/constants";
import { View, Text, ActivityIndicator } from "react-native";

export default function ProtectedScreen() {
  const [authorized, setAuthorized] = useState<null | boolean>(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = await SecureStore.getItemAsync(ACCESS_TOKEN);
    if (!token) return setAuthorized(false);

    try {
      const decoded: any = jwtDecode(token);
      const now = Date.now() / 1000;

      if (decoded.exp < now) {
        await refreshToken();
      } else {
        setAuthorized(true);
      }
    } catch (err) {
      console.log("Decode failed", err);
      setAuthorized(false);
    }
  };

  const refreshToken = async () => {
    const refresh = await SecureStore.getItemAsync(REFRESH_TOKEN);
    if (!refresh) return setAuthorized(false);

    try {
      const res = await api.post("/api/token/refresh/", {
        refresh,
      });

      if (res.status === 200) {
        await SecureStore.setItemAsync(ACCESS_TOKEN, res.data.access);
        setAuthorized(true);
      } else {
        setAuthorized(false);
      }
    } catch (err) {
      console.log("Refresh failed", err);
      setAuthorized(false);
    }
  };

  if (authorized === null) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" />
        <Text>Checking authorization...</Text>
      </View>
    );
  }

  if (!authorized) {
    return <Redirect href="/login" />;
  }

  return (
    <>
      <Stack.Screen options={{ title: "Protected" }} />
      <View className="flex-1 items-center justify-center bg-white">
        <Text className="text-2xl font-bold text-black">You are logged in!</Text>
      </View>
    </>
  );
}
