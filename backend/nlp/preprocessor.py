"""Text preprocessing for agricultural queries."""
import re
import json
import os
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Agricultural domain stopwords - we KEEP domain-critical words
GENERAL_STOPWORDS = {'a','an','the','is','are','was','were','be','been','being','have','has','had',
    'do','does','did','will','would','shall','should','may','might','can','could',
    'i','me','my','we','our','you','your','he','she','it','they','them','their',
    'this','that','these','those','am','not','no','but','or','and','if','then',
    'so','very','just','also','too','some','any','all','each','every','both',
    'few','more','most','other','such','only','own','same','than','about',
    'up','out','on','off','over','under','again','further','once','here','there',
    'when','where','why','how','what','which','who','whom','with','from','into',
    'through','during','before','after','above','below','to','of','at','by','for',
    'in','as','between','because','until','while','get','got','getting','please',
    'tell','give','want','need','help','sir','madam','hello','hi','thank','thanks'}

# Words we must NEVER remove (domain-critical)
KEEP_WORDS = {'water','soil','leaf','leaves','root','stem','seed','fruit','flower',
    'rain','sun','wind','dry','wet','yellow','brown','black','white','red','green',
    'crop','plant','tree','field','farm','acre','hectare','kg','gram','ml','liter',
    'spray','apply','dose','mix','per','organic','chemical','natural','disease',
    'pest','insect','fungus','wilt','rot','blight','blast','spot','curl',
    'fertilizer','urea','dap','mop','npk','manure','compost',
    'paddy','rice','sugarcane','ragi','coconut','maize','banana','tomato',
    'drip','canal','bore','irrigation','pump','sprinkler'}

stemmer = PorterStemmer()
_synonyms_cache = None

def _load_synonyms():
    global _synonyms_cache
    if _synonyms_cache is not None:
        return _synonyms_cache
    syn_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "synonyms.json")
    try:
        with open(syn_path) as f:
            _synonyms_cache = json.load(f)
    except FileNotFoundError:
        _synonyms_cache = {}
    return _synonyms_cache

def _build_reverse_synonym_map():
    """Build reverse lookup: any synonym -> canonical term."""
    synonyms = _load_synonyms()
    reverse = {}
    for category in synonyms.values():
        for canonical, syns in category.items():
            for s in syns:
                reverse[s.lower()] = canonical.lower()
            reverse[canonical.lower()] = canonical.lower()
    return reverse

_reverse_map = None
def _get_reverse_map():
    global _reverse_map
    if _reverse_map is None:
        _reverse_map = _build_reverse_synonym_map()
    return _reverse_map

def clean_text(text):
    """Basic text cleaning."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s\-/]', ' ', text)  # Keep hyphens and slashes
    text = re.sub(r'\s+', ' ', text)
    return text

def tokenize(text):
    """Tokenize with domain awareness."""
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    return tokens

def remove_stopwords(tokens):
    """Remove general stopwords but keep domain-critical words."""
    return [t for t in tokens if t in KEEP_WORDS or t not in GENERAL_STOPWORDS]

def expand_synonyms(tokens):
    """Expand tokens by adding canonical forms of synonyms."""
    rev_map = _get_reverse_map()
    expanded = list(tokens)
    for t in tokens:
        if t in rev_map and rev_map[t] != t:
            expanded.append(rev_map[t])
    return list(set(expanded))

def stem_tokens(tokens):
    """Stem tokens for matching."""
    return [stemmer.stem(t) for t in tokens]

def extract_ngrams(tokens, n=2):
    """Extract n-grams for compound terms."""
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngrams.append(' '.join(tokens[i:i+n]))
    return ngrams

def preprocess(text, expand=True, stem=False):
    """Full preprocessing pipeline.
    Returns dict with: cleaned text, tokens, expanded tokens, ngrams, stemmed tokens.
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    filtered = remove_stopwords(tokens)
    
    result = {
        'original': text,
        'cleaned': cleaned,
        'tokens': filtered,
    }
    
    if expand:
        expanded = expand_synonyms(filtered)
        result['expanded_tokens'] = expanded
    else:
        result['expanded_tokens'] = filtered
    
    result['bigrams'] = extract_ngrams(filtered, 2)
    result['trigrams'] = extract_ngrams(filtered, 3)
    
    if stem:
        result['stemmed'] = stem_tokens(filtered)
    
    # Rejoin for search
    result['search_text'] = ' '.join(result['expanded_tokens'])
    
    return result

def extract_crop_mentions(text):
    """Extract any crop names mentioned in text."""
    rev_map = _get_reverse_map()
    text_lower = text.lower()
    crops_found = set()
    
    crop_names = ['paddy','rice','sugarcane','ragi','coconut','maize','corn','jowar','sorghum',
                  'banana','tomato','mulberry','turmeric','groundnut','cowpea','green gram',
                  'black gram','horse gram','tur dal','mango','brinjal','chili','bhendi']
    
    for crop in crop_names:
        if crop in text_lower:
            canonical = rev_map.get(crop, crop)
            crops_found.add(canonical)
    
    return list(crops_found)

if __name__ == "__main__":
    test_queries = [
        "My paddy leaves are turning yellow with brown spots",
        "How much urea for sugarcane per acre?",
        "What crop should I grow in Kharif season?",
        "kabbu has red color inside the cane",
        "Tell me about PM-KISAN scheme",
    ]
    for q in test_queries:
        result = preprocess(q)
        crops = extract_crop_mentions(q)
        print(f"\nQuery: {q}")
        print(f"  Tokens: {result['tokens']}")
        print(f"  Expanded: {result['expanded_tokens']}")
        print(f"  Crops: {crops}")
        print(f"  Search: {result['search_text']}")
