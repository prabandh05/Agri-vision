import React, { useEffect, useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet,
  ActivityIndicator, Modal, ScrollView,
} from 'react-native';
import { Colors, Fonts, Spacing, Radius, Shadow } from '../constants/theme';
import { getAllCrops } from '../database/DatabaseService';

export default function CropsScreen({ navigation }) {
  const [crops, setCrops]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    getAllCrops().then(data => {
      setCrops(data);
      setLoading(false);
    });
  }, []);

  const parseMeta = (row) => {
    try { return JSON.parse(row.metadata || '{}'); }
    catch { return {}; }
  };

  const renderCrop = ({ item }) => {
    const meta = parseMeta(item);
    const seasons = Array.isArray(meta.season) ? meta.season.join(', ') : meta.season || '—';

    return (
      <TouchableOpacity style={[styles.cropCard, Shadow.card]} onPress={() => setSelected(item)} activeOpacity={0.8}>
        <View style={styles.cropHeader}>
          <Text style={styles.cropEmoji}>
            {meta.category === 'cereal' ? '🌾' :
             meta.category === 'millet' ? '🌽' :
             meta.category === 'commercial' ? '🌿' :
             meta.category === 'plantation' ? '🌴' :
             meta.category === 'fruit' ? '🍌' :
             meta.category === 'vegetable' ? '🍅' :
             meta.category === 'spice' ? '🌼' :
             meta.category === 'sericulture' ? '🦋' : '🌱'}
          </Text>
          <View style={styles.cropInfo}>
            <Text style={styles.cropName}>{item.title}</Text>
            <Text style={styles.cropLocal}>{meta.local_name || ''}</Text>
          </View>
          <View style={[styles.cropTypeBadge, { backgroundColor: meta.type === 'irrigated' ? Colors.water + '33' : Colors.organic + '33' }]}>
            <Text style={[styles.cropTypeText, { color: meta.type === 'irrigated' ? Colors.water : Colors.organic }]}>
              {meta.type === 'irrigated' ? '💧' : '☔'} {meta.type}
            </Text>
          </View>
        </View>
        <View style={styles.cropMeta}>
          <Text style={styles.metaItem}>📅 {seasons}</Text>
          <Text style={styles.metaItem}>📊 {meta.yield_quintals_per_acre || '—'} qtl/acre</Text>
          <Text style={styles.metaItem}>💰 {meta.msp_per_quintal || '—'}</Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator color={Colors.primary} size="large" />
          <Text style={styles.loadingText}>Loading crops...</Text>
        </View>
      ) : (
        <FlatList
          data={crops}
          keyExtractor={item => item.doc_id}
          renderItem={renderCrop}
          contentContainerStyle={styles.list}
          ListHeaderComponent={
            <Text style={styles.header}>🌾 Mandya District Crops ({crops.length})</Text>
          }
        />
      )}

      {/* Detail Modal */}
      <Modal visible={!!selected} animationType="slide" transparent onRequestClose={() => setSelected(null)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            {selected && <CropDetail crop={selected} parseMeta={parseMeta} onClose={() => setSelected(null)} navigation={navigation} />}
          </View>
        </View>
      </Modal>
    </View>
  );
}

function CropDetail({ crop, parseMeta, onClose, navigation }) {
  const meta = parseMeta(crop);
  return (
    <ScrollView showsVerticalScrollIndicator={false}>
      <View style={styles.modalHeader}>
        <Text style={styles.modalTitle}>{crop.title}</Text>
        <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
          <Text style={styles.closeBtnText}>✕</Text>
        </TouchableOpacity>
      </View>

      {meta.local_name && <Text style={styles.localName}>📛 {meta.local_name}</Text>}

      {[
        ['📅 Season', Array.isArray(meta.season) ? meta.season.join(', ') : meta.season],
        ['⏱️ Duration', `${meta.duration_days} days`],
        ['💧 Water Need', meta.water_requirement],
        ['📊 Yield', `${meta.yield_quintals_per_acre} quintals/acre`],
        ['💰 MSP', meta.msp_per_quintal],
        ['📍 Suitable Taluks', meta.suitable_taluks?.join(', ')],
      ].filter(([, v]) => v).map(([label, value]) => (
        <View key={label} style={styles.detailRow}>
          <Text style={styles.detailLabel}>{label}</Text>
          <Text style={styles.detailValue}>{value}</Text>
        </View>
      ))}

      {meta.recommended_varieties?.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🌱 Recommended Varieties</Text>
          {meta.recommended_varieties.map((v, i) => (
            <Text key={i} style={styles.bullet}>• {v}</Text>
          ))}
        </View>
      )}

      {meta.fertilizer_schedule && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🧪 Fertilizer Schedule</Text>
          {Object.entries(meta.fertilizer_schedule).map(([k, v]) => (
            <View key={k} style={styles.fertRow}>
              <Text style={styles.fertKey}>{k.replace(/_/g, ' ').toUpperCase()}</Text>
              <Text style={styles.fertVal}>{v}</Text>
            </View>
          ))}
        </View>
      )}

      <TouchableOpacity
        style={styles.askBtn}
        onPress={() => { onClose(); navigation.navigate('Chat', { initialQuery: `Tell me about ${crop.title} cultivation in Mandya` }); }}
      >
        <Text style={styles.askBtnText}>💬 Ask About This Crop</Text>
      </TouchableOpacity>
      <View style={{ height: 20 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  centered:  { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40 },
  loadingText: { color: Colors.textMuted, marginTop: 12 },
  list:      { padding: Spacing.md },
  header:    { fontSize: Fonts.sizes.xl, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, marginBottom: Spacing.lg },

  cropCard:  { backgroundColor: Colors.surface, borderWidth: 1, borderColor: Colors.surfaceBorder, borderRadius: Radius.lg, padding: Spacing.md, marginBottom: Spacing.sm },
  cropHeader:{ flexDirection: 'row', alignItems: 'center', gap: Spacing.sm },
  cropEmoji: { fontSize: 32 },
  cropInfo:  { flex: 1 },
  cropName:  { fontSize: Fonts.sizes.lg, fontWeight: Fonts.weights.bold, color: Colors.textPrimary },
  cropLocal: { fontSize: Fonts.sizes.sm, color: Colors.textMuted, fontStyle: 'italic' },
  cropTypeBadge: { borderRadius: Radius.full, paddingVertical: 3, paddingHorizontal: 8 },
  cropTypeText:  { fontSize: Fonts.sizes.xs, fontWeight: Fonts.weights.medium },
  cropMeta:  { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm, marginTop: Spacing.sm },
  metaItem:  { fontSize: Fonts.sizes.xs, color: Colors.textSecondary, backgroundColor: Colors.surfaceHigh, paddingVertical: 2, paddingHorizontal: 6, borderRadius: Radius.sm },

  // Modal
  modalOverlay:{ flex: 1, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'flex-end' },
  modalCard:   { backgroundColor: Colors.surface, borderTopLeftRadius: Radius.xl, borderTopRightRadius: Radius.xl, padding: Spacing.xl, maxHeight: '85%' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: Spacing.md },
  modalTitle:  { fontSize: Fonts.sizes.xl, fontWeight: Fonts.weights.bold, color: Colors.textPrimary, flex: 1 },
  closeBtn:    { width: 32, height: 32, borderRadius: 16, backgroundColor: Colors.surfaceHigh, alignItems: 'center', justifyContent: 'center' },
  closeBtnText:{ color: Colors.textPrimary, fontSize: 16 },
  localName:   { fontSize: Fonts.sizes.md, color: Colors.primaryLight, fontStyle: 'italic', marginBottom: Spacing.sm },

  detailRow:   { flexDirection: 'row', paddingVertical: Spacing.xs, borderBottomWidth: 1, borderBottomColor: Colors.surfaceBorder },
  detailLabel: { width: 140, fontSize: Fonts.sizes.sm, fontWeight: Fonts.weights.medium, color: Colors.textSecondary },
  detailValue: { flex: 1, fontSize: Fonts.sizes.sm, color: Colors.textPrimary },

  section:     { marginTop: Spacing.md },
  sectionTitle:{ fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.bold, color: Colors.primary, marginBottom: Spacing.sm },
  bullet:      { fontSize: Fonts.sizes.sm, color: Colors.textSecondary, marginLeft: Spacing.sm, lineHeight: 22 },
  fertRow:     { marginBottom: Spacing.xs },
  fertKey:     { fontSize: Fonts.sizes.xs, color: Colors.accent, fontWeight: Fonts.weights.semibold },
  fertVal:     { fontSize: Fonts.sizes.sm, color: Colors.textSecondary, lineHeight: 20 },

  askBtn:      { backgroundColor: Colors.primary, borderRadius: Radius.full, padding: Spacing.md, alignItems: 'center', marginTop: Spacing.xl },
  askBtnText:  { fontSize: Fonts.sizes.md, fontWeight: Fonts.weights.bold, color: Colors.textDark },
});
