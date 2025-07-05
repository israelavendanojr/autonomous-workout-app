// app/index.tsx
import { Redirect } from 'expo-router';

export default function Index() {
  return <Redirect href="/login" />; // Or "/(auth)/login" if using segmented routing
}
