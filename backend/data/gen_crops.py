#!/usr/bin/env python3
"""Generate crops section of knowledge base."""

def get_crops():
    return [
        {
            "id": "crop_paddy",
            "name": "Paddy (Rice)",
            "local_name": "Bhatta / Akki",
            "category": "cereal",
            "type": "irrigated",
            "season": ["Kharif", "Rabi"],
            "sowing_months": {"Kharif": "June-July", "Rabi": "November-December"},
            "harvest_months": {"Kharif": "October-November", "Rabi": "March-April"},
            "duration_days": "120-150",
            "water_requirement": "high",
            "soil_type": "Clay loam, red sandy loam with good water retention",
            "suitable_taluks": ["Mandya", "Maddur", "Malavalli", "Srirangapatna", "Pandavapura"],
            "irrigation_source": "KRS Canal, Hemavathy Canal",
            "seed_rate_kg_per_acre": "30-40 (transplanting), 80-100 (direct seeding)",
            "recommended_varieties": ["MTU-1010", "Jaya", "IR-64", "KRH-4 (Hybrid)", "Tanu", "Intan"],
            "yield_quintals_per_acre": "20-25",
            "msp_per_quintal": "₹2,300 (Common), ₹2,320 (Grade A)",
            "cultivation_practices": [
                "Nursery: Prepare raised nursery bed 1m wide. Soak seeds for 24hrs, incubate 48hrs. Sow pre-germinated seeds.",
                "Main field: Puddle field 2-3 times. Level field properly for uniform water distribution.",
                "Transplanting: Transplant 20-25 day old seedlings, 2-3 seedlings per hill at 20x15cm spacing.",
                "Water management: Maintain 2-5cm water during vegetative stage. Drain 10 days before harvest.",
                "Weed management: Apply Pretilachlor 500ml/acre within 3 days of transplanting. Hand weed at 25 and 45 days."
            ],
            "fertilizer_schedule": {
                "basal": "DAP 50kg/acre + MOP 25kg/acre at transplanting",
                "first_top_dress": "Urea 25kg/acre at 21 days after transplanting (tillering)",
                "second_top_dress": "Urea 25kg/acre at 42 days (panicle initiation)",
                "micronutrients": "Zinc Sulphate 10kg/acre as basal in zinc-deficient soils"
            },
            "common_diseases": ["blast", "brown_leaf_spot", "sheath_blight", "bacterial_leaf_blight", "sheath_rot"],
            "common_pests": ["stem_borer", "leaf_folder", "brown_plant_hopper", "gall_midge"],
            "intercropping": "Not common for paddy; can grow green gram/black gram after harvest as relay crop",
            "organic_practices": "Apply FYM 4 tonnes/acre. Use neem cake 100kg/acre. Jeevamrutha 200L/acre monthly."
        },
        {
            "id": "crop_sugarcane",
            "name": "Sugarcane",
            "local_name": "Kabbu",
            "category": "commercial",
            "type": "irrigated",
            "season": ["Year-round (perennial)"],
            "sowing_months": {"Plant crop": "January-March", "Ratoon": "After harvest"},
            "harvest_months": {"Plant crop": "December-March (12 months)", "Ratoon": "11-12 months after ratooning"},
            "duration_days": "330-365",
            "water_requirement": "very high",
            "soil_type": "Deep red sandy loam, well-drained fertile soils",
            "suitable_taluks": ["Mandya", "Maddur", "Srirangapatna", "Pandavapura"],
            "irrigation_source": "KRS Canal, bore wells",
            "seed_rate_kg_per_acre": "25,000-30,000 three-bud setts",
            "recommended_varieties": ["Co-86032", "Co-62175", "CoC-671", "Co-0238", "SNK-44"],
            "yield_quintals_per_acre": "400-500 (plant crop), 300-400 (ratoon)",
            "msp_per_quintal": "₹315 (FRP - Fair & Remunerative Price)",
            "cultivation_practices": [
                "Land preparation: Deep plough 2-3 times. Form furrows 90cm apart, 20cm deep.",
                "Planting: Place 3-bud setts end-to-end in furrows. Treat setts with Carbendazim 1g/L for 15 min.",
                "Earthing up: First at 45 days, second at 90 days, third at 120 days.",
                "Detrashing: Remove dry leaves at 5th and 7th month to prevent pest harboring.",
                "Propping: Support tall canes with bamboo at 8-9 months to prevent lodging."
            ],
            "fertilizer_schedule": {
                "basal": "DAP 75kg/acre + MOP 40kg/acre + FYM 8 tonnes/acre",
                "first_top_dress": "Urea 50kg/acre at 45 days (with first earthing up)",
                "second_top_dress": "Urea 50kg/acre at 90 days (with second earthing up)",
                "third_top_dress": "Urea 35kg/acre at 120 days (with third earthing up)",
                "micronutrients": "Ferrous Sulphate 10kg/acre for iron deficiency"
            },
            "common_diseases": ["red_rot", "smut", "wilt", "grassy_shoot", "rust"],
            "common_pests": ["early_shoot_borer", "internode_borer", "top_borer", "white_grub", "mealybug"],
            "intercropping": "Short-duration pulses (green gram, cowpea) or vegetables between rows in first 3 months",
            "organic_practices": "Apply press mud 4 tonnes/acre. Use bio-fertilizers Azotobacter + PSB. Trash mulching."
        },
        {
            "id": "crop_ragi",
            "name": "Ragi (Finger Millet)",
            "local_name": "Ragi",
            "category": "millet",
            "type": "rainfed/irrigated",
            "season": ["Kharif"],
            "sowing_months": {"Kharif": "May-July"},
            "harvest_months": {"Kharif": "September-November"},
            "duration_days": "100-130",
            "water_requirement": "low-medium",
            "soil_type": "Red sandy loam, laterite soils, well-drained",
            "suitable_taluks": ["Nagamangala", "K.R. Pet", "Malavalli", "Pandavapura"],
            "irrigation_source": "Rainfed, supplemental irrigation from bore wells",
            "seed_rate_kg_per_acre": "4-5 (transplanting), 8-10 (direct seeding)",
            "recommended_varieties": ["GPU-28", "GPU-67", "MR-6", "GPU-45", "ML-365"],
            "yield_quintals_per_acre": "12-18 (irrigated), 6-10 (rainfed)",
            "msp_per_quintal": "₹4,290",
            "cultivation_practices": [
                "Nursery: Prepare 1m wide beds. Sow seeds mixed with fine sand. Water daily. Seedlings ready in 18-22 days.",
                "Main field: Plough 2-3 times. Apply FYM before last ploughing.",
                "Transplanting: 18-22 day seedlings at 22.5x10cm spacing (SRI: 25x25cm, single seedling).",
                "Direct seeding: Line sowing at 25cm row spacing. Thin to 10cm between plants at 15 days.",
                "Weed management: Hand weed twice at 20 and 40 days. Intercultivation with blade harrow."
            ],
            "fertilizer_schedule": {
                "basal": "DAP 30kg/acre + MOP 20kg/acre",
                "top_dress": "Urea 20kg/acre at 30 days after transplanting",
                "micronutrients": "Zinc Sulphate 5kg/acre in deficient soils"
            },
            "common_diseases": ["finger_blast", "neck_blast", "foot_rot", "leaf_spot"],
            "common_pests": ["stem_borer", "army_worm", "aphids", "grasshopper"],
            "intercropping": "Ragi + Tur dal (8:2 ratio), Ragi + Field bean, Ragi + Niger",
            "organic_practices": "Ideal for organic farming. Apply FYM 3 tonnes/acre. Jeevamrutha 200L/acre. Seed treatment with Beejamrutha."
        },
        {
            "id": "crop_coconut",
            "name": "Coconut",
            "local_name": "Tenginakaayi",
            "category": "plantation",
            "type": "irrigated/rainfed",
            "season": ["Perennial"],
            "sowing_months": {"Planting": "June-July (onset of monsoon)"},
            "harvest_months": {"Harvest": "Throughout year, every 45-60 days"},
            "duration_days": "First yield in 5-7 years, productive for 60+ years",
            "water_requirement": "medium-high",
            "soil_type": "Red sandy loam, laterite, well-drained",
            "suitable_taluks": ["Mandya", "Maddur", "Malavalli", "K.R. Pet", "Nagamangala", "Srirangapatna", "Pandavapura"],
            "irrigation_source": "Drip irrigation recommended, bore wells, canal",
            "seed_rate_kg_per_acre": "70 palms per acre (7.5m x 7.5m spacing)",
            "recommended_varieties": ["Tiptur Tall", "DxT Hybrid", "Gangabondam", "Chowghat Orange Dwarf"],
            "yield_quintals_per_acre": "80-120 nuts/palm/year (bearing palm)",
            "msp_per_quintal": "₹3,300/quintal copra",
            "cultivation_practices": [
                "Pit preparation: Dig 1m x 1m x 1m pits. Fill with topsoil + 20kg FYM + 1kg neem cake + 200g bone meal.",
                "Planting: Select 9-12 month old seedlings with 6+ leaves. Plant during monsoon.",
                "Basin management: Maintain 1.8m radius basin around palm. Mulch with coconut fronds/coir pith.",
                "Intercropping: Grow banana, turmeric, ginger, cowpea between palms in first 8 years.",
                "Harvest: Harvest every 45-60 days when nuts mature (11 months after flowering)."
            ],
            "fertilizer_schedule": {
                "year_1_to_3": "FYM 20kg + Urea 300g + SSP 500g + MOP 500g per palm per year",
                "bearing_palm": "FYM 25kg + Urea 1kg + SSP 1.5kg + MOP 2kg per palm per year",
                "application": "Apply in 2 split doses: May-June and September-October in circular trenches",
                "micronutrients": "Borax 50g + MgSO4 500g per palm per year"
            },
            "common_diseases": ["bud_rot", "stem_bleeding", "leaf_blight", "root_wilt"],
            "common_pests": ["red_palm_weevil", "rhinoceros_beetle", "eriophyid_mite", "black_headed_caterpillar"],
            "intercropping": "Banana, Turmeric, Ginger, Cowpea, Groundnut, Fodder grass between rows",
            "organic_practices": "Apply Jeevamrutha 5L/palm/month. Coir pith composting. Neem cake 2kg/palm. Green manuring with sun hemp."
        },
        {
            "id": "crop_maize",
            "name": "Maize (Corn)",
            "local_name": "Mekkejola",
            "category": "cereal",
            "type": "irrigated/rainfed",
            "season": ["Kharif", "Rabi"],
            "sowing_months": {"Kharif": "June-July", "Rabi": "October-November"},
            "harvest_months": {"Kharif": "September-October", "Rabi": "February-March"},
            "duration_days": "95-110",
            "water_requirement": "medium",
            "soil_type": "Red sandy loam, well-drained",
            "suitable_taluks": ["Nagamangala", "K.R. Pet", "Malavalli"],
            "irrigation_source": "Rainfed, supplemental irrigation",
            "seed_rate_kg_per_acre": "8-10 (hybrid)",
            "recommended_varieties": ["NK-6240", "900M Gold", "Pioneer 3502", "Kaveri 50", "Bio 9681"],
            "yield_quintals_per_acre": "25-35",
            "msp_per_quintal": "₹2,090",
            "cultivation_practices": [
                "Land preparation: Deep plough, 2 harrowings. Form ridges 60cm apart.",
                "Sowing: Dibble 1-2 seeds per hill at 20cm spacing on ridges. Thin to 1 plant/hill.",
                "Critical irrigation: At knee-high stage, tasseling, and grain filling.",
                "Weed management: Atrazine 800g/acre pre-emergence. Hand weed at 25 days."
            ],
            "fertilizer_schedule": {
                "basal": "DAP 50kg/acre + MOP 20kg/acre",
                "first_top_dress": "Urea 30kg/acre at knee-high (25-30 days)",
                "second_top_dress": "Urea 30kg/acre at tasseling (50-55 days)"
            },
            "common_diseases": ["turcicum_leaf_blight", "downy_mildew", "stalk_rot", "rust"],
            "common_pests": ["fall_army_worm", "stem_borer", "shoot_fly", "cob_borer"],
            "intercropping": "Maize + Red gram (4:1), Maize + Soybean",
            "organic_practices": "FYM 4 tonnes/acre. Trichogramma cards for stem borer. Neem-based sprays."
        },
        {
            "id": "crop_jowar",
            "name": "Jowar (Sorghum)",
            "local_name": "Jola",
            "category": "millet",
            "type": "rainfed",
            "season": ["Kharif", "Rabi"],
            "sowing_months": {"Kharif": "June-July", "Rabi": "September-October"},
            "harvest_months": {"Kharif": "October-November", "Rabi": "January-February"},
            "duration_days": "100-120",
            "water_requirement": "low",
            "soil_type": "Red sandy loam, medium black soil",
            "suitable_taluks": ["Nagamangala", "K.R. Pet"],
            "irrigation_source": "Rainfed",
            "seed_rate_kg_per_acre": "4-5",
            "recommended_varieties": ["CSV-20", "DSV-4", "M-35-1 (Rabi)", "CSH-16"],
            "yield_quintals_per_acre": "10-15",
            "msp_per_quintal": "₹3,371 (Hybrid), ₹3,421 (Maldandi)",
            "cultivation_practices": [
                "Land preparation: 2 ploughings + harrowing. Ridge and furrow for moisture conservation.",
                "Sowing: Line sow at 45cm x 15cm spacing. Seed treat with Thiram 3g/kg.",
                "Thinning: Thin to 1 plant/hill at 15 days.",
                "Harvest: Harvest when grains are hard and moisture below 14%."
            ],
            "fertilizer_schedule": {
                "basal": "DAP 25kg/acre + MOP 10kg/acre",
                "top_dress": "Urea 15kg/acre at 30 days"
            },
            "common_diseases": ["grain_mold", "charcoal_rot", "downy_mildew", "anthracnose"],
            "common_pests": ["shoot_fly", "stem_borer", "midge", "ear_head_worm"],
            "intercropping": "Jowar + Tur dal (4:2), Jowar + Groundnut",
            "organic_practices": "FYM 3 tonnes/acre. Low input crop suitable for organic."
        },
        {
            "id": "crop_banana",
            "name": "Banana",
            "local_name": "Bale Hannu",
            "category": "fruit",
            "type": "irrigated",
            "season": ["Year-round"],
            "sowing_months": {"Planting": "June-July or February-March"},
            "harvest_months": {"Harvest": "12-14 months after planting"},
            "duration_days": "365-420",
            "water_requirement": "high",
            "soil_type": "Deep, well-drained loamy soil, rich in organic matter",
            "suitable_taluks": ["Mandya", "Maddur", "Srirangapatna", "Malavalli"],
            "irrigation_source": "Canal, drip irrigation recommended",
            "seed_rate_kg_per_acre": "1000-1200 suckers or tissue culture plants",
            "recommended_varieties": ["Yelakki (Poovan)", "Robusta (Cavendish)", "Nendran", "Grand Naine", "Red Banana"],
            "yield_quintals_per_acre": "200-300 (depends on variety)",
            "msp_per_quintal": "Market price based",
            "cultivation_practices": [
                "Pit: 45x45x45cm pits at 1.8x1.8m spacing. Fill with topsoil + 10kg FYM + 250g neem cake.",
                "Planting: Use disease-free sword suckers or tissue culture plants.",
                "Desuckering: Remove all suckers except 1 follower at 4th month.",
                "Propping: Support bunch-bearing plants with bamboo props.",
                "Denaveling: Remove male bud 15 days after last hand opens."
            ],
            "fertilizer_schedule": {
                "per_plant": "200g N + 60g P2O5 + 300g K2O per plant per crop",
                "application": "Split into 4 doses at 2, 4, 6, and 8 months after planting",
                "micronutrients": "FeSO4 + ZnSO4 foliar spray at 3, 5, 7 months"
            },
            "common_diseases": ["panama_wilt", "sigatoka_leaf_spot", "bunchy_top", "anthracnose"],
            "common_pests": ["banana_weevil", "thrips", "aphids", "nematodes"],
            "intercropping": "Cowpea, beans, or vegetables between rows in first 3-4 months",
            "organic_practices": "Jeevamrutha 2L/plant/month. Pseudomonas 20g/plant for wilt. Neem cake 1kg/plant."
        },
        {
            "id": "crop_tomato",
            "name": "Tomato",
            "local_name": "Tomato Hannu",
            "category": "vegetable",
            "type": "irrigated",
            "season": ["Kharif", "Rabi", "Summer"],
            "sowing_months": {"Kharif": "June-July", "Rabi": "September-October", "Summer": "January-February"},
            "harvest_months": {"Kharif": "Sept-Nov", "Rabi": "Dec-Feb", "Summer": "April-May"},
            "duration_days": "90-120",
            "water_requirement": "medium",
            "soil_type": "Red sandy loam, well-drained",
            "suitable_taluks": ["Mandya", "Maddur", "Malavalli", "Srirangapatna"],
            "irrigation_source": "Drip, canal, bore well",
            "seed_rate_kg_per_acre": "150-200g (nursery + transplant)",
            "recommended_varieties": ["Arka Rakshak", "Arka Samrat", "TO-1057 (Hybrid)", "Abhinav"],
            "yield_quintals_per_acre": "120-200",
            "msp_per_quintal": "Market price (₹800-3000 varies)",
            "cultivation_practices": [
                "Nursery: Raise seedlings in pro-trays or raised beds. Ready in 25-30 days.",
                "Transplant: 30-day seedlings at 60x45cm spacing on raised beds/ridges.",
                "Staking: Stake plants with bamboo/wire for indeterminate varieties.",
                "Pruning: Remove suckers below first flower cluster for better yield."
            ],
            "fertilizer_schedule": {
                "basal": "FYM 8 tonnes/acre + DAP 50kg + MOP 30kg",
                "top_dress_1": "Urea 20kg at 30 days",
                "top_dress_2": "19:19:19 complex 5g/L foliar spray at flowering"
            },
            "common_diseases": ["early_blight", "late_blight", "bacterial_wilt", "tomato_leaf_curl_virus"],
            "common_pests": ["fruit_borer", "whitefly", "thrips", "leaf_miner"],
            "intercropping": "Marigold as trap crop for fruit borer",
            "organic_practices": "Trichoderma soil application. Pseudomonas for wilt. Neem oil 3ml/L for pests."
        },
        {
            "id": "crop_mulberry",
            "name": "Mulberry (for Sericulture)",
            "local_name": "Hippunerale",
            "category": "sericulture",
            "type": "irrigated",
            "season": ["Perennial"],
            "sowing_months": {"Planting": "June-August"},
            "harvest_months": {"Leaf harvest": "Every 65-70 days (5-6 harvests/year)"},
            "duration_days": "Perennial, productive for 15-20 years",
            "water_requirement": "medium-high",
            "soil_type": "Red sandy loam, deep fertile soils",
            "suitable_taluks": ["Mandya", "Maddur", "Malavalli", "K.R. Pet", "Srirangapatna"],
            "irrigation_source": "Canal, drip, bore well",
            "seed_rate_kg_per_acre": "6000-8000 saplings (paired row: 60cm+150cm x 60cm)",
            "recommended_varieties": ["V-1", "S-36", "S-54", "M-5"],
            "yield_quintals_per_acre": "60-80 tonnes leaf/acre/year",
            "msp_per_quintal": "Cocoon price: ₹350-600/kg",
            "cultivation_practices": [
                "Land prep: Deep plough. Prepare beds 60cm wide with 150cm path.",
                "Planting: Plant rooted saplings at 60x60cm in paired rows.",
                "Pruning: Bottom prune at 15cm from ground every 65-70 days.",
                "Harvest leaf at 65-70 days after pruning for silkworm rearing."
            ],
            "fertilizer_schedule": {
                "per_harvest": "Urea 25kg + SSP 15kg + MOP 10kg per acre after each harvest",
                "organic": "FYM 8 tonnes/acre/year"
            },
            "common_diseases": ["root_rot", "powdery_mildew", "leaf_rust", "tukra"],
            "common_pests": ["whitefly", "thrips", "mealybug", "leaf_roller"],
            "intercropping": "Not recommended for mulberry gardens",
            "organic_practices": "Vermicompost 2 tonnes/acre. Neem cake 200kg/acre. Bio-fertilizers."
        },
        {
            "id": "crop_turmeric",
            "name": "Turmeric",
            "local_name": "Arishina",
            "category": "spice",
            "type": "irrigated",
            "season": ["Kharif"],
            "sowing_months": {"Kharif": "June-July"},
            "harvest_months": {"Harvest": "January-March (8-9 months)"},
            "duration_days": "240-270",
            "water_requirement": "medium",
            "soil_type": "Red sandy loam, well-drained, rich organic",
            "suitable_taluks": ["Mandya", "Maddur", "K.R. Pet"],
            "irrigation_source": "Canal, drip",
            "seed_rate_kg_per_acre": "600-800 kg rhizome fingers",
            "recommended_varieties": ["Pratibha", "Salem", "Erode Local", "Rajendra Sonia"],
            "yield_quintals_per_acre": "80-100 (fresh), 16-20 (cured)",
            "msp_per_quintal": "Market price ₹8000-15000/quintal (cured)",
            "cultivation_practices": [
                "Land prep: Deep plough, form ridges/beds 1m wide.",
                "Planting: Plant mother/finger rhizomes 5cm deep at 30x20cm.",
                "Mulching: Apply green leaves/paddy straw mulch immediately after planting and at 45, 90 days.",
                "Earthing up: At 45 and 90 days after planting."
            ],
            "fertilizer_schedule": {
                "basal": "FYM 8 tonnes + neem cake 200kg + SSP 50kg/acre",
                "top_dress_1": "Urea 20kg + MOP 15kg at 60 days",
                "top_dress_2": "Urea 20kg + MOP 15kg at 120 days"
            },
            "common_diseases": ["rhizome_rot", "leaf_blotch", "leaf_spot"],
            "common_pests": ["shoot_borer", "leaf_roller", "scale_insect", "rhizome_fly"],
            "intercropping": "Excellent intercrop in coconut and areca nut gardens",
            "organic_practices": "Trichoderma seed treatment. Mulching critical. Jeevamrutha 200L/acre."
        }
    ]

if __name__ == "__main__":
    import json
    print(json.dumps(get_crops(), indent=2))
