"""Query type detection with confidence scoring."""
import json
import os
import re

_patterns_cache = None

def _load_patterns():
    global _patterns_cache
    if _patterns_cache is not None:
        return _patterns_cache
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "intent_patterns.json")
    try:
        with open(path) as f:
            _patterns_cache = json.load(f)
    except FileNotFoundError:
        _patterns_cache = {}
    return _patterns_cache

def classify_query(preprocessed):
    """Classify query into intent categories with confidence scores.
    
    Args:
        preprocessed: dict from preprocessor.preprocess()
    
    Returns:
        dict with 'primary_intent', 'confidence', 'all_scores', 'sub_intents'
    """
    patterns = _load_patterns()
    tokens = set(preprocessed.get('expanded_tokens', preprocessed.get('tokens', [])))
    text = preprocessed.get('cleaned', '')
    
    scores = {}
    
    for intent, data in patterns.items():
        score = 0.0
        keywords = set(data.get('keywords', []))
        regex_patterns = data.get('patterns', [])
        
        # Keyword matching (each match = 1 point)
        keyword_matches = tokens.intersection(keywords)
        score += len(keyword_matches) * 1.0
        
        # Pattern matching (each match = 2 points - more specific)
        for pattern in regex_patterns:
            try:
                if re.search(pattern, text):
                    score += 2.0
            except re.error:
                continue
        
        # Normalize by total possible (keywords + patterns)
        max_possible = len(keywords) + len(regex_patterns) * 2
        if max_possible > 0:
            normalized = score / max_possible
        else:
            normalized = 0.0
        
        scores[intent] = {
            'raw_score': score,
            'normalized': round(normalized, 3),
            'keyword_matches': list(keyword_matches)
        }
    
    # Determine primary intent
    if scores:
        primary = max(scores, key=lambda k: scores[k]['raw_score'])
        confidence = scores[primary]['raw_score']
    else:
        primary = 'general'
        confidence = 0.0
    
    # Get secondary intents (score > 0)
    sub_intents = [k for k, v in sorted(scores.items(), key=lambda x: -x[1]['raw_score']) 
                   if v['raw_score'] > 0 and k != primary]
    
    # Determine query type category
    if primary in ('disease',):
        query_type = 'problem'
    elif primary in ('recommendation',):
        query_type = 'recommendation'
    elif primary in ('scheme', 'market'):
        query_type = 'information'
    else:
        query_type = 'problem' if confidence > 2 else 'information'
    
    return {
        'primary_intent': primary,
        'query_type': query_type,
        'confidence': confidence,
        'all_scores': scores,
        'sub_intents': sub_intents[:3]
    }

if __name__ == "__main__":
    from preprocessor import preprocess
    
    test_queries = [
        "My paddy leaves have brown spots and are dying",
        "What crop should I grow in Kharif season?",
        "How much urea for sugarcane?",
        "Tell me about PM-KISAN scheme",
        "How to make jeevamrutha?",
        "When to sow paddy in Mandya?",
        "Where to sell coconut?",
    ]
    
    for q in test_queries:
        pp = preprocess(q)
        result = classify_query(pp)
        print(f"\n'{q}'")
        print(f"  Type: {result['query_type']} | Intent: {result['primary_intent']} | Confidence: {result['confidence']}")
        if result['sub_intents']:
            print(f"  Sub-intents: {result['sub_intents']}")
