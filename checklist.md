# AgriVision — Pre-Development Checklist

## ✅ Pre-Requisites Verification

### System Requirements
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm 9+ installed (`npm --version`)
- [ ] Git installed (`git --version`)
- [ ] Expo CLI available (`npx expo --version`)
- [ ] Android Studio / Expo Go app on phone for testing

### Project Setup
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] NLTK data downloaded (stopwords, punkt tokenizer)
- [ ] Expo project initialized in `mobile/` directory
- [ ] Node modules installed in `mobile/` (`npm install`)

### Knowledge Base Preparation
- [ ] `mandya_knowledge_base.json` — 500+ entries covering all categories
- [ ] `synonyms.json` — 200+ agricultural synonym pairs
- [ ] `intent_patterns.json` — Intent classification patterns
- [ ] `crop_recommendations.json` — Decision engine rules
- [ ] All data validated for correctness and completeness

### Database
- [ ] SQLite database created with FTS5 tables
- [ ] All knowledge base entries seeded into database
- [ ] FTS5 search indices verified
- [ ] Database file copied to `mobile/assets/db/`

### Backend Verification
- [ ] Flask server starts without errors
- [ ] All API endpoints respond correctly
- [ ] Query processing returns relevant results
- [ ] Edge cases handled (empty query, unknown topic, misspellings)

### Mobile App Verification
- [ ] Expo dev server starts (`npx expo start`)
- [ ] App loads on Expo Go / Android emulator
- [ ] SQLite database loads correctly on device
- [ ] Chat interface sends and receives messages
- [ ] All 5 screens navigate properly
- [ ] Offline mode works (airplane mode test)
- [ ] Suggested queries return correct responses

### Final Quality
- [ ] 20+ test queries produce accurate, helpful responses
- [ ] UI looks premium (dark theme, animations, proper spacing)
- [ ] No console errors or warnings
- [ ] README.txt is complete and accurate
- [ ] All files properly organized per project structure
