/**
 * DatabaseService.js
 * Handles copying the bundled SQLite DB to device storage and running FTS5 queries.
 * Works fully offline — no network calls.
 */
import * as FileSystem from 'expo-file-system';
import * as SQLite from 'expo-sqlite';
import { Asset } from 'expo-asset';

const DB_NAME = 'mandya_agri.db';
const DB_DIR  = FileSystem.documentDirectory + 'SQLite/';
const DB_PATH = DB_DIR + DB_NAME;

let _db = null;

// ─── Initialization ──────────────────────────────────────────────────────────

export async function initDatabase() {
  if (_db) return _db;

  // Ensure SQLite directory exists
  const dirInfo = await FileSystem.getInfoAsync(DB_DIR);
  if (!dirInfo.exists) {
    await FileSystem.makeDirectoryAsync(DB_DIR, { intermediates: true });
  }

  // Check if DB already copied to device
  const dbInfo = await FileSystem.getInfoAsync(DB_PATH);
  if (!dbInfo.exists) {
    // Load from bundled asset
    const asset = Asset.fromModule(require('../../assets/db/mandya_agri.db'));
    await asset.downloadAsync();
    await FileSystem.copyAsync({
      from: asset.localUri,
      to:   DB_PATH,
    });
    console.log('✅ AgriVision DB copied to device storage');
  }

  // Open database — expo-sqlite v55: pass just the name, it auto-resolves to documentDirectory/SQLite/
  _db = await SQLite.openDatabaseAsync(DB_NAME);
  console.log('✅ AgriVision DB opened');
  return _db;
}

export function getDb() {
  return _db;
}

// ─── FTS5 Query Helpers ───────────────────────────────────────────────────────

/**
 * Sanitize query text for FTS5 — remove special chars that break the parser.
 */
function sanitizeFts(text) {
  // Remove non-alphanumeric characters (keep spaces)
  const cleaned = text.replace(/[^\w\s]/g, ' ');
  const tokens  = cleaned.split(/\s+/).filter(t => t.length > 1).map(t => t.toLowerCase());
  return tokens.join(' OR ');
}

/**
 * FTS5 full-text search on knowledge_fts virtual table.
 */
export async function ftsSearch(queryText, limit = 15) {
  const db = await initDatabase();
  const ftsQuery = sanitizeFts(queryText);
  if (!ftsQuery) return [];

  try {
    const rows = await db.getAllAsync(
      `SELECT k.doc_id, k.category, k.title, k.content, k.metadata, k.crop, k.tags, fts.rank
       FROM knowledge_fts fts
       JOIN knowledge k ON k.id = fts.rowid
       WHERE knowledge_fts MATCH ?
       ORDER BY fts.rank
       LIMIT ?`,
      [ftsQuery, limit]
    );
    return rows.map(r => ({
      ...r,
      fts_rank: Math.abs(r.rank || 0),
      source: 'fts5',
    }));
  } catch (e) {
    console.warn('FTS5 error:', e.message);
    return [];
  }
}

/**
 * Direct category-filtered search.
 */
export async function searchByCategory(category, limit = 20) {
  const db = await initDatabase();
  try {
    return await db.getAllAsync(
      `SELECT doc_id, category, title, content, metadata, crop, tags
       FROM knowledge
       WHERE category = ? AND doc_id NOT LIKE '%_faq_%'
       ORDER BY title
       LIMIT ?`,
      [category, limit]
    );
  } catch (e) {
    console.warn('Category search error:', e.message);
    return [];
  }
}

/**
 * Get a single entry by doc_id.
 */
export async function getEntryById(docId) {
  const db = await initDatabase();
  try {
    return await db.getFirstAsync(
      'SELECT * FROM knowledge WHERE doc_id = ?',
      [docId]
    );
  } catch (e) {
    return null;
  }
}

/**
 * Get all crops.
 */
export async function getAllCrops() {
  return searchByCategory('crop', 50);
}

/**
 * Get all schemes.
 */
export async function getAllSchemes() {
  return searchByCategory('scheme', 50);
}

/**
 * Get diseases for a specific crop.
 */
export async function getDiseasesForCrop(cropName) {
  const db = await initDatabase();
  try {
    return await db.getAllAsync(
      `SELECT doc_id, category, title, content, metadata, crop, tags
       FROM knowledge
       WHERE category = 'disease' AND doc_id NOT LIKE '%_faq_%'
       AND (crop LIKE ? OR content LIKE ?)
       LIMIT 30`,
      [`%${cropName}%`, `%${cropName}%`]
    );
  } catch (e) {
    return [];
  }
}

/**
 * Get DB statistics.
 */
export async function getDbStats() {
  const db = await initDatabase();
  try {
    const total = await db.getFirstAsync('SELECT COUNT(*) as count FROM knowledge');
    const cats  = await db.getAllAsync(
      'SELECT category, COUNT(*) as count FROM knowledge GROUP BY category'
    );
    return { total: total?.count || 0, categories: cats };
  } catch (e) {
    return { total: 0, categories: [] };
  }
}
