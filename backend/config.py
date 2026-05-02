"""AgriVision Configuration"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "db")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DB_PATH = os.path.join(DB_DIR, "mandya_agri.db")
TFIDF_VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
TFIDF_MATRIX_PATH = os.path.join(MODELS_DIR, "tfidf_matrix.pkl")
KNOWLEDGE_BASE_PATH = os.path.join(DATA_DIR, "mandya_knowledge_base.json")
SYNONYMS_PATH = os.path.join(DATA_DIR, "synonyms.json")
INTENT_PATTERNS_PATH = os.path.join(DATA_DIR, "intent_patterns.json")
CROP_RECOMMENDATIONS_PATH = os.path.join(DATA_DIR, "crop_recommendations.json")

# NLP Settings
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 3)
FUZZY_THRESHOLD = 60
CONFIDENCE_THRESHOLD = 0.25
MAX_RESULTS = 5
