================================================================================
                    AGRIVISION — MANDYA DISTRICT OFFLINE
                   AGRICULTURAL ADVISORY MOBILE APPLICATION
================================================================================

DESCRIPTION
-----------
AgriVision is a self-contained, on-device decision engine mobile app that 
understands farmer queries and provides comprehensive agricultural advice 
without internet connectivity. It uses locally stored Mandya district-specific 
data and intelligent matching logic to serve as a complete agricultural 
advisory system for farmers.

The system covers:
  - 20+ crops grown in Mandya district
  - 50+ crop diseases with symptoms and treatments
  - 30+ pest management solutions
  - Fertilizer schedules and dosage calculations
  - Irrigation management (KRS Dam, canal, drip, sprinkler)
  - Government schemes (PM-KISAN, PMFBY, Krishi Bhagya, etc.)
  - Organic farming practices (Jeevamrutha, Panchagavya, etc.)
  - Season-wise crop recommendations
  - Soil management for red sandy loam soils
  - Market information and MSP prices

ARCHITECTURE
------------
The system has two layers:

1. PYTHON BACKEND (Build-Time Intelligence)
   - Heavy NLP processing (TF-IDF vectorization, text preprocessing)
   - Knowledge base management and database seeding
   - Flask development API for testing before mobile integration
   - Pre-computes all data that gets bundled into the mobile app

2. REACT NATIVE MOBILE APP (Runtime - Expo)
   - Cross-platform mobile app (Android + iOS)
   - On-device SQLite database with FTS5 full-text search
   - JavaScript-based NLP for runtime query matching
   - Fuse.js fuzzy matching for typo tolerance
   - Rule-based decision engine for crop recommendations
   - Premium chat interface with dark agricultural theme
   - 100% offline — no internet required after installation

TECH STACK
----------
  Backend:   Python 3.9+, Flask, scikit-learn, NLTK, RapidFuzz, SQLite
  Mobile:    React Native (Expo), expo-sqlite, Fuse.js, React Navigation
  Database:  SQLite with FTS5 virtual tables
  Data:      JSON knowledge base (500+ entries)

PROJECT STRUCTURE
-----------------
  Agri vision/
  ├── README.txt              <- This file
  ├── requirements.txt        <- Python dependencies
  ├── checklist.md            <- Pre-development checklist
  ├── backend/                <- Python backend
  │   ├── app.py              <- Flask API server
  │   ├── config.py           <- Configuration
  │   ├── data/               <- Knowledge base JSON files
  │   ├── db/                 <- Database seeder and SQLite DB
  │   ├── nlp/                <- NLP processing pipeline
  │   ├── engine/             <- Decision engine and response generator
  │   └── models/             <- Pre-computed TF-IDF models
  └── mobile/                 <- React Native (Expo) app
      ├── App.jsx             <- Root component
      ├── assets/db/          <- Bundled SQLite database
      └── src/                <- App source code

SETUP INSTRUCTIONS
==================

STEP 1: Python Backend Setup
-----------------------------
  # Create and activate virtual environment
  cd "Agri vision"
  python3 -m venv venv
  source venv/bin/activate        # Linux/Mac
  # venv\Scripts\activate         # Windows

  # Install dependencies
  pip install -r requirements.txt

  # Download NLTK data
  python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"

STEP 2: Seed the Knowledge Base
---------------------------------
  # Make sure virtual environment is activated
  source venv/bin/activate
  
  # Run the database seeder
  python3 backend/db/seed_database.py

  # This creates: backend/db/mandya_agri.db

STEP 3: Test Backend API (Optional)
-------------------------------------
  # Start Flask development server
  python3 backend/app.py

  # Test with curl:
  curl -X POST http://localhost:5000/api/query \
    -H "Content-Type: application/json" \
    -d '{"query": "my paddy leaves have brown spots"}'

  # API runs on http://localhost:5000

STEP 4: Mobile App Setup
--------------------------
  # Navigate to mobile directory
  cd mobile

  # Install Node.js dependencies
  npm install

  # Copy database to app assets
  cp ../backend/db/mandya_agri.db assets/db/

  # Start Expo development server
  

  # Scan QR code with Expo Go app on your phone
  # Or press 'a' to open in Android emulator

STEP 5: Build APK (Android)
-----------------------------
  cd mobile
  npx eas build -p android --profile preview

  # This generates an APK file you can install directly

API ENDPOINTS (Development Server)
====================================
  POST /api/query          - Process farmer query
  GET  /api/crops          - List all crops
  GET  /api/crops/<name>   - Get crop details
  GET  /api/diseases/<crop> - Get crop diseases
  GET  /api/schemes        - List government schemes
  POST /api/recommend      - Get crop recommendations
  GET  /api/health         - Health check
  GET  /api/categories     - Query categories
  GET  /api/suggestions    - Suggested queries

SAMPLE QUERIES
===============
  - "My paddy leaves are turning yellow with brown spots"
  - "What crop should I grow in Kharif season?"
  - "How much urea for sugarcane per acre?"
  - "Tell me about PM-KISAN scheme"
  - "My coconut tree has red palm weevil attack"
  - "Best organic fertilizer for ragi"
  - "When to sow paddy in Mandya?"
  - "How to do drip irrigation for sugarcane?"
  - "What is the MSP for paddy this year?"
  - "My sugarcane has red rot disease"

AUTHOR
------
  AgriVision Project — Mandya District Agricultural Advisory System

================================================================================
