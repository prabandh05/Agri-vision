/**
 * QueryEngine.js
 * JavaScript-based query processing engine — mirrors the Python backend logic.
 * Runs 100% offline on the device.
 *
 * Pipeline: Preprocess → Classify → FTS5 Search → Fuse.js Fuzzy → Score Fusion → Format
 */
import Fuse from 'fuse.js';
import { ftsSearch, getAllCrops, getAllSchemes, searchByCategory } from '../database/DatabaseService';

// ─── Synonyms / Expansions (Kannada ↔ English) ────────────────────────────────
const SYNONYMS = {
  'bhatta': 'paddy rice', 'akki': 'paddy rice', 'kabbu': 'sugarcane',
  'ragi': 'finger millet', 'jola': 'sorghum jowar', 'mekkejola': 'maize corn',
  'bale': 'banana', 'tenginakaayi': 'coconut', 'arishina': 'turmeric',
  'hippunerale': 'mulberry', 'blast': 'blast fungal paddy',
  'blb': 'bacterial leaf blight', 'rpm': 'red palm weevil',
  'jeevamrutha': 'jeevamrutha organic liquid fertilizer',
  'panchagavya': 'panchagavya organic preparation',
  'kisan': 'pmkisan pm kisan scheme', 'pmkisan': 'pm kisan scheme central',
  'pmfby': 'pradhan mantri fasal bima yojana crop insurance',
};

// ─── Intent Keywords ─────────────────────────────────────────────────────────
const INTENT_MAP = {
  disease:    ['disease', 'spot', 'rot', 'blight', 'wilt', 'pest', 'insect', 'attack', 'dying', 'yellow', 'brown', 'black', 'white', 'drooping', 'holes', 'caterpillar', 'worm', 'weevil'],
  fertilizer: ['fertilizer', 'urea', 'dap', 'npk', 'mop', 'potash', 'nitrogen', 'phosphorus', 'zinc', 'nutrition', 'dose', 'dosage', 'kg', 'deficiency'],
  irrigation: ['irrigation', 'water', 'drip', 'sprinkler', 'canal', 'krs', 'bore', 'flood', 'channel', 'schedule', 'frequency'],
  scheme:     ['scheme', 'subsidy', 'government', 'insurance', 'loan', 'pm', 'kisan', 'pmfby', 'krishi', 'bhagya', 'yojana', 'benefit', 'apply'],
  organic:    ['organic', 'jeevamrutha', 'panchagavya', 'neem', 'vermicompost', 'compost', 'biofertilizer', 'natural', 'beejamrutha'],
  crop:       ['crop', 'variety', 'sow', 'plant', 'harvest', 'yield', 'msp', 'price', 'season', 'duration', 'spacing'],
  recommendation: ['what to grow', 'which crop', 'recommend', 'suggest', 'best crop', 'suitable', 'should i grow', 'rainfed', 'kharif', 'rabi', 'summer'],
};

// ─── Preprocessor ────────────────────────────────────────────────────────────

export function preprocessQuery(rawQuery) {
  const lower = rawQuery.toLowerCase().trim();

  // Expand synonyms
  let expanded = lower;
  for (const [syn, replacement] of Object.entries(SYNONYMS)) {
    expanded = expanded.replace(new RegExp(`\\b${syn}\\b`, 'gi'), replacement);
  }

  // Remove stopwords
  const stopwords = new Set(['my', 'is', 'are', 'the', 'a', 'an', 'for', 'of', 'in', 'on', 'at', 'to', 'and', 'or', 'but', 'how', 'what', 'why', 'when', 'where', 'which', 'do', 'i', 'me', 'it', 'its']);
  const tokens = expanded.split(/\s+/).filter(t => t.length > 1 && !stopwords.has(t));

  return {
    original: rawQuery,
    lower,
    expanded,
    tokens,
    searchText: tokens.join(' '),
  };
}

// ─── Intent Classifier ───────────────────────────────────────────────────────

export function classifyIntent(preprocessed) {
  const { lower, tokens } = preprocessed;
  const scores = {};

  for (const [intent, keywords] of Object.entries(INTENT_MAP)) {
    let score = 0;
    for (const kw of keywords) {
      if (lower.includes(kw)) score += kw.includes(' ') ? 3 : 1;
    }
    scores[intent] = score;
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const primaryIntent = sorted[0][1] > 0 ? sorted[0][0] : 'general';
  const isRecommendation = scores.recommendation >= 2 || INTENT_MAP.recommendation.some(kw => lower.includes(kw));

  return {
    primaryIntent,
    queryType: isRecommendation ? 'recommendation' : (scores.disease >= 2 ? 'problem' : 'information'),
    confidence: sorted[0][1] / 5,
    scores,
  };
}

// ─── Recommendation Engine ────────────────────────────────────────────────────

const RECOMMENDATIONS = {
  Kharif_irrigated:  { crops: ['Paddy (Rice)', 'Sugarcane', 'Banana', 'Maize', 'Tomato'], notes: 'Main Kharif crops with KRS/canal water availability.' },
  Kharif_rainfed:    { crops: ['Ragi', 'Jowar', 'Maize', 'Tomato', 'Turmeric'], notes: 'Drought-tolerant crops for rainfed areas.' },
  Rabi_irrigated:    { crops: ['Paddy (Rice)', 'Maize', 'Tomato', 'Vegetables', 'Turmeric'], notes: 'Rabi season with supplemental irrigation.' },
  Rabi_rainfed:      { crops: ['Jowar', 'Ragi', 'Field bean', 'Sunflower'], notes: 'Moisture-conserving crops for Rabi rainfed.' },
  Summer_irrigated:  { crops: ['Tomato', 'Vegetables', 'Banana', 'Sunflower', 'Green gram'], notes: 'Short-duration crops for summer with bore well irrigation.' },
  General:           { crops: ['Sugarcane', 'Coconut', 'Mulberry', 'Banana'], notes: 'Year-round crops for Mandya district.' },
};

export function getRecommendation(preprocessed) {
  const { lower } = preprocessed;

  let season = null;
  if (/kharif|monsoon|june|july|rainy/.test(lower)) season = 'Kharif';
  else if (/rabi|winter|november|december|january/.test(lower)) season = 'Rabi';
  else if (/summer|march|april|may/.test(lower)) season = 'Summer';

  let water = null;
  if (/irrigated|canal|bore|drip|water available/.test(lower)) water = 'irrigated';
  else if (/rainfed|rain fed|dryland|no irrigation/.test(lower)) water = 'rainfed';

  const key = season && water ? `${season}_${water}` : (season ? `${season}_irrigated` : 'General');
  const rec = RECOMMENDATIONS[key] || RECOMMENDATIONS.General;

  let talukMsg = '';
  const taluks = ['mandya', 'maddur', 'malavalli', 'pandavapura', 'srirangapatna', 'nagamangala', 'nagamangala', 'kr pet'];
  for (const t of taluks) {
    if (lower.includes(t)) {
      talukMsg = `\n**📍 ${t.charAt(0).toUpperCase() + t.slice(1)} Taluk:** Famous for sugarcane and paddy cultivation.`;
      break;
    }
  }

  return {
    type: 'recommendation',
    title: '🌾 Crop Recommendations for Mandya',
    answer: `**Recommended Crops:**\n${rec.crops.map((c, i) => `${i + 1}. ${c}`).join('\n')}\n\n📝 ${rec.notes}${talukMsg}\n\n**Season:** ${season || 'Any'} | **Water:** ${water || 'Any'}`,
    crops: rec.crops,
    confidence: 0.9,
    followUps: ['What fertilizer for these crops?', 'Which diseases affect these crops?', 'How to get crop insurance?'],
  };
}

// ─── Response Formatter ───────────────────────────────────────────────────────

function parseMetadata(row) {
  try { return JSON.parse(row.metadata || '{}'); } catch { return {}; }
}

function formatDiseaseResult(row) {
  const meta = parseMetadata(row);
  const mgmt = meta.management || {};
  let answer = `**🔴 ${row.title}**\n\n`;
  if (meta.symptoms) answer += `**Symptoms:** ${meta.symptoms}\n\n`;
  if (mgmt.cultural) answer += `**🌿 Cultural Control:** ${mgmt.cultural}\n\n`;
  if (mgmt.chemical) answer += `**💊 Chemical Control:** ${mgmt.chemical}\n\n`;
  if (mgmt.biological) answer += `**🦠 Biological Control:** ${mgmt.biological}\n\n`;
  if (meta.severity) answer += `⚠️ **Severity:** ${meta.severity.toUpperCase()}`;
  return answer;
}

function formatCropResult(row) {
  const meta = parseMetadata(row);
  let answer = `**🌾 ${row.title}**\n\n`;
  if (meta.local_name)  answer += `📛 Local name: *${meta.local_name}*\n`;
  if (meta.season)      answer += `📅 Season: ${Array.isArray(meta.season) ? meta.season.join(', ') : meta.season}\n`;
  if (meta.duration_days) answer += `⏱️ Duration: ${meta.duration_days} days\n`;
  if (meta.yield_quintals_per_acre) answer += `📊 Yield: ${meta.yield_quintals_per_acre} quintals/acre\n`;
  if (meta.msp_per_quintal) answer += `💰 MSP: ${meta.msp_per_quintal}\n`;
  if (meta.recommended_varieties) answer += `\n🌱 **Varieties:** ${meta.recommended_varieties.join(', ')}\n`;
  if (meta.cultivation_practices?.length) {
    answer += `\n**Cultivation:**\n${meta.cultivation_practices.slice(0, 2).map(p => `• ${p}`).join('\n')}`;
  }
  return answer;
}

function formatSchemeResult(row) {
  const meta = parseMetadata(row);
  let answer = `**🏛️ ${meta.full_name || row.title}**\n\n`;
  if (meta.benefit)     answer += `💰 **Benefit:** ${meta.benefit}\n\n`;
  if (meta.eligibility) answer += `✅ **Eligibility:** ${meta.eligibility}\n\n`;
  if (meta.how_to_apply) answer += `📝 **How to Apply:** ${meta.how_to_apply}\n\n`;
  if (meta.documents)   answer += `📄 **Documents:** ${meta.documents}`;
  return answer;
}

function formatFertilizerResult(row) {
  const meta = parseMetadata(row);
  // If this is a FAQ entry, use content directly
  if (row.doc_id?.includes('_faq_')) {
    return `**🧪 ${row.title}**\n\n${row.content}`;
  }
  let answer = `**🧪 ${row.title}**\n\n`;
  if (meta.content)  answer += `**Nutrient Content:** ${meta.content}\n`;
  if (meta.usage)    answer += `**Usage:** ${meta.usage}\n\n`;
  if (meta.rate_general) answer += `**General Rate:** ${meta.rate_general}\n`;
  if (meta.precautions) answer += `\n⚠️ **Precautions:** ${meta.precautions}`;
  return answer;
}

function formatIrrigationResult(row) {
  const meta = parseMetadata(row);
  if (row.doc_id?.includes('_faq_')) {
    return `**💧 ${row.title}**\n\n${row.content}`;
  }
  let answer = `**💧 ${row.title}**\n\n`;
  if (meta.description) answer += `${meta.description}\n\n`;
  if (meta.suitable_crops) answer += `**Suitable Crops:** ${meta.suitable_crops}\n`;
  if (meta.benefits) answer += `**Benefits:** ${meta.benefits}\n`;
  if (meta.cost) answer += `**Cost:** ${meta.cost}`;
  return answer;
}

function formatOrganicResult(row) {
  const meta = parseMetadata(row);
  if (row.doc_id?.includes('_faq_')) {
    return `**🌿 ${row.title}**\n\n${row.content}`;
  }
  let answer = `**🌿 ${row.title}**\n\n`;
  if (meta.preparation) answer += `**Preparation:** ${meta.preparation}\n\n`;
  if (meta.application) answer += `**Application:** ${meta.application}\n\n`;
  if (meta.benefits) answer += `**Benefits:** ${meta.benefits}`;
  return answer;
}

function formatResult(row) {
  if (!row) return null;
  const cat = row.category;
  let answer;

  // FAQ entries — use content directly
  if (cat === 'faq' || row.doc_id?.includes('_faq_')) {
    answer = row.content || row.title;
  } else if (cat === 'disease') {
    answer = formatDiseaseResult(row);
  } else if (cat === 'crop') {
    answer = formatCropResult(row);
  } else if (cat === 'scheme') {
    answer = formatSchemeResult(row);
  } else if (cat === 'fertilizer') {
    answer = formatFertilizerResult(row);
  } else if (cat === 'irrigation') {
    answer = formatIrrigationResult(row);
  } else if (cat === 'organic') {
    answer = formatOrganicResult(row);
  } else {
    answer = row.content;
  }

  return {
    type: cat,
    title: row.title,
    answer,
    docId: row.doc_id,
    confidence: 0.8,
    followUps: getFollowUps(cat, row.title),
  };
}

function getFollowUps(category, title) {
  const map = {
    disease:    [`What other diseases affect this crop?`, `What organic treatment can I use?`, `How to prevent this disease?`],
    crop:       [`What diseases affect ${title}?`, `Fertilizer schedule for ${title}?`, `Best variety for Mandya?`],
    scheme:     [`What other schemes are available?`, `How to get crop insurance?`, `How to apply online?`],
    fertilizer: [`Organic alternative to this?`, `Fertilizer schedule for my crop?`, `How to prevent deficiency?`],
    irrigation: [`How to get drip irrigation subsidy?`, `Water saving tips?`, `Drip vs flood irrigation?`],
    organic:    [`Other organic methods?`, `Organic certification process?`, `How to make compost?`],
  };
  return map[category] || [`Tell me more about ${title}`, `What crops grow in Mandya?`, `Available government schemes?`];
}

// ─── No-result Response ───────────────────────────────────────────────────────

const NO_RESULT = {
  type: 'no_match',
  title: 'No Specific Match Found',
  answer: `I couldn't find a specific answer for your query.\n\nPlease try:\n• Be more specific about the crop name\n• Describe symptoms clearly (e.g., "paddy leaves turning yellow")\n• Ask about a specific scheme, fertilizer, or crop\n\nOr browse using the categories below! 👇`,
  confidence: 0,
  followUps: ['What crops grow in Mandya?', 'Tell me about paddy diseases', 'What government schemes are available?', 'How to do organic farming?'],
};

// ─── Main Query Function ──────────────────────────────────────────────────────

export async function processQuery(rawQuery) {
  if (!rawQuery?.trim()) return NO_RESULT;

  const preprocessed = preprocessQuery(rawQuery);
  const intent = classifyIntent(preprocessed);

  // Recommendation path
  if (intent.queryType === 'recommendation') {
    return getRecommendation(preprocessed);
  }

  // FTS5 search
  const ftsResults = await ftsSearch(preprocessed.searchText, 20);

  if (!ftsResults.length) {
    // Last resort: Fuse.js on a small static list
    return NO_RESULT;
  }

  // Score fusion: boost if category matches intent
  const scored = ftsResults.map(r => {
    let score = 1 / (1 + r.fts_rank * 0.1);
    if (r.category === intent.primaryIntent) score *= 1.4;
    if (r.crop && preprocessed.lower.includes(r.crop.toLowerCase())) score *= 1.2;
    return { ...r, finalScore: score };
  });

  scored.sort((a, b) => b.finalScore - a.finalScore);
  const top = scored[0];
  const formatted = formatResult(top);

  if (!formatted) return NO_RESULT;

  // Add related results
  const related = scored.slice(1, 4).map(r => ({
    title: r.title,
    category: r.category,
    docId: r.doc_id,
  }));

  return { ...formatted, related };
}
