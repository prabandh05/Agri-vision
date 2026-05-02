"""Multi-stage matching engine: FTS5 + TF-IDF + Fuzzy matching."""
import os
import json
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz, process
import joblib

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH, TFIDF_VECTORIZER_PATH, TFIDF_MATRIX_PATH, FUZZY_THRESHOLD, CONFIDENCE_THRESHOLD, MAX_RESULTS

class AgriMatcher:
    def __init__(self):
        self.db_path = DB_PATH
        self.vectorizer = None
        self.tfidf_matrix = None
        self.doc_ids = []
        self._load_models()
    
    def _load_models(self):
        """Load pre-computed TF-IDF models."""
        try:
            self.vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
            data = joblib.load(TFIDF_MATRIX_PATH)
            self.tfidf_matrix = data['matrix']
            self.doc_ids = data['doc_ids']
        except FileNotFoundError:
            print("Warning: TF-IDF models not found. Run seed_database.py first.")
            self.vectorizer = None
    
    @staticmethod
    def _sanitize_fts_query(query_text):
        """Sanitize query for FTS5 — strip special chars that FTS5 treats as operators."""
        import re
        # Replace hyphens with space, remove characters that FTS5 uses as operators
        cleaned = re.sub(r'[^\w\s]', ' ', query_text)
        # Split, filter empty/short tokens, lowercase
        tokens = [t.lower() for t in cleaned.split() if len(t) > 1]
        if not tokens:
            return None
        # FTS5 reserved words that would be misinterpreted as column names: avoid bare uppercase
        return ' OR '.join(tokens)

    def fts5_search(self, query_text, limit=20):
        """Stage 1: Full-text search using SQLite FTS5."""
        results = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            # Clean query for FTS5 — sanitize special chars before building OR query
            fts_query = self._sanitize_fts_query(query_text)
            if not fts_query:
                return results
            
            cur.execute("""
                SELECT k.*, fts.rank
                FROM knowledge_fts fts
                JOIN knowledge k ON k.id = fts.rowid
                WHERE knowledge_fts MATCH ?
                ORDER BY fts.rank
                LIMIT ?
            """, (fts_query, limit))
            
            for row in cur.fetchall():
                results.append({
                    'doc_id': row['doc_id'],
                    'category': row['category'],
                    'title': row['title'],
                    'content': row['content'],
                    'metadata': row['metadata'],
                    'fts_rank': abs(row['rank']),
                    'source': 'fts5'
                })
            conn.close()
        except Exception as e:
            print(f"FTS5 search error: {e}")
        return results
    
    def tfidf_search(self, query_text, limit=20):
        """Stage 2: TF-IDF cosine similarity search."""
        if self.vectorizer is None:
            return []
        
        try:
            query_vec = self.vectorizer.transform([query_text])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            top_indices = similarities.argsort()[-limit:][::-1]
            
            results = []
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            for idx in top_indices:
                if similarities[idx] < 0.01:
                    continue
                doc_id = self.doc_ids[idx]
                cur.execute("SELECT * FROM knowledge WHERE doc_id = ?", (doc_id,))
                row = cur.fetchone()
                if row:
                    results.append({
                        'doc_id': row['doc_id'],
                        'category': row['category'],
                        'title': row['title'],
                        'content': row['content'],
                        'metadata': row['metadata'],
                        'tfidf_score': float(similarities[idx]),
                        'source': 'tfidf'
                    })
            conn.close()
            return results
        except Exception as e:
            print(f"TF-IDF search error: {e}")
            return []
    
    def fuzzy_search(self, query_text, candidates, limit=10):
        """Stage 3: Fuzzy string matching on candidate titles/content."""
        if not candidates:
            return []
        
        # Build searchable strings from candidates
        search_strings = []
        for c in candidates:
            search_str = f"{c['title']} {c['content'][:200]}"
            search_strings.append(search_str)
        
        # Use RapidFuzz for fast fuzzy matching
        fuzzy_results = []
        for i, c in enumerate(candidates):
            score = fuzz.token_set_ratio(query_text, search_strings[i])
            if score >= FUZZY_THRESHOLD:
                c_copy = dict(c)
                c_copy['fuzzy_score'] = score / 100.0
                fuzzy_results.append(c_copy)
        
        fuzzy_results.sort(key=lambda x: x['fuzzy_score'], reverse=True)
        return fuzzy_results[:limit]
    
    def search(self, preprocessed, intent_info=None):
        """Multi-stage search combining FTS5 + TF-IDF + Fuzzy.
        
        Args:
            preprocessed: dict from preprocessor
            intent_info: dict from query_classifier
        
        Returns:
            list of ranked results with combined scores
        """
        search_text = preprocessed.get('search_text', preprocessed.get('cleaned', ''))
        
        # Stage 1: FTS5
        fts_results = self.fts5_search(search_text)
        
        # Stage 2: TF-IDF
        tfidf_results = self.tfidf_search(search_text)
        
        # Combine candidates (deduplicate by doc_id)
        candidates = {}
        for r in fts_results:
            candidates[r['doc_id']] = r
            candidates[r['doc_id']]['fts_rank'] = r.get('fts_rank', 0)
        
        for r in tfidf_results:
            if r['doc_id'] in candidates:
                candidates[r['doc_id']]['tfidf_score'] = r.get('tfidf_score', 0)
            else:
                candidates[r['doc_id']] = r
        
        candidate_list = list(candidates.values())
        
        # Stage 3: Fuzzy matching on combined candidates
        if candidate_list:
            fuzzy_results = self.fuzzy_search(search_text, candidate_list)
            for fr in fuzzy_results:
                if fr['doc_id'] in candidates:
                    candidates[fr['doc_id']]['fuzzy_score'] = fr['fuzzy_score']
        
        # Score fusion
        final_results = []
        for doc_id, r in candidates.items():
            fts_score = min(r.get('fts_rank', 0) / 10.0, 1.0) if r.get('fts_rank') else 0
            tfidf_score = r.get('tfidf_score', 0)
            fuzzy_score = r.get('fuzzy_score', 0)
            
            # Weighted combination
            combined = (fts_score * 0.3) + (tfidf_score * 0.4) + (fuzzy_score * 0.3)
            
            # Context boost: if result category matches detected intent
            if intent_info:
                intent = intent_info.get('primary_intent', '')
                if r.get('category', '') == intent:
                    combined *= 1.3
                # Boost if crop mentioned in query matches result
                if intent in r.get('content', '').lower():
                    combined *= 1.1
            
            r['combined_score'] = round(combined, 4)
            final_results.append(r)
        
        # Sort by combined score
        final_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Apply confidence threshold
        filtered = [r for r in final_results if r['combined_score'] >= CONFIDENCE_THRESHOLD]
        
        if not filtered and final_results:
            filtered = final_results[:3]  # Return top 3 even if below threshold
        
        return filtered[:MAX_RESULTS]

# Singleton
_matcher_instance = None
def get_matcher():
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = AgriMatcher()
    return _matcher_instance
