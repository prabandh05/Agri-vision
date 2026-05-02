import React, { useEffect, useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet,
  ActivityIndicator, Modal, ScrollView, Linking,
} from 'react-native';
import { Colors, Fonts, Spacing, Radius, Shadow } from '../constants/theme';
import { getAllSchemes } from '../database/DatabaseService';

const SCHEME_COLORS = {
  central: Colors.info,
  state:   Colors.organic,
  default: Colors.accent,
};

export default function SchemesScreen({ navigation }) {
  const [schemes, setSchemes]   = useState([]);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    getAllSchemes().then(data => {
      setSchemes(data);
      setLoading(false);
    });
  }, []);

  const parseMeta = (row) => {
    try { return JSON.parse(row.metadata || '{}'); }
    catch { return {}; }
  };

  const renderScheme = ({ item }) => {
    const meta  = parseMeta(item);
    const color = SCHEME_COLORS[meta.type] || SCHEME_COLORS.default;

    return (
      <TouchableOpacity style={[styles.schemeCard, Shadow.card, { borderLeftColor: color }]} onPress={() => setSelected(item)} activeOpacity={0.8}>
        <View style={styles.schemeTop}>
          <View style={[styles.typeBadge, { backgroundColor: color + '22' }]}>
            <Text style={[styles.typeText, { color }]}>{meta.type?.toUpperCase() || 'SCHEME'}</Text>
          </View>
          <Text style={styles.schemeName}>{item.title}</Text>
        </View>
        {meta.full_name && <Text style={styles.schemeFullName}>{meta.full_name}</Text>}
        {meta.benefit && (
          <View style={styles.benefitRow}>
            <Text style={styles.benefitEmoji}>💰</Text>
            <Text style={styles.benefitText} numberOfLines={2}>{meta.benefit}</Text>
          </View>
        )}
        <Text style={styles.tapHint}>Tap for details →</Text>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator color={Colors.primary} size="large" />
          <Text style={styles.loadingText}>Loading schemes...</Text>
        </View>
      ) : (
        <FlatList
          data={schemes}
          keyExtractor={item => item.doc_id}
          renderItem={renderScheme}
          contentContainerStyle={styles.list}
          ListHeaderComponent={
            <View>
              <Text style={styles.header}>🏛️ Government Schemes</Text>
              <Text style={styles.subheader}>Available for Mandya district farmers</Text>
            </View>
          }
        />
      )}

      {/* Detail Modal */}
      <Modal visible={!!selected} animationType="slide" transparent onRequestClose={() => setSelected(null)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            {selected && <SchemeDetail scheme={selected} parseMeta={parseMeta} onClose={() => setSelected(null)} navigation={navigation} />}
          </View>
        </View>
      </Modal>
    </View>
  );
}

function SchemeDetail({ scheme, parseMeta, onClose, navigation }) {
  const meta = parseMeta(scheme);
  const color = SCHEME_COLORS[meta.type] || SCHEME_COLORS.default;

  return (
    <ScrollView showsVerticalScrollIndicator={false}>
      <View style={styles.modalHeader}>
        <Text style={styles.modalTitle}>{meta.full_name || scheme.title}</Text>
        <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
          <Text style={styles.closeBtnText}>✕</Text>
        </TouchableOpacity>
      </View>

      <View style={[styles.typeBadge, { backgroundColor: color + '22', alignSelf: 'flex-start', marginBottom: Spacing.md }]}>
        <Text style={[styles.typeText, { color }]}>{meta.type?.toUpperCase()} SCHEME</Text>
      </View>

      {[
        ['💰 Benefit',        meta.benefit],
        ['✅ Eligibility',    meta.eligibility],
        ['📋 Premium/Cost',   meta.premium],
        ['📝 How to Apply',   meta.how_to_apply],
        ['📄 Documents',      meta.documents],
        ['🌐 Website',        meta.website],
        ['📞 Helpline',       meta.helpline],
      ].filter(([, v]) => v).map(([label, value]) => (
        <View key={label} style={styles.detailBlock}>
          <Text style={styles.detailLabel}>{label}</Text>
          <Text style={styles.detailValue}>{value}</Text>
        </View>
      ))}

      <TouchableOpacity
        style={styles.askBtn}
        onPress={() => {
          onClose();
          navigation.navigate('Chat', { initialQuery: `Tell me about ${scheme.title}` });
        }}
      >
        <Text style={styles.askBtnText}>💬 Ask About This Scheme</Text>
      </TouchableOpacity>
      <View style={{ height: 20 }} />
    </ScrollView>
  );
}

const SCHEME_COLORS_MODULE = SCHEME_COLORS; // avoid closure re-export issue

const styles = StyleSheet.create({
  container:   { flex: 1, backgroundColor: Colors.background },
  centered:    { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40 },
  loadingText: { color: Colors.textMuted, marginTop: 12 },
  list:        { padding: Spacing.md },
  header:      { fontSize: Fonts.sizes.xl, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, marginBottom: 4 },
  subheader:   { fontSize: Fonts.sizes.sm, color: Colors.textMuted, marginBottom: Spacing.lg },

  schemeCard: {
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderLeftWidth: 4,
    borderRadius: Radius.md,
    padding: Spacing.md,
    marginBottom: Spacing.sm,
  },
  schemeTop:    { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm, marginBottom: 4 },
  schemeName:   { fontSize: Fonts.sizes.lg, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, flex: 1 },
  schemeFullName: { fontSize: Fonts.sizes.sm, color: Colors.textSecondary, marginBottom: Spacing.sm, fontStyle: 'italic' },
  typeBadge:    { paddingVertical: 2, paddingHorizontal: 8, borderRadius: Radius.full },
  typeText:     { fontSize: Fonts.sizes.xs, fontWeight: Fonts.weights.bold },

  benefitRow:  { flexDirection: 'row', alignItems: 'flex-start', gap: Spacing.xs },
  benefitEmoji:{ fontSize: 14 },
  benefitText: { fontSize: Fonts.sizes.sm, color: Colors.accent, flex: 1, lineHeight: 20 },
  tapHint:     { fontSize: Fonts.sizes.xs, color: Colors.primary, marginTop: Spacing.sm, fontWeight: Fonts.weights.medium },

  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'flex-end' },
  modalCard:    { backgroundColor: Colors.surface, borderTopLeftRadius: Radius.xl, borderTopRightRadius: Radius.xl, padding: Spacing.xl, maxHeight: '85%' },
  modalHeader:  { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: Spacing.md },
  modalTitle:   { fontSize: Fonts.sizes.lg, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, flex: 1, marginRight: Spacing.sm },
  closeBtn:     { width: 32, height: 32, borderRadius: 16, backgroundColor: Colors.surfaceHigh, alignItems: 'center', justifyContent: 'center' },
  closeBtnText: { color: Colors.textPrimary, fontSize: 16 },

  detailBlock:  { marginBottom: Spacing.md, paddingBottom: Spacing.md, borderBottomWidth: 1, borderBottomColor: Colors.surfaceBorder },
  detailLabel:  { fontSize: Fonts.sizes.sm, fontWeight: Fonts.weights.semibold, color: Colors.textSecondary, marginBottom: 4 },
  detailValue:  { fontSize: Fonts.sizes.md, color: Colors.textPrimary, lineHeight: 22 },

  askBtn:       { backgroundColor: Colors.primary, borderRadius: Radius.full, padding: Spacing.md, alignItems: 'center', marginTop: Spacing.xl },
  askBtnText:   { fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.bold, color: Colors.textDark },
});
