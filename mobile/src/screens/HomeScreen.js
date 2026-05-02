import React, { useEffect, useRef } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  Animated, StatusBar, Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Colors, Fonts, Spacing, Radius, Shadow, CategoryMeta } from '../constants/theme';
import CategoryCard from '../components/CategoryCard';

const QUICK_QUERIES = [
  { icon: '🌾', text: 'Kharif crop advice', query: 'What to grow in Kharif season?' },
  { icon: '🔴', text: 'Disease help',        query: 'My paddy leaves have brown spots' },
  { icon: '🧪', text: 'Fertilizer guide',   query: 'How much urea for sugarcane per acre?' },
  { icon: '💧', text: 'Irrigation tips',    query: 'How to install drip irrigation?' },
];

export default function HomeScreen({ navigation }) {
  const fadeAnim  = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim,  { toValue: 1, duration: 600, useNativeDriver: true }),
      Animated.spring(slideAnim, { toValue: 0, friction: 7, useNativeDriver: true }),
    ]).start();
  }, []);

  const goToChat = (query = '') => {
    navigation.navigate('Chat', { initialQuery: query });
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={Colors.background} />
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>

        {/* Header Gradient Banner */}
        <LinearGradient
          colors={['#1B5E20', '#0D3318', '#0D1B0F']}
          style={styles.hero}
        >
          <Animated.View style={{ opacity: fadeAnim, transform: [{ translateY: slideAnim }] }}>
            <Text style={styles.heroTagline}>🌱 Offline Agricultural Advisory</Text>
            <Text style={styles.heroTitle}>AgriVision</Text>
            <Text style={styles.heroSubtitle}>Mandya District Farming Intelligence</Text>
            <Text style={styles.heroDesc}>
              Complete crop advisory, disease diagnosis & government scheme info — works without internet.
            </Text>
            <TouchableOpacity style={styles.ctaButton} onPress={() => goToChat()} activeOpacity={0.85}>
              <Text style={styles.ctaText}>💬 Ask Your Farming Question</Text>
            </TouchableOpacity>
          </Animated.View>
        </LinearGradient>

        {/* Quick Action Row */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>⚡ Quick Help</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.quickRow}>
            {QUICK_QUERIES.map((q, i) => (
              <TouchableOpacity key={i} style={styles.quickCard} onPress={() => goToChat(q.query)} activeOpacity={0.8}>
                <Text style={styles.quickIcon}>{q.icon}</Text>
                <Text style={styles.quickText}>{q.text}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Browse Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>📂 Browse by Category</Text>
          <View style={styles.categoryGrid}>
            {Object.entries(CategoryMeta).map(([key, meta]) => (
              <CategoryCard
                key={key}
                emoji={meta.emoji}
                label={meta.label}
                color={meta.color}
                onPress={() => navigation.navigate('Browse', { category: key })}
              />
            ))}
          </View>
        </View>

        {/* Coverage Stats */}
        <View style={[styles.statsCard, Shadow.card]}>
          <Text style={styles.statsTitle}>📊 Knowledge Base</Text>
          <View style={styles.statsRow}>
            {[
              { num: '10+',  label: 'Crops' },
              { num: '50+',  label: 'Diseases' },
              { num: '6+',   label: 'Schemes' },
              { num: '100%', label: 'Offline' },
            ].map((s, i) => (
              <View key={i} style={styles.statItem}>
                <Text style={styles.statNum}>{s.num}</Text>
                <Text style={styles.statLabel}>{s.label}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Bottom nav links */}
        <View style={styles.navLinks}>
          <TouchableOpacity style={styles.navLink} onPress={() => navigation.navigate('Crops')}>
            <Text style={styles.navLinkText}>🌾 All Crops →</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navLink} onPress={() => navigation.navigate('Schemes')}>
            <Text style={styles.navLinkText}>🏛️ Govt Schemes →</Text>
          </TouchableOpacity>
        </View>

        <View style={{ height: 30 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container:  { flex: 1, backgroundColor: Colors.background },
  scroll:     { flexGrow: 1 },

  hero: {
    paddingTop: Platform.OS === 'ios' ? 60 : 50,
    paddingBottom: Spacing.xxxl,
    paddingHorizontal: Spacing.xl,
  },
  heroTagline:  { fontSize: Fonts.sizes.sm, color: Colors.primaryLight, letterSpacing: 1, marginBottom: 6 },
  heroTitle:    { fontSize: 38, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, lineHeight: 44 },
  heroSubtitle: { fontSize: Fonts.sizes.md, color: Colors.textSecondary, marginTop: 4 },
  heroDesc:     { fontSize: Fonts.sizes.sm, color: Colors.textMuted, marginTop: Spacing.sm, lineHeight: 20 },
  ctaButton:    {
    marginTop: Spacing.xl,
    backgroundColor: Colors.primary,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.xl,
    borderRadius: Radius.full,
    alignSelf: 'flex-start',
  },
  ctaText: { fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.bold, color: Colors.textDark },

  section:      { paddingHorizontal: Spacing.lg, marginTop: Spacing.xl },
  sectionTitle: { fontSize: Fonts.sizes.lg, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, marginBottom: Spacing.md },

  quickRow:  { flexDirection: 'row' },
  quickCard: {
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderRadius: Radius.lg,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.lg,
    marginRight: Spacing.sm,
    alignItems: 'center',
    minWidth: 110,
  },
  quickIcon: { fontSize: 28, marginBottom: 4 },
  quickText: { fontSize: Fonts.sizes.xs, color: Colors.textSecondary, textAlign: 'center' },

  categoryGrid: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -Spacing.xs },

  statsCard:  {
    backgroundColor: Colors.surface,
    margin: Spacing.lg,
    borderRadius: Radius.lg,
    padding: Spacing.lg,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
  },
  statsTitle: { fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, marginBottom: Spacing.md },
  statsRow:   { flexDirection: 'row', justifyContent: 'space-around' },
  statItem:   { alignItems: 'center' },
  statNum:    { fontSize: Fonts.sizes.xl, fontWeight: Fonts.weights.bold, color: Colors.primary },
  statLabel:  { fontSize: Fonts.sizes.xs, color: Colors.textMuted, marginTop: 2 },

  navLinks:   { flexDirection: 'row', justifyContent: 'space-around', marginTop: Spacing.md },
  navLink:    { padding: Spacing.md },
  navLinkText:{ fontSize: Fonts.sizes.md, color: Colors.primary, fontWeight: Fonts.weights.medium },
});
