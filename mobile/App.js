/**
 * AgriVision — Root App with Bottom Tab + Stack Navigation
 * Offline-first agricultural advisory for Mandya district farmers.
 */
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Text, View, Platform } from 'react-native';

import HomeScreen    from './src/screens/HomeScreen';
import ChatScreen    from './src/screens/ChatScreen';
import BrowseScreen  from './src/screens/BrowseScreen';
import CropsScreen   from './src/screens/CropsScreen';
import SchemesScreen from './src/screens/SchemesScreen';
import { Colors, Fonts } from './src/constants/theme';

const Tab   = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

// ─── Tab Icon Component ───────────────────────────────────────────────────────
function TabIcon({ emoji, label, focused }) {
  return (
    <View style={{ alignItems: 'center', paddingTop: 4 }}>
      <Text style={{ fontSize: 20, opacity: focused ? 1 : 0.55 }}>{emoji}</Text>
      <Text style={{
        fontSize: 10,
        fontWeight: focused ? '700' : '400',
        color: focused ? Colors.tabActive : Colors.tabInactive,
        marginTop: 2,
      }}>{label}</Text>
    </View>
  );
}

// ─── Main Tab Navigator ───────────────────────────────────────────────────────
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerStyle:          { backgroundColor: Colors.surface },
        headerTintColor:      Colors.textPrimary,
        headerTitleStyle:     { fontWeight: '700', fontSize: Fonts.sizes.lg },
        headerShadowVisible:  false,
        tabBarStyle: {
          backgroundColor:     Colors.tabBackground,
          borderTopColor:      Colors.surfaceBorder,
          borderTopWidth:      1,
          height:              Platform.OS === 'ios' ? 82 : 62,
          paddingBottom:       Platform.OS === 'ios' ? 22 : 6,
          paddingTop:          4,
        },
        tabBarShowLabel: false,
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: '🌱 AgriVision',
          tabBarIcon: ({ focused }) => <TabIcon emoji="🏠" label="Home" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Chat"
        component={ChatScreen}
        options={{
          title: '💬 Ask Advisor',
          tabBarIcon: ({ focused }) => <TabIcon emoji="💬" label="Ask" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Browse"
        component={BrowseScreen}
        options={{
          title: '📂 Browse Topics',
          tabBarIcon: ({ focused }) => <TabIcon emoji="📂" label="Browse" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Crops"
        component={CropsScreen}
        options={{
          title: '🌾 Crops',
          tabBarIcon: ({ focused }) => <TabIcon emoji="🌾" label="Crops" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="Schemes"
        component={SchemesScreen}
        options={{
          title: '🏛️ Schemes',
          tabBarIcon: ({ focused }) => <TabIcon emoji="🏛️" label="Schemes" focused={focused} />,
        }}
      />
    </Tab.Navigator>
  );
}

// ─── Root App ─────────────────────────────────────────────────────────────────
export default function App() {
  return (
    <NavigationContainer
      theme={{
        dark: true,
        colors: {
          primary:    Colors.primary,
          background: Colors.background,
          card:       Colors.surface,
          text:       Colors.textPrimary,
          border:     Colors.surfaceBorder,
          notification: Colors.primary,
        },
        fonts: {
          regular: { fontFamily: 'System', fontWeight: '400' },
          medium:  { fontFamily: 'System', fontWeight: '500' },
          bold:    { fontFamily: 'System', fontWeight: '700' },
          heavy:   { fontFamily: 'System', fontWeight: '900' },
        },
      }}
    >
      <StatusBar style="light" backgroundColor={Colors.background} />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="MainTabs" component={MainTabs} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
