#!/usr/bin/env python3
"""Generate schemes, fertilizers, irrigation, organic, and general FAQ data."""

def get_schemes():
    return [
        {"id":"pmkisan","name":"PM-KISAN","full_name":"Pradhan Mantri Kisan Samman Nidhi","type":"central",
         "benefit":"₹6,000/year in 3 instalments of ₹2,000","eligibility":"All land-holding farmer families",
         "how_to_apply":"Register at pmkisan.gov.in or Common Service Centre. Aadhaar, bank account, land records required. e-KYC mandatory.",
         "documents":"Aadhaar card, Bank passbook, Land ownership documents (RTC/Pahani)",
         "faq":[{"q":"How to apply for PM-KISAN","a":"Visit pmkisan.gov.in or nearest Common Service Centre. You need Aadhaar card, bank passbook, and land documents (RTC). Complete e-KYC for payment. ₹6,000/year in 3 instalments."},
                {"q":"PM-KISAN money not received","a":"Check status at pmkisan.gov.in with Aadhaar/mobile number. Common issues: e-KYC not done, Aadhaar-bank link missing, or land records not updated. Visit CSC or agriculture office."}]},
        {"id":"pmfby","name":"PMFBY","full_name":"Pradhan Mantri Fasal Bima Yojana","type":"central",
         "benefit":"Crop insurance against natural calamities, pests, diseases. Full sum insured coverage.",
         "eligibility":"All farmers growing notified crops. Voluntary for loanee and non-loanee farmers.",
         "premium":"Kharif: 2% of sum insured, Rabi: 1.5%, Commercial/Horticulture: 5%. Government pays remaining premium.",
         "how_to_apply":"Apply through bank, CSC, or PMFBY portal before sowing deadline. Report crop loss within 72 hours.",
         "faq":[{"q":"How to get crop insurance","a":"Apply for PMFBY through your bank, CSC, or pmfby.gov.in before the sowing deadline. Premium: 2% for Kharif, 1.5% for Rabi crops. Report any crop loss to insurance company/bank within 72 hours."},
                {"q":"Crop damaged by rain flood","a":"Report crop loss to your insurance company or bank within 72 hours. Take photos of damage. If enrolled in PMFBY, you'll get compensation based on crop cutting experiments. Contact agriculture office for assessment."}]},
        {"id":"krishi_bhagya","name":"Krishi Bhagya","full_name":"Krishi Bhagya Scheme","type":"state",
         "benefit":"Subsidy for farm ponds (80%), diesel pump sets (50%), sprinkler/drip sets (90% for SC/ST, 80% others)",
         "eligibility":"Farmers in rainfed areas of Karnataka",
         "how_to_apply":"Apply through Raitha Samparka Kendra or agriculture office. Online via Seva Sindhu portal.",
         "faq":[{"q":"How to get farm pond subsidy","a":"Apply for Krishi Bhagya scheme through your local Raitha Samparka Kendra. 80% subsidy on farm ponds, 50% on pump sets. For rainfed area farmers. Apply on Seva Sindhu portal or agriculture office."}]},
        {"id":"savayava_bhagya","name":"Savayava Bhagya","full_name":"Savayava Bhagya (Organic Farming)","type":"state",
         "benefit":"Up to 90% subsidy for organic farming units. Training, inputs, and certification support.",
         "eligibility":"Farmers willing to convert to organic farming in Karnataka",
         "how_to_apply":"Apply through agriculture department or Seva Sindhu portal.",
         "faq":[{"q":"Government help for organic farming","a":"Apply for Savayava Bhagya scheme - up to 90% subsidy for organic farming setup. Includes training, organic inputs, and certification support. Contact agriculture office or apply on Seva Sindhu portal."}]},
        {"id":"surya_raitha","name":"Surya Raitha","full_name":"Karnataka Surya Raitha Scheme","type":"state",
         "benefit":"Financial assistance for solar-powered pump sets for irrigation",
         "eligibility":"Farmers in Karnataka with agricultural land",
         "how_to_apply":"Apply through BESCOM/HESCOM or agriculture department.",
         "faq":[{"q":"Solar pump subsidy for farmers","a":"Apply for Surya Raitha scheme for solar pump set subsidy. Contact your local electricity supply company (HESCOM/BESCOM) or agriculture department for application."}]},
        {"id":"drip_subsidy","name":"Drip Irrigation Subsidy","full_name":"Micro Irrigation Scheme (PMKSY-MI)","type":"central",
         "benefit":"55% subsidy for small/marginal farmers, 45% for others on drip/sprinkler systems",
         "eligibility":"All farmers with minimum 0.5 acre land",
         "how_to_apply":"Apply through agriculture/horticulture department. Select empaneled company.",
         "faq":[{"q":"How to get drip irrigation subsidy","a":"Apply for PMKSY Micro Irrigation scheme. 55% subsidy for small farmers, 45% for others. Apply through horticulture/agriculture department. Minimum 0.5 acre land needed. Select from empaneled drip companies."}]}
    ]

def get_fertilizer_guide():
    return [
        {"id":"urea_guide","name":"Urea","type":"nitrogen","content":"46% N","appearance":"White prills/granules",
         "usage":"Top dressing for all crops. Apply in standing water for paddy. Split application recommended.",
         "rate_general":"50-100 kg/acre depending on crop","price":"₹267/45kg bag (subsidized)",
         "precautions":"Don't apply during heavy rain. Don't mix with alkaline fertilizers. Excess causes lodging and pest susceptibility.",
         "faq":[{"q":"How much urea for paddy per acre","a":"Total 50-75 kg Urea per acre for paddy in 2-3 splits: 25kg at 21 days (tillering), 25kg at 42 days (panicle initiation). Apply in 2-3cm standing water for better absorption. Avoid excess - causes blast disease susceptibility."},
                {"q":"How much urea for sugarcane","a":"Total 135kg Urea per acre for sugarcane in 3 splits: 50kg at 45 days, 50kg at 90 days, 35kg at 120 days. Apply with earthing up operations. Always combine with phosphorus and potassium."}]},
        {"id":"dap_guide","name":"DAP","type":"phosphorus","content":"18% N + 46% P2O5","appearance":"Dark brown/black granules",
         "usage":"Basal application at planting/transplanting. Promotes root development and early growth.",
         "rate_general":"50-75 kg/acre as basal","price":"₹1,350/50kg bag (subsidized)",
         "faq":[{"q":"When to apply DAP","a":"Apply DAP as basal dose at planting or transplanting time. Mix into soil during last ploughing or place in furrows before sowing. Don't top-dress with DAP. For paddy: 50kg/acre, Sugarcane: 75kg/acre."}]},
        {"id":"mop_guide","name":"MOP (Muriate of Potash)","type":"potassium","content":"60% K2O","appearance":"Red/pink crystals",
         "usage":"Basal and top dressing. Strengthens stems, improves grain filling, disease resistance.",
         "rate_general":"20-40 kg/acre","price":"₹850/50kg bag",
         "faq":[{"q":"Why is potash important","a":"Potash (MOP) strengthens stems (prevents lodging), improves grain filling and quality, increases disease resistance, and helps water use efficiency. Mandya soils are often low in potassium. Apply 20-40 kg MOP/acre as basal for most crops."}]},
        {"id":"zinc_sulphate","name":"Zinc Sulphate","type":"micronutrient","content":"21% Zn + 10% S",
         "usage":"Basal for paddy in zinc-deficient soils. Corrects zinc deficiency causing bronzing/browning of leaves.",
         "rate_general":"10 kg/acre","price":"₹50-60/kg",
         "faq":[{"q":"Paddy leaves turning brown bronze color","a":"This could be Zinc deficiency (Khaira disease). Apply Zinc Sulphate 10kg/acre to soil. For immediate relief, spray ZnSO4 5g + lime 2.5g per liter of water. Common in alkaline and waterlogged soils of Mandya."}]}
    ]

def get_irrigation_guide():
    return [
        {"id":"krs_canal","name":"KRS Canal Irrigation","type":"canal",
         "description":"Krishna Raja Sagara (KRS) dam on Cauvery river is primary irrigation source for Mandya district. Water released through Visvesvaraya Canal network covering Mandya, Maddur, Malavalli, Srirangapatna, Pandavapura taluks.",
         "schedule":"Kharif release: June-July to November. Rabi: January-April. Summer: Limited based on storage. On-off pattern of release.",
         "crops_supported":"Paddy, Sugarcane (main), Banana, Vegetables",
         "faq":[{"q":"When does canal water release start","a":"KRS canal water for Kharif is usually released in June-July depending on dam storage and monsoon. Rabi release starts January. Follow ICC (Irrigation Consultative Committee) announcements. Check with Cauvery Neeravari Nigam Limited (CNNL) for exact dates."},
                {"q":"Canal water not reaching my field","a":"Contact your local Water User Association or Cauvery Neeravari Nigam Limited (CNNL). File complaint at district irrigation office. Possible issues: channel blockage, unauthorized tapping upstream, or scheduled rotation. Tail-end farmers should coordinate with WUA for equitable distribution."}]},
        {"id":"drip_irrigation","name":"Drip Irrigation","type":"micro_irrigation",
         "description":"Most water-efficient method. Delivers water directly to root zone through emitters. Saves 40-60% water compared to flood irrigation.",
         "suitable_crops":"Sugarcane, Coconut, Banana, Tomato, Vegetables, Turmeric, All horticultural crops",
         "benefits":"40-60% water saving, 20-30% yield increase, reduced weed growth, fertigation possible, uniform water application",
         "cost":"₹40,000-60,000/acre (before subsidy). With PMKSY subsidy: ₹18,000-33,000/acre",
         "faq":[{"q":"How to install drip irrigation","a":"1. Contact empaneled drip company (Jain, Netafim, etc.). 2. Apply for PMKSY subsidy through horticulture dept (55% for small farmers). 3. Company surveys field and designs system. 4. Installation takes 1-2 days per acre. Cost: ₹40,000-60,000/acre before subsidy."},
                {"q":"Drip vs flood irrigation which is better","a":"Drip irrigation saves 40-60% water, increases yield 20-30%, reduces weeds, enables fertigation, and gives uniform water. Initial cost ₹40,000-60,000/acre but 55% subsidy available. Best for sugarcane, coconut, banana, vegetables. Flood irrigation wastes water and causes waterlogging."}]},
        {"id":"sprinkler","name":"Sprinkler Irrigation","type":"micro_irrigation",
         "description":"Overhead water application simulating rainfall. Good for field crops.",
         "suitable_crops":"Ragi, Maize, Groundnut, Pulses, Vegetables",
         "cost":"₹20,000-30,000/acre (before subsidy)",
         "faq":[{"q":"Sprinkler irrigation for ragi","a":"Sprinkler is good for ragi and millets. Cost ₹20,000-30,000/acre. Subsidy available under PMKSY. Saves 30-40% water. Provide 1 irrigation of 30mm every 7-10 days during dry spells. Best for supplemental irrigation in rainfed areas."}]}
    ]

def get_organic_farming():
    return [
        {"id":"jeevamrutha","name":"Jeevamrutha","type":"liquid_manure",
         "preparation":"Mix in 200L water: 10kg fresh cow dung + 10L cow urine + 2kg jaggery + 2kg pulse flour (gram/tur) + handful of soil from farm. Stir well. Ferment 48 hours in shade, stirring twice daily.",
         "application":"Apply 200L/acre through irrigation every 15 days. Or dilute 1:10 and drench around plants.",
         "benefits":"Improves soil microbial activity, provides nutrients, enhances soil structure, promotes earthworms.",
         "faq":[{"q":"How to make jeevamrutha","a":"In 200L water barrel, mix: 10kg fresh cow dung + 10L cow urine + 2kg jaggery + 2kg pulse flour (any dal flour) + handful of farm soil. Stir well, cover loosely, keep in shade. Stir twice daily for 48 hours. Apply 200L/acre through irrigation or dilute 1:10 for drenching. Make fresh batch every 2 weeks."}]},
        {"id":"beejamrutha","name":"Beejamrutha","type":"seed_treatment",
         "preparation":"Mix: 5kg cow dung + 5L cow urine + 50g lime + 20L water. Mix well. Soak seeds for 20 minutes before sowing.",
         "application":"Seed treatment before sowing. Protects against soil-borne diseases.",
         "faq":[{"q":"Organic seed treatment method","a":"Use Beejamrutha: Mix 5kg fresh cow dung + 5L cow urine + 50g lime in 20L water. Soak seeds for 20 minutes, dry in shade, then sow. Protects against soil-borne fungal diseases naturally. Use for paddy, ragi, maize, pulses."}]},
        {"id":"panchagavya","name":"Panchagavya","type":"growth_promoter",
         "preparation":"Mix: 5kg cow dung + 3L cow urine + 2L cow milk + 2L curd + 1L ghee + 3L sugarcane juice + 3L tender coconut water + 12 ripe bananas. Ferment 15 days, stir twice daily.",
         "application":"Dilute 3% (30ml/L) for foliar spray. Apply every 15 days. Also through drip/irrigation.",
         "faq":[{"q":"What is panchagavya how to use","a":"Panchagavya is a powerful organic growth promoter. Mix cow dung, urine, milk, curd, ghee, sugarcane juice, coconut water, bananas. Ferment 15 days. Dilute 30ml/L water for foliar spray every 15 days. Improves growth, flowering, fruit quality. Use for all crops."}]},
        {"id":"vermicompost","name":"Vermicompost","type":"compost",
         "preparation":"Layer cow dung + crop residues + kitchen waste in brick/cement bed. Add earthworms (Eisenia fetida). Keep moist. Ready in 60-90 days.",
         "application":"2-4 tonnes/acre as basal. Mix in pit for horticultural crops.",
         "cost":"₹8-12/kg if purchased. Make at home for free.",
         "faq":[{"q":"How to make vermicompost at home","a":"Build 3x1x0.5m brick bed in shade. Layer: 10cm dry crop residue + 10cm cow dung + 10cm kitchen waste/green matter. Add 1kg earthworms (Eisenia fetida). Keep moist (not waterlogged). Cover with jute. Ready in 60-90 days. Harvest by heaping and collecting worms from bottom. Apply 2-4 tonnes/acre."}]}
    ]

def get_general_faq():
    return [
        {"id":"mandya_profile","q":"Tell me about Mandya district agriculture","category":"general",
         "a":"Mandya district is one of Karnataka's most agriculturally prosperous regions, situated in the Cauvery river basin. It has 7 taluks: Mandya, Maddur, Malavalli, Pandavapura, Srirangapatna, Nagamangala, and K.R. Pet. Major crops: Paddy, Sugarcane, Ragi, Coconut, Banana, Mulberry (sericulture). Irrigation from KRS and Hemavathy dams. Soil: primarily red sandy loam. Known as 'Sugar Bowl of Karnataka'."},
        {"id":"kharif_crops","q":"What crops to grow in Kharif season in Mandya","category":"recommendation",
         "a":"Kharif (June-November) crops for Mandya: IRRIGATED - Paddy (main), Maize, Banana. RAINFED - Ragi (main), Jowar, Cowpea, Horse gram, Green gram, Black gram. Also sow Turmeric and Ginger in June-July. Start coconut planting. Nursery for vegetable seedlings (Tomato, Brinjal, Chili)."},
        {"id":"rabi_crops","q":"What crops to grow in Rabi season in Mandya","category":"recommendation",
         "a":"Rabi (November-March) crops for Mandya: IRRIGATED - Paddy (second crop), Maize, Tomato, Brinjal, Chili, Beans, Cabbage. RAINFED - Jowar (Rabi), Horse gram, Safflower. Winter vegetables do well. Good time for planting fruit trees. Sugarcane continues (perennial)."},
        {"id":"summer_crops","q":"What to grow in summer in Mandya","category":"recommendation",
         "a":"Summer (March-May) in Mandya: IRRIGATED - Watermelon, Muskmelon, Cucumber, Sunflower, Groundnut, Green gram (short duration). Summer ploughing recommended for pest/disease control. Prepare nursery for Kharif paddy (May-June). Apply FYM/compost to fields."},
        {"id":"soil_testing","q":"Where to get soil testing done in Mandya","category":"general",
         "a":"Get soil testing at: 1. Soil Testing Laboratory, Dept of Agriculture, Mandya. 2. KVK Mandya (V.C. Farm, Mandya). 3. IIHR Bangalore soil testing lab. Collect soil sample: Take 10-15 samples from field at 15cm depth in V-shape pattern. Mix well, take 500g. Cost: ₹50-100. Get test done before every season for best fertilizer recommendation."},
        {"id":"kvk_mandya","q":"Contact details KVK Mandya","category":"general",
         "a":"Krishi Vigyan Kendra (KVK) Mandya: Located at V.C. Farm, Mandya-571405, Karnataka. Under University of Agricultural Sciences, Bangalore. Services: Soil testing, Seed availability, Training programs, Farm advisory, Disease diagnosis. Visit for free expert advice on any farming problem."},
        {"id":"market_info","q":"Where to sell crops in Mandya","category":"market",
         "a":"APMC Markets in Mandya district: 1. Mandya APMC (main market yard). 2. Maddur APMC. 3. K.R. Pet APMC. 4. Nagamangala APMC. Sugar factories for sugarcane: Mandya Sugar (MySugar), Pandavapura Sugar Factory. Coconut: Mandya APMC or Tiptur market. Also sell through e-NAM portal for better prices."},
        {"id":"water_saving","q":"How to save water in farming","category":"irrigation",
         "a":"Water saving methods for Mandya farmers: 1. Drip irrigation (saves 40-60% water). 2. Sprinkler for field crops (saves 30%). 3. Mulching with crop residues (reduces evaporation 25%). 4. SRI method for paddy (uses 30% less water). 5. Raised bed planting for vegetables. 6. Farm ponds for rainwater harvesting (Krishi Bhagya subsidy available). 7. Alternate wetting-drying in paddy."},
        {"id":"crop_rotation","q":"Best crop rotation for Mandya","category":"recommendation",
         "a":"Recommended crop rotations for Mandya: 1. Paddy-Paddy-Green gram (2 year). 2. Sugarcane (3 years)-Paddy (1 year)-repeat. 3. Ragi-Horse gram-Ragi. 4. Tomato-Beans-Cabbage (vegetable rotation). 5. Maize-Groundnut rotation. Avoid: continuous paddy (depletes nutrients), continuous sugarcane beyond 3 ratoons. Rotate to break disease cycles."},
        {"id":"emergency_pest","q":"Emergency pest attack what to do","category":"emergency",
         "a":"Emergency pest attack steps: 1. IDENTIFY the pest - take photo/sample to agriculture office or KVK Mandya. 2. If identified, buy recommended pesticide from authorized dealer. 3. SPRAY in early morning or late evening (not mid-day). 4. Follow dosage exactly on label. 5. Wear protective clothing. 6. For large outbreaks, report to agriculture officer - government may provide free pesticides. 7. Keep Mandya agriculture officer helpline handy."},
        {"id":"seed_source","q":"Where to buy quality seeds in Mandya","category":"general",
         "a":"Quality seed sources in Mandya: 1. Karnataka State Seeds Corporation (KSSC) depot. 2. Raitha Samparka Kendra (RSK) at hobli level. 3. KVK Mandya (V.C. Farm). 4. University of Agricultural Sciences seed unit. 5. KSSC authorized dealers. 6. National Seeds Corporation outlets. Always buy certified/truthfully labeled seeds. Check packing date and germination percentage."},
        {"id":"loan_info","q":"How to get farm loan","category":"scheme",
         "a":"Farm loans available: 1. Kisan Credit Card (KCC) - up to ₹3 lakh at 4% interest (with subsidy). Apply at any bank with land documents. 2. Crop loan - short term for seasonal expenses. 3. Term loan for farm machinery, drip, bore well. Visit nearest bank (SBI, Canara Bank, Cooperative bank) with: RTC, Aadhaar, land documents, photos. Interest subvention makes effective rate 4% for loans up to ₹3 lakh."}
    ]

if __name__ == "__main__":
    import json
    data = {"schemes": get_schemes(), "fertilizers": get_fertilizer_guide(),
            "irrigation": get_irrigation_guide(), "organic": get_organic_farming(), "faq": get_general_faq()}
    print(json.dumps(data, indent=2))
