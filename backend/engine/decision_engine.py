"""Rule-based decision engine for crop/fertilizer/irrigation recommendations."""
import json
import os
import sqlite3

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

_recommendations_cache = None

def _load_recommendations():
    global _recommendations_cache
    if _recommendations_cache is not None:
        return _recommendations_cache
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "crop_recommendations.json")
    try:
        with open(path) as f:
            _recommendations_cache = json.load(f)
    except FileNotFoundError:
        _recommendations_cache = {"rules": [], "taluk_specific": {}}
    return _recommendations_cache

def recommend_crops(season=None, water=None, soil=None, taluk=None):
    """Recommend crops based on factors.
    
    Args:
        season: 'Kharif', 'Rabi', 'Summer', 'Year-round'
        water: 'irrigated', 'rainfed'
        soil: 'red_sandy_loam', 'clay_loam', 'laterite', 'deep_loam', 'any'
        taluk: taluk name or None
    
    Returns:
        dict with recommendations, notes, and taluk-specific info
    """
    data = _load_recommendations()
    results = []
    
    # Match rules
    for rule in data.get('rules', []):
        score = 0
        if season and rule['season'].lower() == season.lower():
            score += 3
        elif rule['season'] == 'Year-round':
            score += 1
        
        if water and rule['water'].lower() == water.lower():
            score += 2
        
        if soil and (rule['soil'].lower() == soil.lower() or rule['soil'] == 'any'):
            score += 1
        elif not soil:
            score += 0.5
        
        if score >= 3:
            results.append({
                'crops': rule['crops'],
                'notes': rule['notes'],
                'match_score': score,
                'season': rule['season'],
                'water': rule['water'],
                'soil': rule['soil']
            })
    
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Taluk-specific info
    taluk_info = None
    if taluk:
        taluk_data = data.get('taluk_specific', {})
        taluk_info = taluk_data.get(taluk) or taluk_data.get(taluk.title())
    
    # Build response
    all_crops = []
    for r in results[:5]:
        all_crops.extend(r['crops'])
    all_crops = list(dict.fromkeys(all_crops))  # Deduplicate preserving order
    
    return {
        'recommended_crops': all_crops[:10],
        'detailed_matches': results[:5],
        'taluk_info': taluk_info,
        'parameters': {'season': season, 'water': water, 'soil': soil, 'taluk': taluk}
    }

def get_crop_details(crop_name):
    """Get full crop details from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM knowledge WHERE category='crop' AND title LIKE ?", (f"%{crop_name}%",))
        row = cur.fetchone()
        conn.close()
        if row:
            return json.loads(row['metadata']) if row['metadata'] else None
    except Exception:
        pass
    return None

def get_fertilizer_recommendation(crop_name, stage=None):
    """Get fertilizer recommendation for a crop."""
    details = get_crop_details(crop_name)
    if details and 'fertilizer_schedule' in details:
        return {
            'crop': crop_name,
            'schedule': details['fertilizer_schedule'],
            'organic_alternative': details.get('organic_practices', ''),
            'stage': stage
        }
    return None

def detect_recommendation_params(preprocessed, intent_info):
    """Extract recommendation parameters from query."""
    text = preprocessed.get('cleaned', '')
    tokens = preprocessed.get('expanded_tokens', [])
    
    # Detect season
    season = None
    if any(s in text for s in ['kharif', 'monsoon', 'rainy', 'june', 'july']):
        season = 'Kharif'
    elif any(s in text for s in ['rabi', 'winter', 'november', 'december', 'january']):
        season = 'Rabi'
    elif any(s in text for s in ['summer', 'march', 'april', 'may', 'hot']):
        season = 'Summer'
    
    # Detect water availability
    water = None
    if any(w in text for w in ['irrigated', 'canal', 'bore well', 'drip', 'water available']):
        water = 'irrigated'
    elif any(w in text for w in ['rainfed', 'rain fed', 'dry land', 'dryland', 'no irrigation', 'no water']):
        water = 'rainfed'
    
    # Detect soil
    soil = None
    if any(s in text for s in ['red soil', 'red sandy', 'sandy loam']):
        soil = 'red_sandy_loam'
    elif any(s in text for s in ['clay', 'black soil', 'black cotton']):
        soil = 'clay_loam'
    elif 'laterite' in text:
        soil = 'laterite'
    
    # Detect taluk
    taluk = None
    taluks = ['mandya', 'maddur', 'malavalli', 'pandavapura', 'srirangapatna', 'nagamangala', 'k.r. pet', 'kr pet']
    for t in taluks:
        if t in text:
            taluk = t.title().replace('K.r.', 'K.R.').replace('Kr', 'K.R.')
            break
    
    return {
        'season': season,
        'water': water,
        'soil': soil,
        'taluk': taluk
    }
