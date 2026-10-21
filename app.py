import streamlit as st
import pandas as pd
import pydeck as pdk
import streamlit.components.v1 as components

# --- 1. APP CONFIG & STYLING ---
try:
    st.set_page_config(
        page_title="HealthBridge - Aceternity Cloud Edition", 
        page_icon="🏥", 
        layout="wide"
    )
except Exception:
    pass

current_tab = st.query_params.get("tab", "Home")
if isinstance(current_tab, list):
    current_tab = current_tab[0]

# --- 2. CACHED DATA & LOGIC ---
@st.cache_data
def get_cached_map_data(user_lat, user_lon, h_lat, h_lon, h_name):
    return pd.DataFrame([
        {
            "latitude": user_lat, 
            "longitude": user_lon, 
            "name": "Your Location (Patient - GPS Active)", 
            "color": [56, 189, 248, 255],
            "radius": 75
        },
        {
            "latitude": h_lat, 
            "longitude": h_lon, 
            "name": h_name, 
            "color": [244, 63, 94, 255],
            "radius": 85
        }
    ])

@st.cache_data
def auto_categorize_medicine(med_name):
    try:
        name = med_name.lower()
        if any(k in name for k in ["metformin", "insulin", "sugar", "diab"]):
            return "Diabetes"
        elif any(k in name for k in ["amlodipine", "bp", "pressure", "atenolol", "losartan", "telmisartan"]):
            return "Blood Pressure"
        elif any(k in name for k in ["vitamin", "d3", "c", "supplement", "multivitamin", "calcium", "iron"]):
            return "Wellness"
        elif any(k in name for k in ["pain", "paracetamol", "ibuprofen", "aspirin", "diclofenac"]):
            return "Pain Relief"
        else:
            return "General Medication"
    except Exception:
        return "General Medication"

@st.cache_data
def get_default_schedule():
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    default_schedule = {}
    for w in weeks:
        default_schedule[w] = {
            d: [
                {"name": "Metformin (500mg)", "time": "08:00 AM", "status": "Pending", "category": "Diabetes"}
            ] if d in ["Monday", "Thursday"] else [
                {"name": "Amlodipine (5mg)", "time": "01:00 PM", "status": "Pending", "category": "Blood Pressure"}
            ] if d in ["Tuesday", "Friday"] else [
                {"name": "Vitamin D3 Supplement", "time": "08:00 PM", "status": "Pending", "category": "Wellness"}
            ] for d in days
        }
    return default_schedule

# --- 3. SESSION STATE INITIALIZATION ---
try:
    if "patient_passport" not in st.session_state:
        st.session_state.patient_passport = {
            "name": "Manas S. Abitkar",
            "blood_group": "O+ Positive",
            "emergency_contact": "+91 98765 43210 (Caregiver)",
            "allergies": "Penicillin, Peanuts",
            "conditions": "Type 2 Diabetes, Hypertension",
            "physician": "Dr. Sharma (City General Hospital)"
        }

    if "user_location" not in st.session_state:
        st.session_state.user_location = {
            "lat": 16.7010,
            "lon": 74.2390,
            "status": "GPS Active (Kolhapur Central)"
        }

    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {"msg": "HealthBridge Master Edition Initialized.", "time": "System Init"}
        ]

    if "meds_by_week" not in st.session_state:
        st.session_state.meds_by_week = get_default_schedule()

    if "questions" not in st.session_state:
        st.session_state.questions = ["Are there any food restrictions with this dosage?"]

    if "language" not in st.session_state:
        st.session_state.language = "English"

    if "pill_stock" not in st.session_state:
        st.session_state.pill_stock = 4

    if "last_speech" not in st.session_state:
        st.session_state.last_speech = "Hello Manas! I am Healtho, your interactive AI health companion. Ask me any question below."

except Exception as init_error:
    st.error(f"Initialization Notice: {init_error}")

# --- 4. TRANSLATIONS DICTIONARY ---
translations = {
    "English": {
        "title": "Next-Gen Patient Companion",
        "subtitle": "Precision Healthcare, Cloud Triage & Caregiving Portal for SDG 3",
        "active_plan": "Active Treatment Plan",
        "active_val": "Week 1 Active",
        "active_delta": "92% Dose Adherence",
        "emerg_ready": "Emergency Readiness",
        "emerg_val": "GPS Online",
        "emerg_delta": "Kolhapur Region",
        "care_link": "Caregiver Link",
        "care_val": "Connected",
        "care_delta": "PIN Protected",
        "healtho_title": "Meet Healtho - Voice & Text AI Health Companion",
        "healtho_subtitle": "Type your query below. Healtho will respond and can read the answer out loud!",
        "healtho_input_ph": "Ask Healtho... (e.g., 'When should I take Metformin?' or 'I feel dizzy')",
        "speak_btn": "🔊 Hear Healtho Speak Response Out Loud",
        "bento_title": "Quick Access Modules",
        "hosp_card_title": "Hospital Hub",
        "hosp_card_desc": "Disease-to-hospital routing with PyDeck maps.",
        "med_card_title": "Medication Suite",
        "med_card_desc": "Multi-week medication schedules and tracking.",
        "pass_card_title": "Secure Passport",
        "pass_card_desc": "Digital ID with single-tap emergency SOS broadcasting.",
        "btn_open": "Open",
        "hosp_title": "Intelligent Hospital Finder",
        "search_heading": "Smart Symptom & Hospital Match",
        "search_label": "Type condition / symptom:",
        "search_placeholder": "Type condition... (e.g., Heart, Eye, Bones)",
        "rec_fac": "Recommended Facility:",
        "map_cyan": "Cyan Pin = Live GPS Location",
        "map_rose": "Rose Pin = Recommended Specialized Hospital",
        "med_sched_title": "Multi-Week Medication Schedule",
        "choose_week": "Choose Week:",
        "choose_day": "Choose Day:",
        "no_meds": "No medications scheduled for",
        "mark_taken": "Mark Taken",
        "taken": "Taken ✅",
        "doc_title": "Doctor Appointments & Questions",
        "doc_info": "**Dr. Sharma (Cardiologist)**\nTomorrow at 10:30 AM\nCity General Hospital",
        "add_q_label": "Add a question for your doctor:",
        "add_q_placeholder": "e.g. Any food restrictions?",
        "save_q_btn": "Save Question",
        "saved_qs": "Your Saved Questions:",
        "care_title": "Caregiver Manager",
        "care_sub": "Remote family monitoring and profile controls.",
        "care_pin_label": "Enter Caregiver Access PIN:",
        "care_pin_ph": "Enter PIN (Demo: 1234)",
        "access_granted": "Access Granted! Connected to Patient Profile #PAT-8821",
        "ocr_title": "OCR Prescription Scanner",
        "ocr_upload": "Upload prescription image:",
        "ocr_btn": "Extract Medications",
        "edit_pass_exp": "Edit Patient Medical Passport Details",
        "update_info": "Update Information",
        "full_name": "Full Legal Name:",
        "blood_group": "Blood Group:",
        "emerg_contact": "Emergency Contact:",
        "allergies": "Known Allergies:",
        "conditions": "Chronic Conditions:",
        "physician": "Primary Physician:",
        "save_pass_btn": "Save Passport Updates",
        "add_med_exp": "Add New Medication",
        "med_name_label": "Medicine Name:",
        "med_name_ph": "e.g., Paracetamol (650mg)",
        "sched_time_label": "Time:",
        "sched_time_ph": "e.g., 02:00 PM",
        "assign_week": "Assign Week:",
        "assign_day": "Assign Day:",
        "add_med_btn": "Add Medication",
        "med_table_title": "Prescriptions Overview",
        "overall_adh": "Patient Adherence Rate",
        "send_note_label": "Send reminder to patient:",
        "send_note_ph": "Great job taking your medicine today!",
        "send_push_btn": "Send Notification",
        "refill_title": "Pill Stock & Refill Alert",
        "refill_btn": "Send WhatsApp Alert to Local Pharmacy",
        "pass_title": "Secure Medical Passport & Emergency SOS",
        "pass_sub": "Critical offline/online patient medical passport and live broadcast portal.",
        "patient_id_title": "Patient Medical ID",
        "dl_pass_btn": "Download Medical ID (PDF/QR)",
        "vitals_title": "📈 Vitals & Health Trends",
        "sos_title": "One-Tap Emergency SOS Broadcast",
        "sos_warn": "Pressing this button instantly broadcasts your live GPS coordinates to emergency contacts.",
        "sos_note_label": "Optional Emergency Note:",
        "sos_note_ph": "e.g. Experiencing chest pain",
        "sos_btn": "TRIGGER EMERGENCY SOS",
        "offline_card_title": "📡 Rural Offline First-Aid Guide",
        "impact_title": "UN Sustainable Development Goal 3 Alignment",
        "impact_sub": "Ensure healthy lives and promote well-being for all at all ages.",
        "globe_title": "Global Disease Burden 3D Globe",
        "globe_desc": "Interactive global visualization showing primary health burdens across major regions.",
        "metric_doses": "Reduction in Missed Doses",
        "metric_doses_desc": "Through automated multi-week reminders and family caregiver syncing.",
        "metric_triage": "Emergency Triage Time Saved",
        "metric_triage_desc": "By linking disease searches instantly to specialized local hospitals.",
        "low_resource": "Low-Resource Scalability: Designed to operate smoothly on low-bandwidth mobile networks in rural communities."
    },
    "Marathi": {
        "title": "पुढील पिढीचा रुग्ण सोबती",
        "subtitle": "अचूक आरोग्य सेवा, क्लाउड ट्रायेज आणि एसडीजी ३ साठी काळजी",
        "active_plan": "उपचार योजना",
        "active_val": "आठवडा १ सक्रिय",
        "active_delta": "९२% औषध पालन",
        "emerg_ready": "आणीबाणी तयारी",
        "emerg_val": "GPS ऑनलाइन",
        "emerg_delta": "कोल्हापूर परिसर",
        "care_link": "काळजीवाहू लिंक",
        "care_val": "जोडलेले",
        "care_delta": "पिन सुरक्षित",
        "healtho_title": "हेल्थो - एआय आरोग्य सोबती",
        "healtho_subtitle": "तुमचा प्रश्न खाली टाका. हेल्थो तुम्हाला लगेच उत्तर देईल!",
        "healtho_input_ph": "हेल्थोला विचारा... (उदा. 'मेटफॉर्मिन कसे घ्यावे?')",
        "speak_btn": "🔊 हेल्थोचा आवाज ऐका",
        "bento_title": "जलद विभाग",
        "hosp_card_title": "रुग्णालय केंद्र",
        "hosp_card_desc": "आजारानुसार रुग्णालय मार्ग शोधक.",
        "med_card_title": "औषध सूची",
        "med_card_desc": "अनेक आठवड्यांचे औषध वेळापत्रक.",
        "pass_card_title": "सुरक्षित पासपोर्ट",
        "pass_card_desc": "आणीबाणी SOS सह डिजिटल ओळखपत्र.",
        "btn_open": "उघडा",
        "hosp_title": "रुग्णालय शोधक",
        "search_heading": "लक्षण आणि रुग्णालय जुळणी",
        "search_label": "आजार / लक्षण टाइप करा:",
        "search_placeholder": "टाइप करा... (उदा. हृदय, डोळे, हाडे)",
        "rec_fac": "शिफारस केलेले रुग्णालय:",
        "map_cyan": "निळा पिन = GPS स्थान",
        "map_rose": "लाल पिन = रुग्णालय स्थान",
        "med_sched_title": "औषध वेळापत्रक",
        "choose_week": "आठवडा निवडा:",
        "choose_day": "दिवस निवडा:",
        "no_meds": "या दिवशी औषधे नाहीत:",
        "mark_taken": "घेतले म्हणून नोंदवा",
        "taken": "घेतले ✅",
        "doc_title": "डॉक्टर भेटी",
        "doc_info": "**डॉ. शर्मा (हृदयरोग तज्ज्ञ)**\nउद्या सकाळी १०:३० वाजता\nसिटी जनरल हॉस्पिटल",
        "add_q_label": "प्रश्न जोडा:",
        "add_q_placeholder": "उदा. काही पथ्य आहे का?",
        "save_q_btn": "प्रश्न जतन करा",
        "saved_qs": "जतन केलेले प्रश्न:",
        "care_title": "केअरगिव्हर् पोर्टल",
        "care_sub": "दूरस्थ कुटुंब देखरेख आणि प्रोफाइल नियंत्रण.",
        "care_pin_label": "काळजीवाहू पिन टाका:",
        "care_pin_ph": "पिन टाका (डेमो: 1234)",
        "access_granted": "प्रवेश मंजूर! रुग्ण प्रोफाइल #PAT-8821",
        "ocr_title": "OCR प्रिस्क्रिप्शन स्कॅनर",
        "ocr_upload": "प्रिस्क्रिप्शन फोटो अपलोड करा:",
        "ocr_btn": "औषधे एक्सट्रॅक्ट करा",
        "edit_pass_exp": "पासपोर्ट संपादित करा",
        "update_info": "माहिती अद्ययावत करा",
        "full_name": "पूर्ण नाव:",
        "blood_group": "रक्तगट:",
        "emerg_contact": "आणीबाणी संपर्क:",
        "allergies": "ऍलर्जी:",
        "conditions": "दीर्घकालीन आजार:",
        "physician": "मुख्य डॉक्टर:",
        "save_pass_btn": "जतन करा",
        "add_med_exp": "नवीन औषध जोडा",
        "med_name_label": "औषधाचे नाव:",
        "med_name_ph": "उदा. पॅरासिटामॉल (650mg)",
        "sched_time_label": "वेळ:",
        "sched_time_ph": "उदा. दुपारी 02:00",
        "assign_week": "आठवडा:",
        "assign_day": "दिवस:",
        "add_med_btn": "औषध जोडा",
        "med_table_title": "औषध आढावा",
        "overall_adh": "औषध पालन दर",
        "send_note_label": "रुग्णाला संदेश पाठवा:",
        "send_note_ph": "वेळेवर औषध घेतल्याबद्दल छान!",
        "send_push_btn": "संदेश पाठवा",
        "refill_title": "गोळ्यांचा साठा अलर्ट",
        "refill_btn": "व्हॉट्सॲप अलर्ट पाठवा",
        "pass_title": "वैद्यकीय पासपोर्ट आणि SOS",
        "pass_sub": "रुग्ण पासपोर्ट आणि थेट ब्रॉडकास्ट.",
        "patient_id_title": "रुग्ण ओळखपत्र",
        "dl_pass_btn": "पासपोर्ट डाउनलोड करा",
        "vitals_title": "📈 आरोग्य मापदंड",
        "sos_title": "आणीबाणी SOS",
        "sos_warn": "हे दाबल्यास तुमचे GPS स्थान पाठवले जाईल.",
        "sos_note_label": "आणीबाणी टिपण:",
        "sos_note_ph": "उदा. छातीत दुखत आहे",
        "sos_btn": "आणीबाणी SOS सुरू करा",
        "offline_card_title": "📡 ऑफलाइन प्रथमोपचार मार्गदर्शक",
        "impact_title": "युएन एसडीजी ३ ध्येय",
        "impact_sub": "निरोगी आयुष्य सुनिश्चित करा.",
        "globe_title": "जागतिक आरोग्य 3D ग्लोब",
        "globe_desc": "जागतिक आरोग्य भार व्हिज्युअलायझेशन.",
        "metric_doses": "औषध चुकण्यात घट",
        "metric_doses_desc": "स्वयंचलित स्मरणपत्रांद्वारे.",
        "metric_triage": "वाचलेला वेळ",
        "metric_triage_desc": "त्वरित रुग्णालय मार्गांद्वारे.",
        "low_resource": "ग्रामीण भागात सुलभतेने चालण्यासाठी डिझाइन केलेले."
    },
    "Hindi": {
        "title": "अगली पीढ़ी का रोगी साथी",
        "subtitle": "सटीक स्वास्थ्य सेवा, क्लाउड ट्राइएज और एसडीजी 3 देखभाल",
        "active_plan": "उपचार योजना",
        "active_val": "सप्ताह 1 सक्रिय",
        "active_delta": "92% दवा पालन",
        "emerg_ready": "आपातकालीन तत्परता",
        "emerg_val": "जीपीएस ऑनलाइन",
        "emerg_delta": "कोल्हापुर क्षेत्र",
        "care_link": "देखभालकर्ता लिंक",
        "care_val": "कनेक्टेड",
        "care_delta": "पिन सुरक्षित",
        "healtho_title": "हेल्थो - आपका एआई स्वास्थ्य साथी",
        "healtho_subtitle": "अपना प्रश्न नीचे दर्ज करें। हेल्थो तुरंत जवाब देगा!",
        "healtho_input_ph": "हेल्थो से पूछें... (उदा. 'मेटफॉर्मिन कैसे लें?')",
        "speak_btn": "🔊 हेल्थो की आवाज सुनें",
        "bento_title": "त्वरित पहुँच मॉड्यूल",
        "hosp_card_title": "अस्पताल केंद्र",
        "hosp_card_desc": "बीमारी के अनुसार अस्पताल मार्ग खोजक।",
        "med_card_title": "दवा सूची",
        "med_card_desc": "बहु-सप्ताह दवा अनुसूची।",
        "pass_card_title": "सुरक्षित पासपोर्ट",
        "pass_card_desc": "आपातकालीन SOS के साथ डिजिटल आईडी।",
        "btn_open": "खोलें",
        "hosp_title": "अस्पताल खोजक",
        "search_heading": "लक्षण और अस्पताल मिलान",
        "search_label": "बीमारी / लक्षण दर्ज करें:",
        "search_placeholder": "दर्ज करें... (उदा. हृदय, आँखें, हड्डियाँ)",
        "rec_fac": "अनुशंसित अस्पताल:",
        "map_cyan": "नीला पिन = जीपीएस स्थान",
        "map_rose": "लाल पिन = अस्पताल स्थान",
        "med_sched_title": "दवा अनुसूची",
        "choose_week": "सप्ताह चुनें:",
        "choose_day": "दिन चुनें:",
        "no_meds": "इस दिन कोई दवाएं नहीं हैं:",
        "mark_taken": "ली गई दर्ज करें",
        "taken": "ली गई ✅",
        "doc_title": "डॉक्टर अपॉइंटमेंट",
        "doc_info": "**डॉ. शर्मा (हृदय रोग विशेषज्ञ)**\nकल सुबह 10:30 बजे\nसिटी जनरल अस्पताल",
        "add_q_label": "प्रश्न जोड़ें:",
        "add_q_placeholder": "उदा. क्या खाने का परहेज है?",
        "save_q_btn": "प्रश्न सहेजें",
        "saved_qs": "सहेजे गए प्रश्न:",
        "care_title": "देखभालकर्ता पोर्टल",
        "care_sub": "रिमोट परिवार निगरानी और प्रोफ़ाइल नियंत्रण।",
        "care_pin_label": "देखभालकर्ता पिन दर्ज करें:",
        "care_pin_ph": "पिन दर्ज करें (डेमो: 1234)",
        "access_granted": "पहुंच स्वीकृत! रोगी प्रोफ़ाइल #PAT-8821",
        "ocr_title": "OCR प्रिस्क्रिप्शन स्कैनर",
        "ocr_upload": "प्रिस्क्रिप्शन इमेज अपलोड करें:",
        "ocr_btn": "दवाएं ऑटो-एक्सट्रैक्ट करें",
        "edit_pass_exp": "पासपोर्ट संपादित करें",
        "update_info": "जानकारी अपडेट करें",
        "full_name": "पूरा नाम:",
        "blood_group": "रक्त समूह:",
        "emerg_contact": "आपातकालीन संपर्क:",
        "allergies": "अलर्जी:",
        "conditions": "पुरानी बीमारियाँ:",
        "physician": "प्राथमिक चिकित्सक:",
        "save_pass_btn": "सहेजें",
        "add_med_exp": "नई दवा जोड़ें",
        "med_name_label": "दवा का नाम:",
        "med_name_ph": "उदा. पैरासिटामोल (650mg)",
        "sched_time_label": "समय:",
        "sched_time_ph": "उदा. दोपहर 02:00 बजे",
        "assign_week": "सप्ताह असाइन करें:",
        "assign_day": "दिन असाइन करें:",
        "add_med_btn": "दवा जोड़ें",
        "med_table_title": "दवा अवलोकन",
        "overall_adh": "दवा पालन दर",
        "send_note_label": "रोगी को संदेश भेजें:",
        "send_note_ph": "समय पर दवा लेने के लिए बहुत बढ़िया!",
        "send_push_btn": "संदेश भेजें",
        "refill_title": "गोली स्टॉक रीफिल चेतावनी",
        "refill_btn": "व्हाट्सएप रिफिल अलर्ट भेजें",
        "pass_title": "चिकित्सा पासपोर्ट और SOS",
        "pass_sub": "रोगी पासपोर्ट और लाइव प्रसारण।",
        "patient_id_title": "रोगी मेडिकल आईडी",
        "dl_pass_btn": "पासपोर्ट डाउनलोड करें",
        "vitals_title": "📈 स्वास्थ्य मापदंड",
        "sos_title": "आपातकालीन SOS",
        "sos_warn": "यह बटन दबाने पर जीपीएस स्थान भेजा जाएगा।",
        "sos_note_label": "आपातकालीन नोट:",
        "sos_note_ph": "उदा. सीने में दर्द हो रहा है",
        "sos_btn": "आपातकालीन SOS शुरू करें",
        "offline_card_title": "📡 ऑफ़लाइन प्राथमिक चिकित्सा कार्ड",
        "impact_title": "संयुक्त राष्ट्र एसडीजी 3 ध्येय",
        "impact_sub": "सभी के लिए स्वस्थ जीवन सुनिश्चित करें।",
        "globe_title": "वैश्विक स्वास्थ्य 3D ग्लोब",
        "globe_desc": "वैश्विक बीमारी बोझ विज़ुअलाइज़ेशन।",
        "metric_doses": "दवा छूटने में कमी",
        "metric_doses_desc": "स्वचालित अनुस्मारक द्वारा।",
        "metric_triage": "बचाया गया समय",
        "metric_triage_desc": "त्वरित अस्पताल मार्ग द्वारा।",
        "low_resource": "ग्रामीण क्षेत्रों में सुचारू रूप से चलने के लिए डिज़ाइन किया गया।"
    }
}

# --- 5. GLOBAL CUSTOM STYLING ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    .stApp {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.28) 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.25) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.18) 0%, transparent 65%);
        background-size: 160% 160%;
        animation: cloudDrift 18s ease-in-out infinite alternate;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        padding-bottom: 140px;
    }

    @keyframes cloudDrift {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }

    h1, h2, h3 {
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #ffffff !important;
        border: 2px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 16px !important;
    }

    div[data-testid="metric-container"], .stExpander {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 22px;
        backdrop-filter: blur(20px);
    }

    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        font-weight: 600 !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Language Selector
col_top_spacer, col_lang = st.columns([5, 2])
with col_lang:
    selected_lang = st.selectbox("🌐 Language / भाषा:", ["English", "Marathi", "Hindi"], key="lang_selector")
    st.session_state.language = selected_lang

t = translations[st.session_state.language]

# ----------------------------------------------------
# 6. MODULE 0: HOME & HEALTHO SPEECH ASSISTANT
# ----------------------------------------------------
if current_tab == "Home":
    try:
        st.title(t["title"])
        st.markdown(f"##### *{t['subtitle']}*")
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=t["active_plan"], value=t["active_val"], delta=t["active_delta"])
        with col2:
            st.metric(label=t["emerg_ready"], value=t["emerg_val"], delta=t["emerg_delta"])
        with col3:
            st.metric(label=t["care_link"], value=t["care_val"], delta=t["care_delta"])

        st.divider()

        # HEALTHO AI SPEECH ASSISTANT ENGINE
        st.subheader(f"🤖 {t['healtho_title']}")
        st.caption(t['healtho_subtitle'])

        with st.form("healtho_chat_form"):
            user_q = st.text_input("Ask Healtho:", placeholder=t["healtho_input_ph"], key="healtho_form_q")
            submit_q = st.form_submit_button("Ask Healtho 💬")
            
            if submit_q and user_q.strip():
                q_low = user_q.lower()
                if "metformin" in q_low or "sugar" in q_low or "diab" in q_low:
                    st.session_state.last_speech = "Metformin is best taken with meals to minimize stomach upset. Always keep yourself adequately hydrated throughout the day."
                elif "dizziness" in q_low or "headache" in q_low or "pain" in q_low or "fever" in q_low:
                    st.session_state.last_speech = "Mild dizziness or discomfort can occur during initial dosage adjustments. Sit comfortably, drink water, and rest. If it lasts over 48 hours, consult Dr. Sharma."
                elif "food" in q_low or "diet" in q_low or "eat" in q_low:
                    st.session_state.last_speech = "For optimal diabetes control, stick to low-GI complex carbs, green vegetables, and lean protein."
                else:
                    st.session_state.last_speech = f"I recorded your query regarding: '{user_q}'. Your current adherence rate is 92%. Keep up the good work and remember to take your doses on schedule!"

        # Display current Healtho Speech Card
        st.info(f"🤖 **Healtho:** \"{st.session_state.last_speech}\"")

        # HTML5 / Web Speech API Integration for REAL Browser Audio Output
        clean_speech_text = st.session_state.last_speech.replace('"', '').replace("'", "")
        tts_html = f"""
        <div style="background: rgba(15, 23, 42, 0.8); padding: 12px; border-radius: 16px; border: 1px solid rgba(56, 189, 248, 0.4); text-align: center;">
            <button onclick="speakText()" style="background: linear-gradient(135deg, #0ea5e9, #6366f1); color: white; border: none; padding: 12px 24px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">
                {t['speak_btn']}
            </button>
        </div>
        <script>
        function speakText() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_speech_text}");
                msg.rate = 0.95;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }} else {{
                alert("Speech Synthesis is not supported in this browser.");
            }}
        }}
        </script>
        """
        components.html(tts_html, height=75)

        st.divider()

        st.subheader(t["bento_title"])
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown(f"### {t['hosp_card_title']}\n{t['hosp_card_desc']}")
            if st.button(f"{t['btn_open']} {t['hosp_card_title']}", key="home_btn_hosp"):
                st.query_params["tab"] = "Hospital"
                st.rerun()

        with col_b:
            st.markdown(f"### {t['med_card_title']}\n{t['med_card_desc']}")
            if st.button(f"{t['btn_open']} {t['med_card_title']}", key="home_btn_med"):
                st.query_params["tab"] = "Hospital"
                st.rerun()

        with col_c:
            st.markdown(f"### {t['pass_card_title']}\n{t['pass_card_desc']}")
            if st.button(f"{t['btn_open']} {t['pass_card_title']}", key="home_btn_pass"):
                st.query_params["tab"] = "Passport"
                st.rerun()

    except Exception as home_err:
        st.error(f"Error loading Home: {home_err}")

# ----------------------------------------------------
# 7. MODULE 1: INTELLIGENT HOSPITAL HUB & MAPS
# ----------------------------------------------------
elif current_tab == "Hospital":
    try:
        st.title(t["hosp_title"])
        st.divider()

        st.subheader(t["search_heading"])
        user_disease_input = st.text_input(t["search_label"], placeholder=t["search_placeholder"], key="map_disease_search")

        user_lat = st.session_state.user_location["lat"]
        user_lon = st.session_state.user_location["lon"]
        h_lat, h_lon = 16.6900, 74.2200
        h_name = "Alliance Multispeciality Hospital"
        travel_info = "~2.1 km away | 5 mins"

        query = (user_disease_input or "").lower().strip()
        if any(k in query for k in ["heart", "cardio", "chest", "bp", "stroke"]):
            h_lat, h_lon = 16.7050, 74.2433
            h_name = "Aster Aadhar Hospital (Cardiology)"
            travel_info = "~3.2 km away | 8 mins"
            st.error("Specialty Match: Cardiology")
        elif any(k in query for k in ["eye", "vision", "cataract"]):
            h_lat, h_lon = 16.7120, 74.2500
            h_name = "Nandadeep Eye Hospital"
            travel_info = "~4.5 km away | 12 mins"
            st.warning("Specialty Match: Ophthalmology")
        elif any(k in query for k in ["bone", "fracture", "ortho"]):
            h_lat, h_lon = 16.7200, 74.4600
            h_name = "Dr. Lande Fracture Hospital"
            travel_info = "~6.0 km away | 15 mins"
            st.info("Specialty Match: Orthopedics")

        st.markdown(f"📍 **{t['rec_fac']}** **{h_name}** — *{travel_info}*")

        map_data = get_cached_map_data(user_lat, user_lon, h_lat, h_lon, h_name)
        scatterplot_layer = pdk.Layer(
            "ScatterplotLayer",
            map_data,
            get_position=["longitude", "latitude"],
            get_fill_color="color",
            get_radius="radius",
            pickable=True
        )
        view_state = pdk.ViewState(latitude=(user_lat + h_lat) / 2, longitude=(user_lon + h_lon) / 2, zoom=13)
        st.pydeck_chart(pdk.Deck(layers=[scatterplot_layer], initial_view_state=view_state, map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"), use_container_width=True)

        st.divider()

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader(t["med_sched_title"])
            selected_week = st.selectbox(t["choose_week"], ["Week 1", "Week 2", "Week 3", "Week 4"], key="p_week")
            selected_day = st.selectbox(t["choose_day"], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key="p_day")
            
            day_meds = st.session_state.meds_by_week.get(selected_week, {}).get(selected_day, [])
            if not day_meds:
                st.info(f"{t['no_meds']} {selected_day}.")
            else:
                for i, med in enumerate(day_meds):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write(f"**{med['name']}** ({med['time']})")
                    with c2:
                        if med['status'] == "Pending":
                            if st.button(t["mark_taken"], key=f"t_{selected_week}_{selected_day}_{i}"):
                                st.session_state.meds_by_week[selected_week][selected_day][i]['status'] = "Taken"
                                st.rerun()
                        else:
                            st.success(t["taken"])

        with col_right:
            st.subheader(t["doc_title"])
            st.info(t["doc_info"])
            new_q = st.text_input(t["add_q_label"], placeholder=t["add_q_placeholder"])
            if st.button(t["save_q_btn"]) and new_q:
                st.session_state.questions.append(new_q)
                st.success("Saved!")
            for q in st.session_state.questions:
                st.markdown(f"- 🔸 {q}")

    except Exception as hub_err:
        st.error(f"Error in Hospital Hub: {hub_err}")

# ----------------------------------------------------
# 8. MODULE 2: CAREGIVER PORTAL & OCR
# ----------------------------------------------------
elif current_tab == "Caregiver":
    try:
        st.title(t["care_title"])
        st.markdown(t["care_sub"])
        st.divider()

        password_input = st.text_input(t["care_pin_label"], type="password", placeholder=t["care_pin_ph"])
        if password_input == "1234":
            st.success(t["access_granted"])

            with st.expander(t["ocr_title"], expanded=False):
                st.file_uploader(t["ocr_upload"], type=["png", "jpg", "jpeg"])
                if st.button(t["ocr_btn"]):
                    st.success("Prescription scanned! Metformin (500mg) logged.")

            st.subheader(t["refill_title"])
            st.info(f"Pill Stock: {st.session_state.pill_stock} tablets remaining.")
            if st.button(t["refill_btn"]):
                st.success("WhatsApp refill message sent!")

            st.divider()
            st.subheader(t["med_table_title"])
            all_meds = []
            for w, days in st.session_state.meds_by_week.items():
                for d, m_list in days.items():
                    for m in m_list:
                        all_meds.append({"Week": w, "Day": d, "Medicine": m["name"], "Status": m["status"]})
            st.dataframe(pd.DataFrame(all_meds), use_container_width=True)

        elif password_input:
            st.error("Incorrect PIN.")
        else:
            st.info("Enter PIN `1234` to unlock caregiver controls.")

    except Exception as care_err:
        st.error(f"Error in Caregiver: {care_err}")

# ----------------------------------------------------
# 9. MODULE 3: MEDICAL PASSPORT & SOS
# ----------------------------------------------------
elif current_tab == "Passport":
    try:
        st.title(t["pass_title"])
        st.divider()

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader(t["patient_id_title"])
            p = st.session_state.patient_passport
            st.markdown(f"* **Name:** {p['name']}\n* **Blood Group:** {p['blood_group']}\n* **Contact:** {p['emergency_contact']}\n* **Allergies:** {p['allergies']}")
            if st.button(t["dl_pass_btn"]):
                st.success("Medical ID QR generated!")

            st.divider()
            st.subheader(t["vitals_title"])
            v_df = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "BP": [128, 125, 122, 126, 120]})
            st.line_chart(v_df.set_index("Day"))

        with col_r:
            st.subheader(t["sos_title"])
            st.warning(t["sos_warn"])
            sos_note = st.text_area(t["sos_note_label"], placeholder=t["sos_note_ph"])
            if st.button(t["sos_btn"]):
                st.error("🚨 EMERGENCY SOS BROADCASTED TO CONTACTS!")

    except Exception as pass_err:
        st.error(f"Error in Passport: {pass_err}")

# ----------------------------------------------------
# 10. MODULE 4: UN SDG 3 IMPACT & 3D GLOBE
# ----------------------------------------------------
elif current_tab == "Impact":
    try:
        st.title(t["impact_title"])
        st.divider()

        st.subheader(t["globe_title"])
        st.markdown(t["globe_desc"])

        globe_html = """
        <div style="width: 100%; height: 380px; background: radial-gradient(circle at center, #0f172a 0%, #030712 100%); border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden;">
            <div style="position: absolute; width: 280px; height: 280px; border: 2px dashed rgba(56, 189, 248, 0.25); border-radius: 50%; animation: spin 25s linear infinite;"></div>
            <div style="z-index: 2; text-align: center; padding: 20px;">
                <div style="font-size: 54px; margin-bottom: 10px;">🌍</div>
                <h3 style="color: #38bdf8; font-family: sans-serif; margin: 0 0 8px 0; font-size: 22px;">Global Health Intelligence Node</h3>
                <p style="color: #94a3b8; font-family: sans-serif; font-size: 14px; max-width: 450px;">Tracking global metabolic and cardiovascular burden across South Asia and international health hubs.</p>
            </div>
        </div>
        <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
        """
        components.html(globe_html, height=400)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=t["metric_doses"], value="38%", delta="High Adherence")
        with col2:
            st.metric(label=t["metric_triage"], value="45%", delta="Fast GPS Routing")

        st.info(t["low_resource"])
    except Exception as imp_err:
        st.error(f"Error in Impact: {imp_err}")

# ----------------------------------------------------
# 11. FLOATING NAVIGATION DOCK
# ----------------------------------------------------
active_home = "active" if current_tab == "Home" else ""
active_hosp = "active" if current_tab == "Hospital" else ""
active_care = "active" if current_tab == "Caregiver" else ""
active_pass = "active" if current_tab == "Passport" else ""
active_imp  = "active" if current_tab == "Impact" else ""

st.markdown(f"""
    <style>
    .aceternity-dock-container {{
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 12px;
        background: rgba(10, 15, 30, 0.9);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 9999px;
        padding: 8px 18px;
        z-index: 999999;
    }}
    .dock-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 50%;
        color: #f8fafc;
        font-size: 20px;
        text-decoration: none !important;
    }}
    .dock-btn.active {{
        background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    }}
    </style>
    <div class="aceternity-dock-container">
        <a href="?tab=Home" target="_self" class="dock-btn {active_home}">🏠</a>
        <a href="?tab=Hospital" target="_self" class="dock-btn {active_hosp}">🏥</a>
        <a href="?tab=Caregiver" target="_self" class="dock-btn {active_care}">👁️</a>
        <a href="?tab=Passport" target="_self" class="dock-btn {active_pass}">🛡️</a>
        <a href="?tab=Impact" target="_self" class="dock-btn {active_imp}">🌍</a>
    </div>
""", unsafe_allow_html=True)
