import React, { useState, useEffect } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet,
  ActivityIndicator, ScrollView,
} from 'react-native';
import { Colors, Fonts, Spacing, Radius, Shadow, CategoryMeta } from '../constants/theme';
import { searchByCategory } from '../database/DatabaseService';

const CATEGORIES = Object.entries(CategoryMeta).map(([key, meta]) => ({ key, ...meta }));

export default function BrowseScreen({ navigation, route }) {
  const [selectedCat, setSelectedCat] = useState(route?.params?.category || 'disease');
  const [entries, setEntries]         = useState([]);
  const [loading, setLoading]         = useState(false);

  useEffect(() => {
    loadCategory(selectedCat);
  }, [selectedCat]);

  const loadCategory = async (cat) => {
    setLoading(true);
    try {
      const rows = await searchByCategory(cat, 50);
      setEntries(rows);
    } catch (e) {
      setEntries([]);
    } finally {
      setLoading(false);
    }
  };

  const meta = CategoryMeta[selectedCat] || CategoryMeta.disease;

  const renderEntry = ({ item }) => {
    let subtitle = '';
    try {
      const parsed = JSON.parse(item.metadata || '{}');
      if (item.category === 'crop')       subtitle = parsed.local_name || '';
      if (item.category === 'disease')    subtitle = `Crop: ${item.crop || '—'} | ${parsed.type || ''}`;
      if (item.category === 'scheme')     subtitle = parsed.benefit?.slice(0, 60) || '';
      if (item.category === 'fertilizer') subtitle = parsed.content || '';
      if (item.category === 'organic')    subtitle = parsed.type || '';
      if (item.category === 'irrigation') subtitle = parsed.type || '';
    } catch {}

    return (
      <TouchableOpacity
        style={[styles.entryCard, Shadow.card]}
        activeOpacity={0.8}
        onPress={() => navigation.navigate('Chat', { initialQuery: item.title })}
      >
        <View style={styles.entryLeft}>
          <Text style={[styles.entryEmoji]}>{meta.emoji}</Text>
        </View>
        <View style={styles.entryRight}>
          <Text style={styles.entryTitle} numberOfLines={2}>{item.title}</Text>
          {subtitle ? <Text style={styles.entrySubtitle} numberOfLines={1}>{subtitle}</Text> : null}
          <Text style={styles.entryAsk}>Tap to ask →</Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {/* Category Tab Strip */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.tabStrip}
        contentContainerStyle={styles.tabContent}
      >
        {CATEGORIES.map(cat => (
          <TouchableOpacity
            key={cat.key}
            style={[styles.tab, selectedCat === cat.key && { backgroundColor: cat.color + '33', borderColor: cat.color }]}
            onPress={() => setSelectedCat(cat.key)}
            activeOpacity={0.7}
          >
            <Text style={styles.tabEmoji}>{cat.emoji}</Text>
            <Text style={[styles.tabLabel, selectedCat === cat.key && { color: cat.color }]}>
              {cat.label.split(' ')[0]}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Entries List */}
      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator color={Colors.primary} size="large" />
          <Text style={styles.loadingText}>Loading {meta.label}...</Text>
        </View>
      ) : (
        <FlatList
          data={entries}
          keyExtractor={item => item.doc_id}
          renderItem={renderEntry}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.centered}>
              <Text style={styles.emptyText}>No entries found in this category.</Text>
            </View>
          }
          ListHeaderComponent={
            <View style={styles.listHeader}>
              <Text style={styles.listHeaderText}>{meta.emoji} {meta.label}</Text>
              <Text style={styles.listCount}>{entries.length} entries</Text>
            </View>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container:   { flex: 1, backgroundColor: Colors.background },

  tabStrip:    { flexGrow: 0, borderBottomWidth: 1, borderBottomColor: Colors.surfaceBorder },
  tabContent:  { paddingHorizontal: Spacing.sm, paddingVertical: Spacing.sm, gap: Spacing.sm },
  tab: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    paddingVertical: 6, paddingHorizontal: Spacing.sm,
    borderRadius: Radius.full,
    borderWidth: 1, borderColor: Colors.surfaceBorder,
    backgroundColor: Colors.surface,
  },
  tabEmoji:    { fontSize: 14 },
  tabLabel:    { fontSize: Fonts.sizes.xs, color: Colors.textMuted, fontWeight: Fonts.weights.medium },

  listContent: { padding: Spacing.md },
  listHeader:  { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: Spacing.md },
  listHeaderText: { fontSize: Fonts.sizes.lg, fontWeight: Fonts.weights.bold, color: Colors.textPrimary },
  listCount:   { fontSize: Fonts.sizes.sm, color: Colors.textMuted },

  entryCard: {
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderRadius: Radius.md,
    flexDirection: 'row',
    marginBottom: Spacing.sm,
    overflow: 'hidden',
  },
  entryLeft: {
    width: 52,
    alignItems: 'center', justifyContent: 'center',
    backgroundColor: Colors.surfaceHigh,
  },
  entryEmoji: { fontSize: 22 },
  entryRight: { flex: 1, padding: Spacing.md },
  entryTitle: { fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.semibold, color: Colors.textPrimary },
  entrySubtitle: { fontSize: Fonts.sizes.xs, color: Colors.textMuted, marginTop: 2 },
  entryAsk:   { fontSize: Fonts.sizes.xs, color: Colors.primary, marginTop: 4, fontWeight: Fonts.weights.medium },

  centered:    { flex: 1, alignItems: 'center', justifyContent: 'center', padding: Spacing.xxxl },
  loadingText: { color: Colors.textMuted, marginTop: Spacing.md, fontSize: Fonts.sizes.sm },
  emptyText:   { color: Colors.textMuted, fontSize: Fonts.sizes.md, textAlign: 'center' },
});
