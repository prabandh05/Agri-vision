#!/usr/bin/env python3
"""Seed SQLite database with FTS5 from knowledge base JSON files."""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH, DATA_DIR, MODELS_DIR, TFIDF_VECTORIZER_PATH, TFIDF_MATRIX_PATH, TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE

def create_tables(conn):
    """Create main and FTS5 tables."""
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS knowledge_fts")
    cur.execute("DROP TABLE IF EXISTS knowledge")
    
    cur.execute("""
        CREATE TABLE knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            search_text TEXT NOT NULL,
            metadata TEXT,
            crop TEXT,
            tags TEXT
        )
    """)
    
    cur.execute("""
        CREATE VIRTUAL TABLE knowledge_fts USING fts5(
            search_text,
            content='knowledge',
            content_rowid='id'
        )
    """)
    
    # Triggers for FTS sync
    cur.execute("""
        CREATE TRIGGER knowledge_ai AFTER INSERT ON knowledge BEGIN
            INSERT INTO knowledge_fts(rowid, search_text) VALUES (new.id, new.search_text);
        END
    """)
    
    conn.commit()

def seed_crops(conn, kb):
    """Seed crop entries."""
    cur = conn.cursor()
    count = 0
    for crop in kb.get('crops', []):
        doc_id = crop['id']
        title = crop['name']
        
        # Build searchable content
        content_parts = [
            f"{crop['name']} ({crop.get('local_name', '')})",
            f"Category: {crop['category']}. Type: {crop['type']}.",
            f"Season: {json.dumps(crop.get('season', []))}.",
            f"Varieties: {', '.join(crop.get('recommended_varieties', []))}.",
            f"Yield: {crop.get('yield_quintals_per_acre', 'N/A')} quintals/acre.",
            f"MSP: {crop.get('msp_per_quintal', 'N/A')}.",
            f"Suitable taluks: {', '.join(crop.get('suitable_taluks', []))}.",
        ]
        if crop.get('cultivation_practices'):
            content_parts.append("Cultivation: " + " ".join(crop['cultivation_practices']))
        
        content = " ".join(content_parts)
        
        # Search text includes everything
        search_parts = [title, crop.get('local_name', ''), crop['category'], crop['type']]
        search_parts.extend(crop.get('season', []))
        search_parts.extend(crop.get('recommended_varieties', []))
        search_parts.extend(crop.get('suitable_taluks', []))
        if crop.get('cultivation_practices'):
            search_parts.extend(crop['cultivation_practices'])
        search_text = ' '.join(search_parts).lower()
        
        tags = ','.join([crop['category'], crop['type']] + crop.get('season', []))
        
        cur.execute("""
            INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, 'crop', title, content, search_text, json.dumps(crop), crop['name'], tags))
        count += 1
    
    conn.commit()
    return count

def seed_diseases(conn, kb):
    """Seed disease entries including embedded FAQs."""
    cur = conn.cursor()
    count = 0
    faq_count = 0
    
    for disease in kb.get('diseases', []):
        doc_id = disease['id']
        title = f"{disease['name']} ({disease.get('crop', '')})"
        
        mgmt = disease.get('management', {})
        content_parts = [
            f"Disease: {disease['name']}. Crop: {disease.get('crop', '')}.",
            f"Type: {disease.get('type', '')}. Pathogen: {disease.get('pathogen', '')}.",
            f"Symptoms: {disease.get('symptoms', '')}.",
            f"Chemical: {mgmt.get('chemical', '')}.",
            f"Cultural: {mgmt.get('cultural', '')}.",
            f"Biological: {mgmt.get('biological', '')}.",
        ]
        content = " ".join(content_parts)
        
        search_parts = [disease['name'], disease.get('crop', ''), disease.get('type', ''),
                        disease.get('symptoms', ''), disease.get('pathogen', '')]
        for v in mgmt.values():
            search_parts.append(str(v))
        search_text = ' '.join(search_parts).lower()
        
        cur.execute("""
            INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, 'disease', title, content, search_text, json.dumps(disease), 
              disease.get('crop', ''), f"disease,{disease.get('type', '')},{disease.get('crop', '')}"))
        count += 1
        
        # Seed embedded FAQs
        for i, faq in enumerate(disease.get('faq', [])):
            faq_doc_id = f"{doc_id}_faq_{i}"
            faq_content = faq['a']
            faq_search = f"{faq['q']} {faq['a']}".lower()
            faq_meta = {**disease, 'faq_question': faq['q'], 'faq_answer': faq['a']}
            
            cur.execute("""
                INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (faq_doc_id, 'disease', faq['q'], faq_content, faq_search, 
                  json.dumps(faq_meta), disease.get('crop', ''), f"faq,disease,{disease.get('crop', '')}"))
            faq_count += 1
    
    conn.commit()
    return count, faq_count

def seed_section(conn, kb, section_key, category):
    """Generic seeder for schemes, fertilizers, irrigation, organic sections."""
    cur = conn.cursor()
    count = 0
    faq_count = 0
    
    for item in kb.get(section_key, []):
        doc_id = item.get('id', f"{category}_{count}")
        title = item.get('name', item.get('full_name', item.get('q', f'{category} {count}')))
        
        # Build content from all string fields
        content_parts = []
        for k, v in item.items():
            if k in ('id', 'faq'):
                continue
            if isinstance(v, str):
                content_parts.append(f"{k}: {v}")
            elif isinstance(v, dict):
                for dk, dv in v.items():
                    content_parts.append(f"{dk}: {dv}")
        content = " ".join(content_parts)
        
        search_text = content.lower()
        
        cur.execute("""
            INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, category, title, content, search_text, json.dumps(item), '', category))
        count += 1
        
        # Seed FAQs
        for i, faq in enumerate(item.get('faq', [])):
            faq_doc_id = f"{doc_id}_faq_{i}"
            faq_content = faq.get('a', '')
            faq_search = f"{faq.get('q', '')} {faq_content}".lower()
            
            cur.execute("""
                INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (faq_doc_id, category, faq.get('q', ''), faq_content, faq_search,
                  json.dumps({**item, 'faq_question': faq.get('q'), 'faq_answer': faq['a']}), '', f"faq,{category}"))
            faq_count += 1
    
    conn.commit()
    return count, faq_count

def seed_general_faq(conn, kb):
    """Seed general FAQ entries."""
    cur = conn.cursor()
    count = 0
    for item in kb.get('general_faq', []):
        doc_id = item.get('id', f"faq_{count}")
        title = item.get('q', '')
        content = item.get('a', '')
        search_text = f"{title} {content}".lower()
        category = item.get('category', 'faq')
        
        cur.execute("""
            INSERT INTO knowledge (doc_id, category, title, content, search_text, metadata, crop, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, 'faq', title, content, search_text, json.dumps(item), '', f"faq,{category}"))
        count += 1
    
    conn.commit()
    return count

def build_tfidf_index(conn):
    """Pre-compute TF-IDF vectors for all entries."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    import joblib
    
    cur = conn.cursor()
    cur.execute("SELECT doc_id, search_text FROM knowledge")
    rows = cur.fetchall()
    
    doc_ids = [r[0] for r in rows]
    texts = [r[1] for r in rows]
    
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        stop_words=None,  # We handle stopwords ourselves
        sublinear_tf=True
    )
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(vectorizer, TFIDF_VECTORIZER_PATH)
    joblib.dump({'matrix': tfidf_matrix, 'doc_ids': doc_ids}, TFIDF_MATRIX_PATH)
    
    return len(doc_ids)

def seed():
    """Main seeding function."""
    print("🌱 Seeding AgriVision Database...\n")
    
    # Load knowledge base
    kb_path = os.path.join(DATA_DIR, "mandya_knowledge_base.json")
    with open(kb_path) as f:
        kb = json.load(f)
    
    # Create database
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    
    # Seed all sections
    crop_count = seed_crops(conn, kb)
    print(f"  ✓ Crops: {crop_count}")
    
    disease_count, disease_faq = seed_diseases(conn, kb)
    print(f"  ✓ Diseases: {disease_count} (+{disease_faq} FAQs)")
    
    scheme_count, scheme_faq = seed_section(conn, kb, 'schemes', 'scheme')
    print(f"  ✓ Schemes: {scheme_count} (+{scheme_faq} FAQs)")
    
    fert_count, fert_faq = seed_section(conn, kb, 'fertilizers', 'fertilizer')
    print(f"  ✓ Fertilizers: {fert_count} (+{fert_faq} FAQs)")
    
    irr_count, irr_faq = seed_section(conn, kb, 'irrigation', 'irrigation')
    print(f"  ✓ Irrigation: {irr_count} (+{irr_faq} FAQs)")
    
    org_count, org_faq = seed_section(conn, kb, 'organic_farming', 'organic')
    print(f"  ✓ Organic farming: {org_count} (+{org_faq} FAQs)")
    
    faq_count = seed_general_faq(conn, kb)
    print(f"  ✓ General FAQs: {faq_count}")
    
    # Verify
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM knowledge")
    total = cur.fetchone()[0]
    print(f"\n  Total entries in database: {total}")
    
    # Build TF-IDF index
    print("\n📊 Building TF-IDF index...")
    tfidf_count = build_tfidf_index(conn)
    print(f"  ✓ TF-IDF vectors computed for {tfidf_count} documents")
    
    conn.close()
    
    db_size = os.path.getsize(DB_PATH)
    print(f"\n✅ Database created: {DB_PATH}")
    print(f"   Size: {db_size / 1024:.1f} KB")
    print(f"   Ready for deployment!")

if __name__ == "__main__":
    seed()
