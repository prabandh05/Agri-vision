"""Format matched results into user-friendly responses."""
import json

def format_response(results, query_type, intent, preprocessed):
    """Generate structured response from search results.
    
    Args:
        results: list of matched results from matcher
        query_type: 'problem', 'recommendation', 'information'
        intent: primary intent string
        preprocessed: preprocessed query dict
    
    Returns:
        dict with formatted response
    """
    if not results:
        return _no_result_response(preprocessed)
    
    top = results[0]
    confidence = top.get('combined_score', 0)
    
    # Parse metadata if available
    metadata = {}
    if top.get('metadata'):
        try:
            metadata = json.loads(top['metadata']) if isinstance(top['metadata'], str) else top['metadata']
        except (json.JSONDecodeError, TypeError):
            metadata = {}
    
    response = {
        'title': top.get('title', 'Agricultural Advisory'),
        'content': top.get('content', ''),
        'category': top.get('category', intent),
        'confidence': round(confidence, 2),
        'query_type': query_type,
        'metadata': metadata,
        'related': [],
        'follow_up_questions': []
    }
    
    # Format based on category
    category = top.get('category', '')
    
    if category == 'disease':
        response = _format_disease_response(response, metadata)
    elif category == 'crop':
        response = _format_crop_response(response, metadata)
    elif category == 'scheme':
        response = _format_scheme_response(response, metadata)
    elif category == 'fertilizer':
        response = _format_fertilizer_response(response, metadata)
    elif category == 'irrigation':
        response = _format_irrigation_response(response, metadata)
    elif category == 'organic':
        response = _format_organic_response(response, metadata)
    elif category == 'faq':
        response['content_formatted'] = response['content']
    
    # Add related results
    for r in results[1:4]:
        response['related'].append({
            'title': r.get('title', ''),
            'category': r.get('category', ''),
            'score': r.get('combined_score', 0)
        })
    
    return response

def format_recommendation_response(recommendation):
    """Format crop recommendation response."""
    rec = recommendation
    crops = rec.get('recommended_crops', [])
    params = rec.get('parameters', {})
    taluk_info = rec.get('taluk_info')
    
    # Build header
    parts = []
    if params.get('season'):
        parts.append(f"**Season:** {params['season']}")
    if params.get('water'):
        parts.append(f"**Water:** {params['water'].title()}")
    if params.get('soil'):
        parts.append(f"**Soil:** {params['soil'].replace('_', ' ').title()}")
    if params.get('taluk'):
        parts.append(f"**Taluk:** {params['taluk']}")
    
    header = " | ".join(parts) if parts else "General recommendation for Mandya district"
    
    # Build crop list
    crop_list = "\n".join([f"  {i+1}. **{c}**" for i, c in enumerate(crops)])
    
    # Build details
    details = []
    for match in rec.get('detailed_matches', [])[:3]:
        detail = f"**{match['season']} ({match['water']}):** {', '.join(match['crops'])}"
        if match.get('notes'):
            detail += f"\n  _{match['notes']}_"
        details.append(detail)
    
    content = f"## 🌾 Crop Recommendations for Mandya\n\n{header}\n\n### Recommended Crops:\n{crop_list}\n"
    
    if details:
        content += "\n### Details:\n" + "\n\n".join(details)
    
    if taluk_info:
        content += f"\n\n### {params.get('taluk', 'Taluk')} Specific:\n"
        content += f"**Best crops:** {', '.join(taluk_info.get('best_crops', []))}\n"
        content += f"**Irrigation:** {taluk_info.get('irrigation', 'N/A')}\n"
        content += f"_{taluk_info.get('notes', '')}_"
    
    return {
        'title': 'Crop Recommendations',
        'content': content,
        'content_formatted': content,
        'category': 'recommendation',
        'confidence': 0.9,
        'query_type': 'recommendation',
        'metadata': rec,
        'related': [],
        'follow_up_questions': [
            "What fertilizer schedule for these crops?",
            "What diseases affect these crops?",
            "Tell me about irrigation for these crops"
        ]
    }

def _format_disease_response(response, metadata):
    """Format disease/pest response with management steps."""
    parts = [f"## 🔴 {response['title']}\n"]
    
    if metadata.get('symptoms'):
        parts.append(f"### Symptoms:\n{metadata['symptoms']}\n")
    
    mgmt = metadata.get('management', {})
    if mgmt:
        parts.append("### Management:\n")
        if mgmt.get('cultural'):
            parts.append(f"**🌿 Cultural:** {mgmt['cultural']}\n")
        if mgmt.get('chemical'):
            parts.append(f"**💊 Chemical:** {mgmt['chemical']}\n")
        if mgmt.get('biological'):
            parts.append(f"**🦠 Biological:** {mgmt['biological']}\n")
    
    if metadata.get('favorable_conditions'):
        parts.append(f"\n**⚠️ Favorable conditions:** {metadata['favorable_conditions']}")
    
    if metadata.get('severity'):
        parts.append(f"\n**Severity:** {metadata['severity'].upper()}")
    
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = [
        f"What other diseases affect {metadata.get('crop', 'this crop')}?",
        "What organic treatment can I use?",
        "How to prevent this disease?"
    ]
    return response

def _format_crop_response(response, metadata):
    parts = [f"## 🌾 {response['title']}\n"]
    
    for key, label in [('season', '📅 Season'), ('duration_days', '⏱️ Duration'), 
                        ('recommended_varieties', '🌱 Varieties'), ('yield_quintals_per_acre', '📊 Yield'),
                        ('msp_per_quintal', '💰 MSP'), ('water_requirement', '💧 Water'),
                        ('suitable_taluks', '📍 Suitable Taluks')]:
        if metadata.get(key):
            val = metadata[key]
            if isinstance(val, list):
                val = ', '.join(val)
            elif isinstance(val, dict):
                val = ', '.join([f"{k}: {v}" for k, v in val.items()])
            parts.append(f"**{label}:** {val}")
    
    if metadata.get('cultivation_practices'):
        parts.append("\n### Cultivation Practices:")
        for p in metadata['cultivation_practices']:
            parts.append(f"  • {p}")
    
    if metadata.get('fertilizer_schedule'):
        parts.append("\n### Fertilizer Schedule:")
        for k, v in metadata['fertilizer_schedule'].items():
            parts.append(f"  • **{k.replace('_', ' ').title()}:** {v}")
    
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = [
        f"What diseases affect {response['title']}?",
        f"Fertilizer schedule for {response['title']}?",
        f"Best variety of {response['title']} for Mandya?"
    ]
    return response

def _format_scheme_response(response, metadata):
    parts = [f"## 🏛️ {metadata.get('full_name', response['title'])}\n"]
    for key, label in [('benefit', '💰 Benefit'), ('eligibility', '✅ Eligibility'),
                        ('premium', '📋 Premium'), ('how_to_apply', '📝 How to Apply'),
                        ('documents', '📄 Documents Required')]:
        if metadata.get(key):
            parts.append(f"**{label}:** {metadata[key]}\n")
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = ["What other schemes are available?", "How to get crop insurance?"]
    return response

def _format_fertilizer_response(response, metadata):
    parts = [f"## 🧪 {response['title']}\n"]
    for key in ['content', 'usage', 'rate_general', 'price', 'precautions']:
        if metadata.get(key):
            parts.append(f"**{key.replace('_', ' ').title()}:** {metadata[key]}")
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = ["Organic alternative?", "Fertilizer schedule for my crop?"]
    return response

def _format_irrigation_response(response, metadata):
    parts = [f"## 💧 {response['title']}\n"]
    if metadata.get('description'):
        parts.append(metadata['description'])
    for key in ['suitable_crops', 'benefits', 'cost', 'schedule']:
        if metadata.get(key):
            parts.append(f"\n**{key.replace('_', ' ').title()}:** {metadata[key]}")
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = ["How to get drip irrigation subsidy?", "Water saving methods?"]
    return response

def _format_organic_response(response, metadata):
    parts = [f"## 🌿 {response['title']}\n"]
    for key in ['preparation', 'application', 'benefits', 'cost']:
        if metadata.get(key):
            parts.append(f"**{key.title()}:** {metadata[key]}\n")
    response['content_formatted'] = "\n".join(parts)
    response['follow_up_questions'] = ["Other organic methods?", "Organic certification process?"]
    return response

def _no_result_response(preprocessed):
    query = preprocessed.get('original', 'your query')
    return {
        'title': 'No Specific Match Found',
        'content': f"I couldn't find a specific answer for: \"{query}\"\n\nPlease try:\n• Being more specific about the crop and problem\n• Using simpler terms\n• Asking about a specific crop, disease, fertilizer, or scheme\n\nYou can also browse crops, diseases, and schemes from the menu.",
        'content_formatted': f"I couldn't find a specific answer for: \"{query}\"\n\nPlease try:\n• Being more specific about the crop and problem\n• Using simpler terms\n• Asking about a specific crop, disease, fertilizer, or scheme\n\nYou can also browse crops, diseases, and schemes from the menu.",
        'category': 'no_match',
        'confidence': 0,
        'query_type': 'unknown',
        'metadata': {},
        'related': [],
        'follow_up_questions': [
            "What crops grow in Mandya?",
            "Tell me about paddy diseases",
            "What government schemes are available?",
            "How to do organic farming?"
        ]
    }
