import React from 'react';
import { TouchableOpacity, View, Text, StyleSheet } from 'react-native';
import { Colors, Fonts, Spacing, Radius, Shadow } from '../constants/theme';

/**
 * CategoryCard — tappable card for browsing categories on HomeScreen / BrowseScreen.
 */
export default function CategoryCard({ emoji, label, color, description, onPress }) {
  return (
    <TouchableOpacity style={[styles.card, Shadow.card]} onPress={onPress} activeOpacity={0.75}>
      <View style={[styles.iconBadge, { backgroundColor: color + '22', borderColor: color + '55' }]}>
        <Text style={styles.emoji}>{emoji}</Text>
      </View>
      <Text style={styles.label}>{label}</Text>
      {description ? <Text style={styles.description}>{description}</Text> : null}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderRadius: Radius.lg,
    padding: Spacing.lg,
    alignItems: 'center',
    minWidth: 110,
    margin: Spacing.xs,
  },
  iconBadge: {
    width: 52, height: 52,
    borderRadius: 26,
    borderWidth: 1,
    alignItems: 'center', justifyContent: 'center',
    marginBottom: Spacing.sm,
  },
  emoji: { fontSize: 24 },
  label: {
    fontSize: Fonts.sizes.sm,
    fontWeight: Fonts.weights.semibold,
    color: Colors.textPrimary,
    textAlign: 'center',
  },
  description: {
    fontSize: Fonts.sizes.xs,
    color: Colors.textMuted,
    textAlign: 'center',
    marginTop: 2,
  },
});
