#!/usr/bin/env python3
"""AgriVision Flask API - Development server for testing the intelligence layer."""
import json
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DB_PATH
from nlp.preprocessor import preprocess, extract_crop_mentions
from nlp.query_classifier import classify_query
from nlp.matcher import get_matcher
from engine.decision_engine import recommend_crops, detect_recommendation_params, get_fertilizer_recommendation
from engine.response_generator import format_response, format_recommendation_response

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM knowledge")
        count = cur.fetchone()[0]
        conn.close()
        return jsonify({"status": "healthy", "entries": count, "database": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def process_query():
    """Main query processing endpoint."""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "Empty query"}), 400
    
    # Step 1: Preprocess
    preprocessed = preprocess(query)
    
    # Step 2: Classify
    intent_info = classify_query(preprocessed)
    
    # Step 3: Extract crop mentions
    crops = extract_crop_mentions(query)
    
    # Step 4: Route based on query type
    if intent_info['query_type'] == 'recommendation':
        # Use decision engine
        params = detect_recommendation_params(preprocessed, intent_info)
        recommendation = recommend_crops(**params)
        response = format_recommendation_response(recommendation)
    else:
        # Use matcher for problem/information queries
        matcher = get_matcher()
        results = matcher.search(preprocessed, intent_info)
        response = format_response(results, intent_info['query_type'], intent_info['primary_intent'], preprocessed)
    
    response['debug'] = {
        'preprocessed_tokens': preprocessed.get('tokens', []),
        'intent': intent_info['primary_intent'],
        'query_type': intent_info['query_type'],
        'confidence': intent_info['confidence'],
        'crops_detected': crops
    }
    
    return jsonify(response)

@app.route('/api/crops', methods=['GET'])
def list_crops():
    """List all crops."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT doc_id, title, metadata FROM knowledge WHERE category='crop'")
        crops = []
        for row in cur.fetchall():
            meta = json.loads(row['metadata']) if row['metadata'] else {}
            crops.append({
                'id': row['doc_id'],
                'name': row['title'],
                'local_name': meta.get('local_name', ''),
                'category': meta.get('category', ''),
                'type': meta.get('type', ''),
                'season': meta.get('season', []),
                'water_requirement': meta.get('water_requirement', ''),
                'suitable_taluks': meta.get('suitable_taluks', [])
            })
        conn.close()
        return jsonify({"crops": crops, "total": len(crops)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crops/<name>', methods=['GET'])
def get_crop(name):
    """Get full crop details."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT metadata FROM knowledge WHERE category='crop' AND (doc_id=? OR title LIKE ?)", 
                     (name, f"%{name}%"))
        row = cur.fetchone()
        conn.close()
        if row:
            return jsonify(json.loads(row['metadata']))
        return jsonify({"error": "Crop not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases/<crop>', methods=['GET'])
def get_diseases(crop):
    """Get diseases for a crop."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT doc_id, title, metadata FROM knowledge WHERE category='disease' AND crop LIKE ? AND doc_id NOT LIKE '%_faq_%'",
                     (f"%{crop}%",))
        diseases = []
        for row in cur.fetchall():
            meta = json.loads(row['metadata']) if row['metadata'] else {}
            diseases.append({
                'id': row['doc_id'],
                'name': meta.get('name', row['title']),
                'type': meta.get('type', ''),
                'severity': meta.get('severity', ''),
                'symptoms': meta.get('symptoms', '')[:200] + '...'
            })
        conn.close()
        return jsonify({"crop": crop, "diseases": diseases, "total": len(diseases)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/schemes', methods=['GET'])
def list_schemes():
    """List government schemes."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT doc_id, title, metadata FROM knowledge WHERE category='scheme' AND doc_id NOT LIKE '%_faq_%'")
        schemes = []
        for row in cur.fetchall():
            meta = json.loads(row['metadata']) if row['metadata'] else {}
            schemes.append({
                'id': row['doc_id'],
                'name': meta.get('name', row['title']),
                'full_name': meta.get('full_name', ''),
                'type': meta.get('type', ''),
                'benefit': meta.get('benefit', '')
            })
        conn.close()
        return jsonify({"schemes": schemes, "total": len(schemes)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Get crop recommendations."""
    data = request.get_json()
    result = recommend_crops(
        season=data.get('season'),
        water=data.get('water'),
        soil=data.get('soil'),
        taluk=data.get('taluk')
    )
    return jsonify(result)

@app.route('/api/categories', methods=['GET'])
def categories():
    """Get all query categories."""
    return jsonify({
        "categories": [
            {"id": "disease", "name": "🔴 Crop Diseases & Pests", "description": "Identify and treat crop problems"},
            {"id": "fertilizer", "name": "🧪 Fertilizers & Nutrition", "description": "Dosage, schedule, application"},
            {"id": "irrigation", "name": "💧 Irrigation & Water", "description": "Canal, drip, water management"},
            {"id": "recommendation", "name": "🌾 Crop Recommendations", "description": "What to grow based on conditions"},
            {"id": "scheme", "name": "🏛️ Government Schemes", "description": "Subsidies, insurance, loans"},
            {"id": "organic", "name": "🌿 Organic Farming", "description": "Natural methods and preparations"},
            {"id": "cultivation", "name": "📋 Cultivation Guide", "description": "Sowing, harvesting, varieties"},
            {"id": "market", "name": "📊 Market & Pricing", "description": "Where to sell, MSP, mandis"}
        ]
    })

@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    """Get suggested queries."""
    category = request.args.get('category', 'all')
    
    all_suggestions = {
        "disease": [
            "My paddy leaves have brown spots",
            "Sugarcane has red color inside",
            "Coconut tree center leaf dying",
            "Caterpillar eating maize whorl",
            "Tomato leaves curling upward",
            "Ragi fingers breaking at base"
        ],
        "fertilizer": [
            "How much urea for paddy per acre?",
            "Fertilizer schedule for sugarcane",
            "When to apply DAP?",
            "Why is potash important?",
            "Paddy leaves turning bronze color"
        ],
        "irrigation": [
            "When does canal water start?",
            "How to install drip irrigation?",
            "Drip vs flood which is better?",
            "Water saving methods for farming",
            "Sprinkler irrigation for ragi"
        ],
        "recommendation": [
            "What to grow in Kharif season?",
            "Best crops for rainfed land",
            "Crops for Nagamangala taluk",
            "What to grow in Rabi season?",
            "Good crops for summer"
        ],
        "scheme": [
            "How to apply for PM-KISAN?",
            "How to get crop insurance?",
            "Subsidy for drip irrigation",
            "Government help for organic farming",
            "How to get farm loan?"
        ],
        "organic": [
            "How to make jeevamrutha?",
            "Organic seed treatment method",
            "What is panchagavya?",
            "How to make vermicompost?",
            "Organic farming for ragi"
        ]
    }
    
    if category != 'all' and category in all_suggestions:
        return jsonify({"suggestions": all_suggestions[category]})
    
    # Return mix of all
    mixed = []
    for cat_suggestions in all_suggestions.values():
        mixed.extend(cat_suggestions[:2])
    return jsonify({"suggestions": mixed})

if __name__ == '__main__':
    print("🌱 AgriVision API Server Starting...")
    print(f"📁 Database: {DB_PATH}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📖 Endpoints: /api/health, /api/query, /api/crops, /api/diseases/<crop>, /api/schemes, /api/recommend")
    app.run(debug=True, host='0.0.0.0', port=5000)
