#!/usr/bin/env python3
"""Master knowledge base builder - combines all data generators and outputs JSON files."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_crops import get_crops
from gen_diseases import get_diseases
from gen_knowledge import get_schemes, get_fertilizer_guide, get_irrigation_guide, get_organic_farming, get_general_faq

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def build_crop_recommendations():
    return {
        "rules": [
            {"season":"Kharif","water":"irrigated","soil":"clay_loam","crops":["Paddy","Maize","Banana"],"notes":"Best season for paddy with KRS canal water"},
            {"season":"Kharif","water":"irrigated","soil":"red_sandy_loam","crops":["Paddy","Sugarcane","Banana","Turmeric"],"notes":"Red sandy loam with irrigation supports wide range"},
            {"season":"Kharif","water":"rainfed","soil":"red_sandy_loam","crops":["Ragi","Jowar","Cowpea","Horse gram","Green gram"],"notes":"Low water requirement millets and pulses ideal"},
            {"season":"Kharif","water":"rainfed","soil":"laterite","crops":["Ragi","Groundnut","Niger","Horse gram"],"notes":"Hardy crops for poor laterite soils"},
            {"season":"Rabi","water":"irrigated","soil":"clay_loam","crops":["Paddy (second crop)","Maize","Tomato","Cabbage"],"notes":"Second paddy crop if canal water available"},
            {"season":"Rabi","water":"irrigated","soil":"red_sandy_loam","crops":["Tomato","Brinjal","Chili","Beans","Maize","Cabbage"],"notes":"Vegetables give best returns in Rabi"},
            {"season":"Rabi","water":"rainfed","soil":"red_sandy_loam","crops":["Jowar (Rabi)","Horse gram","Safflower","Bengal gram"],"notes":"Rabi jowar and pulses for rainfed conditions"},
            {"season":"Summer","water":"irrigated","soil":"any","crops":["Watermelon","Cucumber","Sunflower","Green gram","Groundnut"],"notes":"Short duration crops for summer with limited water"},
            {"season":"Summer","water":"rainfed","soil":"any","crops":["Summer ploughing recommended","Green manure (Sun hemp/Daincha)"],"notes":"Prepare field for Kharif; green manuring improves soil"},
            {"season":"Year-round","water":"irrigated","soil":"red_sandy_loam","crops":["Sugarcane","Coconut","Banana","Mulberry"],"notes":"Perennial crops need continuous irrigation"},
            {"season":"Year-round","water":"irrigated","soil":"deep_loam","crops":["Coconut","Banana","Mango","Sapota"],"notes":"Deep soils for plantation/fruit crops"},
        ],
        "taluk_specific": {
            "Mandya": {"best_crops":["Paddy","Sugarcane","Banana","Coconut","Mulberry"],"irrigation":"KRS Canal, Hemavathy","notes":"Most irrigated taluk, suited for water-intensive crops"},
            "Maddur": {"best_crops":["Paddy","Sugarcane","Coconut","Mulberry","Banana"],"irrigation":"KRS Canal","notes":"Well-irrigated, similar to Mandya taluk"},
            "Malavalli": {"best_crops":["Paddy","Ragi","Coconut","Banana","Mango"],"irrigation":"Mixed - canal and rainfed","notes":"Parts irrigated, parts rainfed. Mango cultivation growing."},
            "Srirangapatna": {"best_crops":["Paddy","Sugarcane","Banana","Vegetables","Mulberry"],"irrigation":"KRS Canal","notes":"Close to KRS dam, well-irrigated, vegetable hub"},
            "Pandavapura": {"best_crops":["Paddy","Sugarcane","Coconut","Tomato","Vegetables"],"irrigation":"KRS Canal","notes":"Sugar factory nearby, sugarcane dominant"},
            "Nagamangala": {"best_crops":["Ragi","Jowar","Coconut","Groundnut","Horse gram"],"irrigation":"Mostly rainfed, bore wells","notes":"Dryland taluk, millets and pulses recommended"},
            "K.R. Pet": {"best_crops":["Ragi","Coconut","Maize","Turmeric","Mulberry"],"irrigation":"Hemavathy canal (partial), rainfed","notes":"Mixed irrigation, coconut and ragi dominant"}
        }
    }

def build_synonyms():
    return {
        "crop_synonyms": {
            "paddy":["rice","bhatta","nellu","akki","dhan"],
            "sugarcane":["cane","kabbu","ganna","sherdi"],
            "ragi":["finger millet","nachni","kelvaragu","mandua"],
            "coconut":["copra","nariyal","tenginakaayi","thengu"],
            "maize":["corn","mekkejola","makka","bhutta"],
            "jowar":["sorghum","jola","cholam","jwari"],
            "banana":["plantain","bale","kela","vazhai"],
            "tomato":["tamatar","thakkali"],
            "turmeric":["arishina","haldi","manjal"],
            "mulberry":["hippunerale","resham"],
            "groundnut":["peanut","shenga","kadalai"],
            "cowpea":["alasande","lobia"],
            "green gram":["moong","hesaru","mung"],
            "black gram":["urad","uddu"],
            "horse gram":["hurali","kulthi","kollu"],
            "tur dal":["red gram","pigeon pea","togari"]
        },
        "disease_synonyms": {
            "blast":["rice blast","leaf blast","neck blast","panicle blast","blight"],
            "brown spot":["brown leaf spot","helminthosporium"],
            "sheath blight":["sheath disease","rhizoctonia"],
            "blight":["bacterial blight","leaf blight","BLB"],
            "wilt":["fusarium wilt","panama wilt","wilting","soaking"],
            "rot":["root rot","bud rot","rhizome rot","stem rot","red rot"],
            "smut":["whip smut","kernel smut"],
            "rust":["leaf rust","stem rust","orange rust"],
            "mildew":["powdery mildew","downy mildew","white powder"]
        },
        "pest_synonyms": {
            "borer":["stem borer","shoot borer","internode borer","cob borer","fruit borer","top borer"],
            "worm":["army worm","fall army worm","caterpillar","huli","larva"],
            "weevil":["red palm weevil","rice weevil","grain weevil"],
            "beetle":["rhinoceros beetle","flea beetle","leaf beetle"],
            "fly":["whitefly","fruit fly","shoot fly","bean fly"],
            "hopper":["brown plant hopper","BPH","green leafhopper","jassid"],
            "mite":["eriophyid mite","spider mite","red mite"],
            "bug":["mealybug","stink bug","plant bug"]
        },
        "action_synonyms": {
            "disease":["problem","issue","infection","attack","damage","affected","dying","sick","unhealthy"],
            "fertilizer":["manure","gombara","nutrition","feed","nutrient","urea","DAP","potash","NPK"],
            "irrigation":["water","watering","neeru","canal","drip","sprinkler","bore well","pump"],
            "spray":["spraying","chemical","pesticide","fungicide","medicine","treatment","control"],
            "recommendation":["suggest","advice","best","suitable","which","what to grow","recommend"],
            "scheme":["subsidy","government","sarkari","help","financial","loan","insurance","PM-KISAN","PMFBY"],
            "organic":["natural","chemical free","jeevamrutha","panchagavya","vermicompost","bio"],
            "market":["sell","price","MSP","mandi","APMC","rate","cost"],
            "seed":["variety","hybrid","beeja","planting material","seedling","sapling"]
        }
    }

def build_intent_patterns():
    return {
        "disease": {
            "keywords":["disease","pest","insect","yellow","brown","spot","rot","wilt","blight","blast","curl","dying","drying","hole","damage","attack","infected","fungus","virus","bacteria","caterpillar","worm","borer","weevil","beetle","mite","fly","bug","mealybug","aphid","thrip"],
            "patterns":["leaves turning","spots on","my .* has","plant is dying","crop is affected","what is wrong","leaves are","problem with","attacked by","damage in","holes in","insects on","pests in","white powder","black spots","brown patches"]
        },
        "fertilizer": {
            "keywords":["fertilizer","urea","DAP","potash","MOP","NPK","manure","nutrient","deficiency","nitrogen","phosphorus","potassium","zinc","iron","dosage","quantity","how much","application"],
            "patterns":["how much .* per acre","fertilizer for","when to apply","which fertilizer","nutrient deficiency","dosage of","rate of","quantity of"]
        },
        "irrigation": {
            "keywords":["water","irrigation","drip","sprinkler","canal","bore well","pump","watering","schedule","frequency","KRS","dam","flood"],
            "patterns":["how often to water","water requirement","irrigation schedule","drip irrigation","canal water","when to irrigate","water management"]
        },
        "recommendation": {
            "keywords":["recommend","suggest","best","suitable","which crop","what to grow","should I grow","can I grow","profitable","good crop","right crop"],
            "patterns":["what .* to grow","best crop for","which crop","should I plant","suitable crop","recommend .* crop","what to sow","can I grow"]
        },
        "scheme": {
            "keywords":["scheme","subsidy","government","PM-KISAN","insurance","PMFBY","loan","help","financial","assistance","benefit","apply","registration","Krishi Bhagya"],
            "patterns":["government scheme","how to apply","subsidy for","financial help","crop insurance","get loan","PM-KISAN"]
        },
        "organic": {
            "keywords":["organic","natural","jeevamrutha","panchagavya","beejamrutha","vermicompost","compost","bio-fertilizer","chemical free","neem","cow dung","cow urine"],
            "patterns":["organic farming","how to make","natural method","without chemical","organic .* for","prepare organic"]
        },
        "cultivation": {
            "keywords":["sowing","planting","harvest","transplant","spacing","seed rate","variety","season","nursery","pruning","intercrop","crop calendar","duration","when to sow","when to plant"],
            "patterns":["how to grow","when to sow","planting time","seed rate","spacing for","how to cultivate","best variety","harvest time","crop duration"]
        },
        "market": {
            "keywords":["price","sell","market","MSP","APMC","mandi","rate","cost","income","profit","where to sell","procurement"],
            "patterns":["market price","where to sell","MSP for","current rate","how much .* per"]
        }
    }

def build_all():
    print("Building AgriVision Knowledge Base...")
    
    # 1. Main knowledge base
    kb = {
        "metadata": {"version": "1.0", "region": "Mandya District, Karnataka", "last_updated": "2026-04-25",
                      "total_crops": 10, "total_diseases": 20, "description": "Comprehensive agricultural advisory knowledge base for Mandya district"},
        "crops": get_crops(),
        "diseases": get_diseases(),
        "schemes": get_schemes(),
        "fertilizers": get_fertilizer_guide(),
        "irrigation": get_irrigation_guide(),
        "organic_farming": get_organic_farming(),
        "general_faq": get_general_faq()
    }
    with open(os.path.join(DATA_DIR, "mandya_knowledge_base.json"), "w") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    print(f"  ✓ mandya_knowledge_base.json ({len(kb['crops'])} crops, {len(kb['diseases'])} diseases, {len(kb['schemes'])} schemes)")

    # 2. Synonyms
    synonyms = build_synonyms()
    with open(os.path.join(DATA_DIR, "synonyms.json"), "w") as f:
        json.dump(synonyms, f, indent=2, ensure_ascii=False)
    total_syns = sum(len(v) for d in synonyms.values() for v in d.values())
    print(f"  ✓ synonyms.json ({total_syns} synonym mappings)")

    # 3. Intent patterns
    intents = build_intent_patterns()
    with open(os.path.join(DATA_DIR, "intent_patterns.json"), "w") as f:
        json.dump(intents, f, indent=2, ensure_ascii=False)
    print(f"  ✓ intent_patterns.json ({len(intents)} intent categories)")

    # 4. Crop recommendations
    recommendations = build_crop_recommendations()
    with open(os.path.join(DATA_DIR, "crop_recommendations.json"), "w") as f:
        json.dump(recommendations, f, indent=2, ensure_ascii=False)
    print(f"  ✓ crop_recommendations.json ({len(recommendations['rules'])} rules, {len(recommendations['taluk_specific'])} taluks)")

    # Count total searchable entries
    total = len(kb['crops']) + len(kb['diseases']) + len(kb['schemes']) + len(kb['fertilizers']) + len(kb['irrigation']) + len(kb['organic_farming']) + len(kb['general_faq'])
    # Count FAQ entries embedded in diseases
    faq_count = sum(len(d.get('faq', [])) for d in kb['diseases'])
    faq_count += sum(len(s.get('faq', [])) for s in kb['schemes'])
    faq_count += sum(len(f.get('faq', [])) for f in kb['fertilizers'])
    faq_count += sum(len(i.get('faq', [])) for i in kb['irrigation'])
    faq_count += sum(len(o.get('faq', [])) for o in kb['organic_farming'])
    faq_count += len(kb['general_faq'])
    
    print(f"\n✅ Knowledge base complete!")
    print(f"   Total main entries: {total}")
    print(f"   Total FAQ/Q&A pairs: {faq_count}")
    print(f"   Total searchable items: {total + faq_count}")

if __name__ == "__main__":
    build_all()
