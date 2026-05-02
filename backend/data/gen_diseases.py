#!/usr/bin/env python3
"""Generate diseases section of knowledge base."""

def get_diseases():
    return [
        {"id":"blast","name":"Rice Blast","crop":"paddy","type":"fungal","pathogen":"Pyricularia oryzae",
         "symptoms":"Diamond-shaped spots with grey center and brown margin on leaves. Neck blast causes panicle breakage at neck node. Node blast causes black lesions on nodes.",
         "favorable_conditions":"High humidity >90%, temperature 25-28°C, excess nitrogen, cloudy weather with drizzle",
         "management":{"chemical":"Spray Tricyclazole 75WP 0.6g/L or Isoprothiolane 1.5ml/L at first symptom. For neck blast: spray Tricyclazole at boot leaf stage (before flowering). Repeat after 10 days if needed.",
                       "cultural":"Use resistant varieties (MTU-1010). Avoid excess nitrogen. Maintain proper spacing. Remove infected plant debris. Balanced NPK fertilization.",
                       "biological":"Pseudomonas fluorescens 10g/L seed treatment + foliar spray at tillering."},
         "severity":"high","critical_stage":"Tillering and flowering","faq":[
            {"q":"How to identify blast in paddy?","a":"Look for diamond or eye-shaped spots on leaves with grey/white center and brown border. In severe cases, entire leaves dry up. Neck blast shows brown/black discoloration at panicle base causing panicle to break and hang."},
            {"q":"When to spray for blast in paddy?","a":"Spray Tricyclazole 0.6g/L at first appearance of leaf blast symptoms. For neck blast prevention, spray at boot leaf stage (when flag leaf sheath swells before panicle emergence). This is the most critical spray."},
            {"q":"My paddy leaves have brown diamond spots","a":"This is rice blast disease caused by Pyricularia oryzae fungus. Spray Tricyclazole 75WP at 0.6g/L or Isoprothiolane at 1.5ml/L. Avoid excess nitrogen. Spray immediately and repeat after 10 days."}
         ]},
        {"id":"brown_leaf_spot","name":"Brown Leaf Spot","crop":"paddy","type":"fungal","pathogen":"Helminthosporium oryzae",
         "symptoms":"Oval brown spots on leaves with grey center. In severe cases, spots merge causing leaf drying. Grains may show black discoloration.",
         "favorable_conditions":"Nutrient-deficient soils, high humidity, temperatures 25-30°C, waterlogged fields",
         "management":{"chemical":"Spray Mancozeb 2.5g/L or Propiconazole 1ml/L. Apply Zineb 75WP 2g/L.",
                       "cultural":"Ensure balanced fertilization especially potassium. Proper drainage. Use certified disease-free seeds. Avoid continuous paddy cropping.",
                       "biological":"Trichoderma viride seed treatment 5g/kg seed."},
         "severity":"medium","critical_stage":"Grain filling","faq":[
            {"q":"Brown spots on paddy leaves","a":"This is likely Brown Leaf Spot (Helminthosporium). Apply balanced fertilizers, especially potassium (MOP). Spray Mancozeb 2.5g/L. Ensure field drainage. This disease is common in nutrient-deficient soils."}
         ]},
        {"id":"sheath_blight","name":"Sheath Blight","crop":"paddy","type":"fungal","pathogen":"Rhizoctonia solani",
         "symptoms":"Water-soaked oval greenish-grey lesions on leaf sheaths near water line. Lesions enlarge with greyish-white center and brown margin. Multiple lesions coalesce forming banded pattern.",
         "favorable_conditions":"Dense planting, excess nitrogen, high humidity, stagnant water, temperature 28-32°C",
         "management":{"chemical":"Spray Hexaconazole 2ml/L or Validamycin 2ml/L targeting lower leaf sheaths. Propiconazole 1ml/L also effective.",
                       "cultural":"Avoid dense planting. Reduce nitrogen. Ensure proper spacing (20x15cm minimum). Drain fields periodically. Remove weed hosts.",
                       "biological":"Trichoderma harzianum application to soil at transplanting."},
         "severity":"high","critical_stage":"Tillering to grain filling","faq":[
            {"q":"White-grey patches on paddy stem near water","a":"This is Sheath Blight caused by Rhizoctonia solani. Spray Hexaconazole 2ml/L or Validamycin 2ml/L on the lower portions of the plant. Drain excess water. Avoid excess nitrogen fertilizer."}
         ]},
        {"id":"bacterial_leaf_blight","name":"Bacterial Leaf Blight (BLB)","crop":"paddy","type":"bacterial","pathogen":"Xanthomonas oryzae pv. oryzae",
         "symptoms":"Water-soaked lesions starting from leaf tips/margins, turning yellow then white-grey. Leaves dry from tip downward. Bacterial ooze visible as yellow beads on leaf surface in morning.",
         "favorable_conditions":"Wounds from storms/heavy rains, high nitrogen, temperature 25-30°C, transplanting injury",
         "management":{"chemical":"No effective chemical cure. Streptocycline 0.5g + Copper oxychloride 2.5g per liter. Copper hydroxide 2g/L.",
                       "cultural":"Use resistant varieties. Avoid clipping seedling tips during transplanting. Balanced NPK. Proper field drainage. Avoid excess nitrogen.",
                       "biological":"Pseudomonas fluorescens 10g/L foliar spray."},
         "severity":"high","critical_stage":"Tillering to heading","faq":[
            {"q":"Paddy leaves drying from tip turning yellow","a":"This could be Bacterial Leaf Blight (BLB). There's no complete chemical cure. Spray Streptocycline 0.5g + Copper oxychloride 2.5g per liter. Use resistant varieties next season. Avoid excess nitrogen. Ensure proper drainage."}
         ]},
        {"id":"sheath_rot","name":"Sheath Rot","crop":"paddy","type":"fungal","pathogen":"Sarocladium oryzae",
         "symptoms":"Dark brown discoloration on flag leaf sheath enclosing panicle. Partially emerged or rotting panicles. White powdery fungal growth inside sheath.",
         "favorable_conditions":"High nitrogen, insect damage (especially rice mite), high humidity",
         "management":{"chemical":"Spray Carbendazim 1g/L + Mancozeb 2g/L at boot leaf stage.",
                       "cultural":"Balanced nutrition. Control mites and insects. Use clean seed. Proper spacing.",
                       "biological":"Pseudomonas fluorescens 10g/L spray at boot stage."},
         "severity":"medium","critical_stage":"Boot leaf to heading","faq":[]},
        {"id":"red_rot","name":"Red Rot","crop":"sugarcane","type":"fungal","pathogen":"Colletotrichum falcatum",
         "symptoms":"Drying and withering of crown leaves. Red discoloration of internal cane tissue with white patches. Rotten cane with alcoholic smell. Cross-section shows reddened vascular bundles.",
         "favorable_conditions":"Waterlogged conditions, susceptible varieties, poor drainage, infected seed material",
         "management":{"chemical":"No effective chemical cure after infection. Sett treatment with Carbendazim 1g/L for 15 minutes before planting.",
                       "cultural":"Use disease-free seed material from healthy nurseries. Grow resistant varieties (Co-86032). Avoid waterlogging. Remove and burn infected canes. Crop rotation with paddy. Hot water treatment of setts at 50°C for 2 hours.",
                       "biological":"Trichoderma viride soil application 2.5kg/acre mixed with FYM."},
         "severity":"very high","critical_stage":"5-8 months (grand growth phase)","faq":[
            {"q":"Sugarcane leaves drying, red inside cane","a":"This is Red Rot - the most destructive sugarcane disease. Remove and burn all infected canes immediately. Don't use infected canes as seed. Treat setts with Carbendazim 1g/L before planting. Switch to resistant variety Co-86032 next season."},
            {"q":"How to prevent red rot in sugarcane","a":"Use disease-free setts from certified nurseries. Treat setts with Carbendazim 1g/L for 15 min. Grow resistant varieties like Co-86032. Ensure proper drainage. Practice crop rotation with paddy every 3-4 years. Hot water treatment at 50°C for 2 hours."}
         ]},
        {"id":"smut","name":"Whip Smut","crop":"sugarcane","type":"fungal","pathogen":"Ustilago scitaminea",
         "symptoms":"Black whip-like structure (sorus) emerging from top of cane, covered with black powdery spores. Thin grassy tillers. Reduced cane girth.",
         "favorable_conditions":"Ratoon crops, infected seed material, dry conditions",
         "management":{"chemical":"Sett treatment with Carbendazim 1g/L or Propiconazole 1ml/L for 15 min.",
                       "cultural":"Remove and burn smut whips before they open. Don't ratoon infected fields. Use disease-free setts. Grow resistant varieties.",
                       "biological":"Trichoderma viride seed treatment."},
         "severity":"high","critical_stage":"5-7 months","faq":[
            {"q":"Black whip coming out of sugarcane top","a":"This is Whip Smut disease. Remove and burn the black whips immediately before spores spread. Don't take ratoon from this field. Use fresh disease-free setts next season. Treat setts with Carbendazim 1g/L."}
         ]},
        {"id":"wilt_sugarcane","name":"Sugarcane Wilt","crop":"sugarcane","type":"fungal","pathogen":"Fusarium sacchari",
         "symptoms":"Yellowing and drying of leaves from bottom. Internal browning of vascular bundles. Hollow pith in advanced stages. Stunted growth.",
         "favorable_conditions":"Waterlogging followed by drought, poor drainage, ratoon crop, nematode damage",
         "management":{"chemical":"Sett treatment with Carbendazim 2g/L + Chlorpyrifos 2.5ml/L.",
                       "cultural":"Avoid waterlogging. Good drainage. Use healthy setts. Crop rotation. Remove infected stools.",
                       "biological":"Trichoderma harzianum 2.5kg/acre mixed with FYM."},
         "severity":"high","critical_stage":"4-7 months","faq":[]},
        {"id":"grassy_shoot","name":"Grassy Shoot Disease","crop":"sugarcane","type":"phytoplasma","pathogen":"Phytoplasma",
         "symptoms":"Profuse tillering producing thin grassy shoots. White or pale green chlorotic leaves. No millable canes formed. Looks like grass clump.",
         "favorable_conditions":"Infected seed material, leafhopper transmission",
         "management":{"chemical":"No chemical cure. Hot water treatment of setts at 50°C for 2 hours.",
                       "cultural":"Use disease-free certified setts only. Rogue out infected clumps immediately. Control leafhopper vectors. Don't ratoon affected fields.",
                       "biological":"None effective."},
         "severity":"very high","critical_stage":"Throughout growth","faq":[
            {"q":"Sugarcane growing like grass, no thick canes","a":"This is Grassy Shoot Disease caused by phytoplasma. No cure exists. Remove all infected clumps immediately. Don't use any canes from this field as seed. Next season, buy fresh certified disease-free setts and treat with hot water at 50°C for 2 hours."}
         ]},
        {"id":"finger_blast","name":"Finger Millet Blast","crop":"ragi","type":"fungal","pathogen":"Pyricularia grisea",
         "symptoms":"Diamond-shaped lesions on leaves. Neck blast: darkening at finger/ear base causing finger breakage. Finger blast: partial or no grain filling in affected fingers.",
         "favorable_conditions":"High humidity, excess nitrogen, cloudy weather, heavy dew",
         "management":{"chemical":"Spray Tricyclazole 0.6g/L at 50% flowering for neck/finger blast prevention. Carbendazim 1g/L for leaf blast.",
                       "cultural":"Use resistant varieties GPU-28. Avoid excess nitrogen. Optimal spacing. Early sowing.",
                       "biological":"Pseudomonas fluorescens seed treatment."},
         "severity":"high","critical_stage":"Flowering","faq":[
            {"q":"Ragi fingers breaking, black at base","a":"This is Finger/Neck Blast in ragi. For current season, if caught early spray Tricyclazole 0.6g/L. For next season, spray preventively at 50% flowering. Use resistant variety GPU-28. Don't apply excess nitrogen."}
         ]},
        {"id":"bud_rot_coconut","name":"Bud Rot","crop":"coconut","type":"fungal","pathogen":"Phytophthora palmivora",
         "symptoms":"Yellowing and wilting of central spindle leaf. Rotting of growing point (bud). Foul smell from crown. Eventually entire crown collapses.",
         "favorable_conditions":"High rainfall, waterlogging, poor drainage, humid conditions",
         "management":{"chemical":"Remove rotted tissue, apply Bordeaux paste on cut surface. Pour Copper oxychloride 3g/L into crown. Metalaxyl-Mancozeb 2.5g/L drench.",
                       "cultural":"Ensure drainage. Remove severely affected palms. Crown cleaning. Avoid injury to crown during harvesting.",
                       "biological":"Trichoderma application to crown region."},
         "severity":"very high","critical_stage":"Monsoon season","faq":[
            {"q":"Coconut tree center leaf dying, bad smell","a":"This is Bud Rot - very serious disease. Act immediately: Remove all rotted tissue from crown. Apply Bordeaux paste on cut surface. Pour Copper oxychloride solution (3g/L) into crown cavity. Ensure drainage around palm. If growing point is completely destroyed, the palm cannot be saved."}
         ]},
        {"id":"red_palm_weevil_disease","name":"Red Palm Weevil Attack","crop":"coconut","type":"pest","pathogen":"Rhynchophorus ferrugineus",
         "symptoms":"Holes on trunk with chewed fiber extruding. Yellowing and drooping of inner fronds. Crown toppling in severe cases. Grubs feed inside trunk.",
         "favorable_conditions":"Wounds on trunk, poor palm health, neglected gardens",
         "management":{"chemical":"Inject Monocrotophos 10ml + 10ml water into trunk holes and seal with cement. Place pheromone traps (Ferrugineol) to catch adults.",
                       "cultural":"Avoid trunk injuries. Remove dead palms. Fill leaf axils with sand + BHC. Regular garden maintenance.",
                       "biological":"Release Beauveria bassiana spore suspension into trunk holes."},
         "severity":"very high","critical_stage":"Year-round","faq":[
            {"q":"Holes in coconut trunk, fiber coming out","a":"This is Red Palm Weevil attack. Inject Monocrotophos 10ml diluted in 10ml water into each hole and seal with cement/mud. Set up Ferrugineol pheromone traps (3-5/acre). Keep garden clean. Apply preventive sand+BHC mixture in leaf axils of healthy palms."}
         ]},
        {"id":"rhinoceros_beetle","name":"Rhinoceros Beetle","crop":"coconut","type":"pest","pathogen":"Oryctes rhinoceros",
         "symptoms":"V-shaped cuts on emerging fronds. Bore holes on crown with chewed fiber. Reduced yield. Secondary fungal infections in bore holes.",
         "favorable_conditions":"Decaying organic matter (breeding sites), neglected manure pits, decomposing trunks",
         "management":{"chemical":"Fill top 3 leaf axils with sand 250g + Neem cake 250g mixture. Insert Naphthalene balls 3-4 in leaf axils.",
                       "cultural":"Remove and burn all decaying trunks/logs. Maintain breeding site hygiene. Cover manure/compost pits.",
                       "biological":"Install Oryctes virus (OrNV) infected beetles. Use Metarhizium anisopliae 50g/palm in crown."},
         "severity":"high","critical_stage":"Year-round, peak in monsoon","faq":[
            {"q":"Coconut leaves have V-shaped cuts","a":"This is Rhinoceros Beetle damage. Fill top 3 leaf axils with mixture of 250g fine sand + 250g neem cake. Place 3-4 naphthalene balls in inner leaf axils. Clean up all decaying organic matter, old trunks and logs around your garden - these are beetle breeding sites."}
         ]},
        {"id":"panama_wilt","name":"Panama Wilt (Fusarium Wilt)","crop":"banana","type":"fungal","pathogen":"Fusarium oxysporum f.sp. cubense",
         "symptoms":"Yellowing and splitting of outer leaf sheaths (pseudostem). Leaves droop and collapse around pseudostem like a skirt. Internal pseudostem shows reddish-brown vascular discoloration.",
         "favorable_conditions":"Infected soil, nematode damage, waterlogging, acidic soils",
         "management":{"chemical":"No effective chemical cure after infection. Drench Carbendazim 2g/L around healthy plants as preventive.",
                       "cultural":"Use disease-free tissue culture plants. Don't plant banana in infected soil for 5 years. Grow resistant varieties (Poovan/Yelakki). Soil solarization. Apply lime 2kg/pit for acidic soils.",
                       "biological":"Trichoderma viride 50g/plant + Pseudomonas fluorescens 50g/plant applied to soil at planting and 3 months."},
         "severity":"very high","critical_stage":"3-6 months","faq":[
            {"q":"Banana plant leaves drooping, yellow, stem splitting","a":"This is Panama Wilt (Fusarium Wilt) - most destructive banana disease. No chemical cure. Remove infected plants with roots and burn. Don't plant banana in same spot for 5 years. Use tissue culture plants next time. Apply Trichoderma 50g + Pseudomonas 50g per plant at planting. Use resistant Poovan/Yelakki variety."}
         ]},
        {"id":"early_blight_tomato","name":"Early Blight","crop":"tomato","type":"fungal","pathogen":"Alternaria solani",
         "symptoms":"Dark brown circular spots with concentric rings (target-board pattern) on lower leaves first. Spots enlarge, leaves yellow and drop. Stem and fruit lesions possible.",
         "favorable_conditions":"Warm humid weather 24-29°C, prolonged leaf wetness, dense planting",
         "management":{"chemical":"Spray Mancozeb 2.5g/L or Chlorothalonil 2g/L at first symptoms. Alternate with Azoxystrobin 1ml/L.",
                       "cultural":"Remove lower infected leaves. Proper spacing. Mulching to prevent soil splash. Crop rotation. Stake plants.",
                       "biological":"Trichoderma viride foliar spray."},
         "severity":"medium-high","critical_stage":"Fruiting","faq":[
            {"q":"Tomato lower leaves brown spots with rings","a":"This is Early Blight (Alternaria). Remove lower infected leaves. Spray Mancozeb 2.5g/L immediately. Ensure proper spacing and staking. Mulch around plants to prevent soil splash. Rotate crops - don't grow tomato/brinjal in same spot next season."}
         ]},
        {"id":"leaf_curl_tomato","name":"Tomato Leaf Curl Virus","crop":"tomato","type":"viral","pathogen":"Tomato leaf curl virus (ToLCV), transmitted by whitefly",
         "symptoms":"Upward curling of leaves. Leaves become thick, leathery, and crinkled. Stunted growth. Reduced or no fruit set. Yellow margin on leaves.",
         "favorable_conditions":"High whitefly population, warm dry weather, no resistant varieties",
         "management":{"chemical":"No cure for virus. Control whitefly vector: Imidacloprid 0.3ml/L or Thiamethoxam 0.3g/L spray every 15 days. Yellow sticky traps.",
                       "cultural":"Use resistant varieties (Arka Rakshak). Remove infected plants early. Barrier crops (maize/sorghum). Avoid planting near old infected fields.",
                       "biological":"Neem oil 5ml/L spray for whitefly. Release Encarsia formosa parasitoid."},
         "severity":"very high","critical_stage":"Seedling to vegetative","faq":[
            {"q":"Tomato leaves curling upward, stunted","a":"This is Tomato Leaf Curl Virus spread by whiteflies. No cure for infected plants - remove and destroy them. Control whiteflies with Imidacloprid 0.3ml/L spray. Use yellow sticky traps. Next season use resistant variety Arka Rakshak. Plant barrier crops like maize around tomato field."}
         ]},
        {"id":"powdery_mildew_mulberry","name":"Powdery Mildew","crop":"mulberry","type":"fungal","pathogen":"Phyllactinia corylea",
         "symptoms":"White powdery patches on lower leaf surface. Leaves curl upward. Premature leaf fall. Reduced leaf quality for silkworm feeding.",
         "favorable_conditions":"Cool dry weather (18-24°C), low humidity, winter months",
         "management":{"chemical":"Spray wettable Sulphur 3g/L or Carbendazim 0.5g/L. Wait 10-15 days after spray before feeding leaves to silkworms.",
                       "cultural":"Proper spacing. Adequate irrigation. Balanced fertilization. Remove affected leaves.",
                       "biological":"None recommended for mulberry (chemical residue affects silkworms)."},
         "severity":"medium","critical_stage":"Winter months","faq":[
            {"q":"White powder on mulberry leaves","a":"This is Powdery Mildew. Spray wettable Sulphur 3g/L. IMPORTANT: Wait at least 15 days after spraying before feeding leaves to silkworms, as chemical residues can kill silkworms."}
         ]},
        {"id":"rhizome_rot_turmeric","name":"Rhizome Rot","crop":"turmeric","type":"fungal","pathogen":"Pythium aphanidermatum",
         "symptoms":"Water-soaked lesions on collar region. Yellowing of lower leaves. Pseudostem pulls out easily. Rhizome becomes soft, brown, rotten with foul smell.",
         "favorable_conditions":"Waterlogging, heavy rain, poor drainage, infected seed rhizomes",
         "management":{"chemical":"Drench Metalaxyl-Mancozeb 2.5g/L around infected plants. Seed treatment with Metalaxyl 2g/kg rhizome.",
                       "cultural":"Use disease-free seed rhizomes. Ensure good drainage. Raised bed cultivation. Remove infected plants. Treat seed with hot water 50°C for 30 min.",
                       "biological":"Trichoderma viride 5g/kg rhizome treatment + soil application 2.5kg/acre."},
         "severity":"high","critical_stage":"Monsoon (July-September)","faq":[
            {"q":"Turmeric plant yellowing, rhizome rotting","a":"This is Rhizome Rot (Pythium). Remove infected plants immediately. Drench surrounding healthy plants with Metalaxyl-Mancozeb 2.5g/L. Ensure drainage. For next season: treat seed rhizomes with Trichoderma 5g/kg or Metalaxyl 2g/kg. Plant on raised beds."}
         ]},
        {"id":"fall_army_worm","name":"Fall Armyworm","crop":"maize","type":"pest","pathogen":"Spodoptera frugiperda",
         "symptoms":"Ragged feeding on whorl leaves. Windowing of leaves. Heavy frass (insect excrement) in whorl. Large caterpillars with inverted Y on head.",
         "favorable_conditions":"Warm weather, late sowing, monocropping, lack of natural enemies",
         "management":{"chemical":"Spray Emamectin benzoate 0.4g/L or Chlorantraniliprole 0.3ml/L into whorls. Spray early morning/late evening when larvae are active.",
                       "cultural":"Early sowing. Intercrop with pulses. Erect bird perches 20/acre. Install pheromone traps 5/acre. Hand-pick egg masses.",
                       "biological":"Release Trichogramma chilonis egg parasitoid cards 8/acre. Spray Bt (Bacillus thuringiensis) 2g/L. Apply NPV (Nuclear Polyhedrosis Virus) 250 LE/acre."},
         "severity":"high","critical_stage":"Vegetative (whorl stage)","faq":[
            {"q":"Caterpillar eating maize whorl leaves","a":"This is Fall Armyworm. Spray Emamectin benzoate 0.4g/L directly into the leaf whorls. Spray early morning when larvae are active. For organic control: apply Bt (Bacillus thuringiensis) 2g/L. Install pheromone traps and bird perches. Hand-pick and destroy egg masses."}
         ]}
    ]

if __name__ == "__main__":
    import json
    print(json.dumps(get_diseases(), indent=2))
