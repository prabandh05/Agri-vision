import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors, Fonts, Spacing, Radius } from '../constants/theme';

const SUGGESTIONS = [
  'My paddy leaves have brown spots',
  'What to grow in Kharif season?',
  'How much urea for sugarcane?',
  'How to make jeevamrutha?',
  'PM-KISAN scheme benefits',
  'Red palm weevil in coconut',
  'Drip irrigation subsidy',
  'Best ragi varieties Mandya',
  'Sugarcane red rot disease',
  'Paddy blast treatment',
  'Crop insurance PMFBY',
  'Organic seed treatment',
];

/**
 * SuggestionChips — horizontal scrolling chips for quick query selection.
 */
export default function SuggestionChips({ onPress, label = '💡 Quick questions:' }) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {SUGGESTIONS.map((suggestion, index) => (
          <TouchableOpacity
            key={index}
            style={styles.chip}
            onPress={() => onPress(suggestion)}
            activeOpacity={0.7}
          >
            <Text style={styles.chipText}>{suggestion}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: Spacing.sm,
    borderTopWidth: 1,
    borderTopColor: Colors.surfaceBorder,
    backgroundColor: Colors.background,
  },
  label: {
    fontSize: Fonts.sizes.xs,
    color: Colors.textMuted,
    marginLeft: Spacing.lg,
    marginBottom: Spacing.xs,
  },
  scrollContent: {
    paddingHorizontal: Spacing.lg,
    gap: Spacing.sm,
    flexDirection: 'row',
  },
  chip: {
    backgroundColor: Colors.surfaceHigh,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderRadius: Radius.full,
    paddingVertical: 6,
    paddingHorizontal: Spacing.md,
  },
  chipText: {
    fontSize: Fonts.sizes.xs,
    color: Colors.textSecondary,
    fontWeight: Fonts.weights.medium,
  },
});
