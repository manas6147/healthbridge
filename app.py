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

# Read active tab from URL query params (defaults to "Home")
current_tab = st.query_params.get("tab", "Home")
if isinstance(current_tab, list):
    current_tab = current_tab[0]

# --- 2. HIGH-PERFORMANCE DATA CACHING ---
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
            {"msg": "HealthBridge Aceternity Master Edition initialized.", "time": "System Init"}
        ]

    if "meds_by_week" not in st.session_state:
        st.session_state.meds_by_week = get_default_schedule()

    if "questions" not in st.session_state:
        st.session_state.questions = ["Are there any food restrictions with this dosage?"]

    if "language" not in st.session_state:
        st.session_state.language = "English"

    if "pill_stock" not in st.session_state:
        st.session_state.pill_stock = 4  # Low stock demo trigger

except Exception as init_error:
    st.error(f"Initialization Notice: {init_error}")

# --- 4. FULL MULTILINGUAL TRANSLATIONS DICTIONARY ---
translations = {
    "English": {
        "title": "Next-Gen Patient Companion",
        "subtitle": "Precision Healthcare, Atmospheric Cloud Triage & Family Caregiving for SDG 3",
        "active_plan": "Active Treatment Plan",
        "active_val": "Week 1 Active",
        "active_delta": "92% Dose Adherence",
        "emerg_ready": "Emergency Readiness",
        "emerg_val": "GPS Online",
        "emerg_delta": "Kolhapur Region",
        "care_link": "Caregiver Link",
        "care_val": "Connected 🔒",
        "care_delta": "PIN Protected",
        "ai_title": "🤖 HealthBridge AI Triage & Drug Safety Checker",
        "ai_prompt": "Enter or speak any new symptom or medication to check for potential side-effects or clinical warnings:",
        "ai_input_label": "Describe symptom or drug name:",
        "ai_placeholder": "e.g., Mild dizziness after taking Metformin",
        "ai_btn": "Run AI Safety Check",
        "ai_res": "💡 **AI Triage Analysis:** Mild side-effects can occur during initial adjustment phases. Ensure adequate hydration. *Disclaimer: Consult Dr. Sharma if symptoms persist beyond 48 hours.*",
        "voice_btn": "🎙️ Speak Symptom (Voice Input)",
        "summary_title": "📋 Printable Doctor Visit Summary",
        "summary_btn": "Generate Downloadable Clinical PDF Report",
        "summary_success": "✅ Clinical summary package compiled successfully! Ready for printing or export to clinic database.",
        "bento_title": "Quick Access Bento Modules",
        "hosp_card_title": "Hospital Hub",
        "hosp_card_desc": "Intelligent disease-to-hospital routing with dynamic dark-mode PyDeck maps.",
        "med_card_title": "Medication Suite",
        "med_card_desc": "Multi-week medication schedules, independent daily resets, and smart categorization.",
        "pass_card_title": "Secure Passport",
        "pass_card_desc": "Digital Medical ID with single-tap emergency SOS broadcasting.",
        "btn_open": "Open",
        # Hospital Tab
        "hosp_title": "Intelligent Hospital Finder & Schedule",
        "search_heading": "Smart Symptom & Hospital Match",
        "search_label": "Type condition / symptom:",
        "search_placeholder": "Type condition here... (e.g., Heart, Eye, Bones)",
        "rec_fac": "Recommended Facility:",
        "map_cyan": "🔵 Cyan Pin = Live GPS Location",
        "map_rose": "🔴 Rose Pin = Recommended Specialized Hospital",
        "med_sched_title": "Multi-Week Medication Schedule",
        "choose_week": "Choose Treatment Week:",
        "choose_day": "Choose Day of Week:",
        "no_meds": "No medications scheduled for",
        "mark_taken": "Mark Taken",
        "taken": "Taken ✅",
        "doc_title": "Doctor Appointments & Questions",
        "doc_info": "**Dr. Sharma (Cardiologist)**\n📅 Tomorrow at 10:30 AM\n📍 City General Hospital",
        "add_q_label": "Add a question for your doctor:",
        "add_q_placeholder": "e.g. Any food restrictions?",
        "save_q_btn": "Save Question",
        "saved_qs": "Your Saved Questions:",
        # Caregiver Tab
        "care_title": "Caregiver Prescription & Profile Manager",
        "care_sub": "Secure portal for remote family monitoring, prescription assignment, and Medical Passport edits.",
        "care_pin_label": "🔒 Enter Caregiver Access PIN:",
        "care_pin_ph": "Enter PIN (Demo PIN: 1234)",
        "access_granted": "🔓 Access Granted! Connected to Patient Profile #PAT-8821",
        "ocr_title": "📷 OCR Prescription & Lab Report Scanner",
        "ocr_upload": "Upload handwritten prescription or lab report image:",
        "ocr_btn": "Extract & Auto-Log Medications",
        "edit_pass_exp": "📝 Edit Patient Medical Passport Details",
        "update_info": "Update Patient Information",
        "full_name": "Full Legal Name:",
        "blood_group": "Blood Group:",
        "emerg_contact": "Emergency Contact:",
        "allergies": "Known Allergies:",
        "conditions": "Chronic Conditions:",
        "physician": "Primary Physician:",
        "save_pass_btn": "Save Passport Updates",
        "add_med_exp": "➕ Add New Medication to Schedule",
        "med_name_label": "Medicine Name & Dosage:",
        "med_name_ph": "e.g., Paracetamol (650mg)",
        "sched_time_label": "Scheduled Time:",
        "sched_time_ph": "e.g., 02:00 PM",
        "assign_week": "Assign to Week:",
        "assign_day": "Assign to Day of Week:",
        "add_med_btn": "Add Medication",
        "med_table_title": "Multi-Week Prescriptions Overview",
        "overall_adh": "Overall Patient Adherence Rate",
        "send_note_label": "Send an encouraging note or reminder to patient:",
        "send_note_ph": "Dad, great job taking your medicine today!",
        "send_push_btn": "Send Push Notification",
        "refill_title": "💊 Pill Refill & Pharmacy Alert",
        "refill_btn": "📲 Trigger WhatsApp Refill Alert to Pharmacy",
        # Passport Tab
        "pass_title": "Secure Medical Passport & Emergency SOS",
        "pass_sub": "Critical offline/online patient medical passport and live broadcast portal.",
        "patient_id_title": "Patient Medical ID",
        "dl_pass_btn": "Download Secure Medical ID (PDF/QR)",
        "vitals_title": "📈 Patient Vitals & Health Trends",
        "sos_title": "One-Tap Emergency SOS Broadcast",
        "sos_warn": "Pressing this button instantly broadcasts your live GPS coordinates to emergency contacts.",
        "sos_note_label": "Optional Emergency Note:",
        "sos_note_ph": "e.g., Experiencing chest pain, need immediate assistance.",
        "sos_btn": "TRIGGER EMERGENCY SOS",
        "offline_card_title": "📡 Rural Offline Emergency First-Aid",
        # Impact Tab
        "impact_title": "UN Sustainable Development Goal 3 Alignment",
        "impact_sub": "Ensure healthy lives and promote well-being for all at all ages.",
        "globe_title": "🌐 Global Disease Burden 3D Globe",
        "globe_desc": "Interactive global visualization showing primary health burdens and case volumes across major regions.",
        "metric_doses": "Projected Reduction in Missed Doses",
        "metric_doses_desc": "Through intelligent automated multi-week reminders and family caregiver prescription syncing.",
        "metric_triage": "Emergency Triage Time Saved",
        "metric_triage_desc": "By linking disease searches instantly to specialized local hospitals and utilizing real-time GPS coordinates.",
        "low_resource": "Low-Resource Scalability: Designed to operate smoothly on low-bandwidth mobile networks in rural communities."
    },
    "Marathi": {
        "title": "पुढील पिढीचा रुग्ण सोबती",
        "subtitle": "अचूक आरोग्य सेवा, क्लाउड ट्रायेज आणि एसडीजी ३ साठी कुटुंब काळजी",
        "active_plan": "सक्रिय उपचार योजना",
        "active_val": "आठवडा १ सक्रिय",
        "active_delta": "९२% औषध पालन",
        "emerg_ready": "आणीबाणीची तयारी",
        "emerg_val": "GPS ऑनलाइन",
        "emerg_delta": "कोल्हापूर परिसर",
        "care_link": "काळजीवाहू लिंक",
        "care_val": "जोडलेले 🔒",
        "care_delta": "पिन सुरक्षित",
        "ai_title": "🤖 हेल्थब्रिज एआय तपासणी आणि औषध सुरक्षा",
        "ai_prompt": "दुष्परिणाम किंवा इशारे तपासण्यासाठी नवीन लक्षण किंवा औषध टाका किंवा बोला:",
        "ai_input_label": "लक्षण किंवा औषधाचे नाव सांगा:",
        "ai_placeholder": "उदा. मेटफॉर्मिन घेतल्यानंतर हलकी चक्कर येणे",
        "ai_btn": "एआय सुरक्षा तपासणी करा",
        "ai_res": "💡 **एआय विश्लेषण:** सुरुवातीच्या काळात सौम्य दुष्परिणाम होऊ शकतात. भरपूर पाणी प्या. *टीप: लक्षणे ४८ तासांपेक्षा जास्त राहिल्यास डॉक्टरांचा सल्ला घ्या.*",
        "voice_btn": "🎙️ लक्षण बोला (आवाज इनपुट)",
        "summary_title": "📋 डॉक्टर भेटीचा सारांश (प्रिंट करण्यायोग्य)",
        "summary_btn": "डाउनलोड करण्यायोग्य रिपोर्ट तयार करा",
        "summary_success": "✅ वैद्यकीय सारांश यशस्वीरीत्या तयार झाला! प्रिंट किंवा निर्यातीसाठी तयार.",
        "bento_title": "जलद प्रवेश विभाग",
        "hosp_card_title": "रुग्णालय केंद्र",
        "hosp_card_desc": "डायनॅमिक डार्क-मोड नकाशांसह बुद्धिमत्तापूर्ण आजार-ते-रुग्णालय मार्ग.",
        "med_card_title": "औषध सूची",
        "med_card_desc": "अनेक आठवड्यांचे औषध वेळापत्रक आणि स्मार्ट वर्गीकरण.",
        "pass_card_title": "सुरक्षित पासपोर्ट",
        "pass_card_desc": "सिंगल-टॅप आणीबाणी SOS सह डिजिटल वैद्यकीय ओळखपत्र.",
        "btn_open": "उघडा",
        # Hospital Tab
        "hosp_title": "हुशार रुग्णालय शोधक आणि वेळापत्रक",
        "search_heading": "स्मार्ट लक्षण आणि रुग्णालय जुळणी",
        "search_label": "आजार / लक्षण टाइप करा:",
        "search_placeholder": "येथे आजार टाइप करा... (उदा. हृदय, डोळे, हाडे)",
        "rec_fac": "शिफारस केलेले रुग्णालय:",
        "map_cyan": "🔵 निळा पिन = तुमचे थेट GPS स्थान",
        "map_rose": "🔴 लाल पिन = शिफारस केलेले विशेष रुग्णालय",
        "med_sched_title": "अनेक आठवड्यांचे औषध वेळापत्रक",
        "choose_week": "उपचार आठवडा निवडा:",
        "choose_day": "आठवड्याचा दिवस निवडा:",
        "no_meds": "या दिवशी कोणतीही औषधे नाहीत:",
        "mark_taken": "घेतले म्हणून नोंदवा",
        "taken": "घेतले ✅",
        "doc_title": "डॉक्टर भेटी आणि प्रश्न",
        "doc_info": "**डॉ. शर्मा (हृदयरोग तज्ज्ञ)**\n📅 उद्या सकाळी १०:३० वाजता\n📍 सिटी जनरल हॉस्पिटल",
        "add_q_label": "डॉक्टरांसाठी प्रश्न जोडा:",
        "add_q_placeholder": "उदा. अन्नाचे काही पथ्य आहे का?",
        "save_q_btn": "प्रश्न जतन करा",
        "saved_qs": "तुमचे जतन केलेले प्रश्न:",
        # Caregiver Tab
        "care_title": "केअरगिव्हर् प्रिस्क्रिप्शन आणि प्रोफाइल व्यवस्थापक",
        "care_sub": "दूरस्थ कुटुंब देखरेख, औषध वाटप आणि वैद्यकीय पासपोर्ट संपादनासाठी सुरक्षित पोर्टल.",
        "care_pin_label": "🔒 काळजीवाहू प्रवेश पिन टाका:",
        "care_pin_ph": "पिन टाका (डेमो पिन: 1234)",
        "access_granted": "🔓 प्रवेश मंजूर! रुग्ण प्रोफाइल #PAT-8821 शी जोडलेले",
        "ocr_title": "📷 OCR प्रिस्क्रिप्शन आणि रिपोर्ट स्कॅनर",
        "ocr_upload": "हस्ताक्षरित प्रिस्क्रिप्शन किंवा लॅब रिपोर्ट अपलोड करा:",
        "ocr_btn": "औषधे ऑटो-एक्सट्रॅक्ट करा",
        "edit_pass_exp": "📝 रुग्णाच्या पासपोर्टची माहिती संपादित करा",
        "update_info": "रुग्णाची माहिती अद्ययावत करा",
        "full_name": "पूर्ण नाव:",
        "blood_group": "रक्तगट:",
        "emerg_contact": "आणीबाणी संपर्क:",
        "allergies": "माहित असलेल्या ऍलर्जी:",
        "conditions": "दीर्घकालीन आजार:",
        "physician": "मुख्य डॉक्टर:",
        "save_pass_btn": "माहिती जतन करा",
        "add_med_exp": "➕ वेळापत्रकात नवीन औषध जोडा",
        "med_name_label": "औषधाचे नाव आणि प्रमाण:",
        "med_name_ph": "उदा. पॅरासिटामॉल (650mg)",
        "sched_time_label": "वेळ:",
        "sched_time_ph": "उदा. दुपारी 02:00",
        "assign_week": "आठवडा निवडा:",
        "assign_day": "दिवस निवडा:",
        "add_med_btn": "औषध जोडा",
        "med_table_title": "अनेक आठवड्यांचा औषध आढावा",
        "overall_adh": "एकूण रुग्ण औषध पालन दर",
        "send_note_label": "रुग्णाला संदेश किंवा आठवण पाठवा:",
        "send_note_ph": "बाबा, आज वेळेवर औषध घेतल्याबद्दल छान!",
        "send_push_btn": "संदेश पाठवा",
        "refill_title": "💊 गोळ्यांचा साठा आणि मेडिकल सूचना",
        "refill_btn": "📲 मेडिकल दुकानदाराला व्हॉट्सॲप मेसेज पाठवा",
        # Passport Tab
        "pass_title": "सुरक्षित वैद्यकीय पासपोर्ट आणि आणीबाणी SOS",
        "pass_sub": "ऑनलाइन/ऑफलाइन रुग्ण वैद्यकीय पासपोर्ट आणि थेट ब्रॉडकास्ट पोर्टल.",
        "patient_id_title": "रुग्ण वैद्यकीय ओळखपत्र",
        "dl_pass_btn": "वैद्यकीय पासपोर्ट डाउनलोड करा (PDF/QR)",
        "vitals_title": "📈 रुग्णाचे आरोग्य मापदंड आणि ट्रेंड",
        "sos_title": "एक-टॅप आणीबाणी SOS",
        "sos_warn": "हे बटण दाबल्यास तुमचे लाईव्ह GPS स्थान त्वरित संपर्क क्रमांकांना पाठवले जाईल.",
        "sos_note_label": "आणीबाणीची टिपण (पर्यायी):",
        "sos_note_ph": "उदा. छातीत दुखत आहे, त्वरित मदतीची गरज आहे.",
        "sos_btn": "आणीबाणी SOS सुरू करा",
        "offline_card_title": "📡 ग्रामीण भागासाठी ऑफलाइन प्रथमोपचार कार्ड",
        # Impact Tab
        "impact_title": "युएन शाश्वत विकास ध्येय ३ संलीकरण",
        "impact_sub": "सर्व वयोगटातील लोकांसाठी निरोगी आयुष्य सुनिश्चित करा आणि कल्याणाला चालना द्या.",
        "globe_title": "🌐 जागतिक आजार भार 3D ग्लोब",
        "globe_desc": "प्रमुख क्षेत्रांमधील प्रमुख आरोग्य भार आणि प्रकरणे दर्शवणारे परस्परसंवादी व्हिज्युअलायझेशन.",
        "metric_doses": "औषध चुकण्याच्या प्रमाणात अपेक्षित घट",
        "metric_doses_desc": "स्वयंचलित स्मरणपत्रे आणि कौटुंबिक काळजीवाहू सिंकद्वारे.",
        "metric_triage": "आणीबाणी उपचारात वाचलेला वेळ",
        "metric_triage_desc": "त्वरित रुग्णालय मार्ग आणि थेट GPS द्वारे.",
        "low_resource": "ग्रामीण भागात कमी इंटरनेट बँडविड्थवरही सुलभतेने चालण्यासाठी डिझाइन केलेले."
    },
    "Hindi": {
        "title": "अगली पीढ़ी का रोगी साथी",
        "subtitle": "सटीक स्वास्थ्य सेवा, क्लाउड ट्राइएज और एसडीजी 3 के लिए पारिवारिक देखभाल",
        "active_plan": "सक्रिय उपचार योजना",
        "active_val": "सप्ताह 1 सक्रिय",
        "active_delta": "92% दवा पालन",
        "emerg_ready": "आपातकालीन तत्परता",
        "emerg_val": "जीपीएस ऑनलाइन",
        "emerg_delta": "कोल्हापुर क्षेत्र",
        "care_link": "देखभालकर्ता लिंक",
        "care_val": "कनेक्टेड 🔒",
        "care_delta": "पिन सुरक्षित",
        "ai_title": "🤖 हेल्थब्रिज एआई लक्षण और दवा सुरक्षा चेकर",
        "ai_prompt": "संभावित दुष्प्रभावों या चेतावनियों की जांच के लिए कोई नया लक्षण या दवा दर्ज करें या बोलें:",
        "ai_input_label": "लक्षण या दवा का नाम बताएं:",
        "ai_placeholder": "उदा. मेटफॉर्मिन लेने के बाद हल्का चक्कर आना",
        "ai_btn": "एआई सुरक्षा जांच चलाएं",
        "ai_res": "💡 **एआई विश्लेषण:** शुरुआती समायोजन चरणों के दौरान हल्के दुष्प्रभाव हो सकते हैं। पर्याप्त पानी पिएं। *अस्वीकरण: यदि लक्षण 48 घंटे से अधिक बने रहते हैं तो डॉक्टर से परामर्श करें।*",
        "voice_btn": "🎙️ लक्षण बोलें (आवाज इनपुट)",
        "summary_title": "📋 डॉक्टर की मुलाक़ात का सारांश",
        "summary_btn": "डाउनलोड करने योग्य मेडिकल रिपोर्ट बनाएं",
        "summary_success": "✅ मेडिकल सारांश सफलतापूर्वक तैयार किया गया! प्रिंट या निर्यात के लिए तैयार।",
        "bento_title": "त्वरित पहुँच मॉड्यूल",
        "hosp_card_title": "अस्पताल केंद्र",
        "hosp_card_desc": "डायनामिक डार्क-मोड मानचित्रों के साथ बुद्धिमान बीमारी-से-अस्पताल मार्ग।",
        "med_card_title": "दवा सूची",
        "med_card_desc": "बहु-सप्ताह दवा अनुसूची और स्मार्ट वर्गीकरण।",
        "pass_card_title": "सुरक्षित पासपोर्ट",
        "pass_card_desc": "सिंगल-टैप आपातकालीन SOS के साथ डिजिटल मेडिकल आईडी।",
        "btn_open": "खोलें",
        # Hospital Tab
        "hosp_title": "इंटेलिजेंट अस्पताल खोजक और अनुसूची",
        "search_heading": "स्मार्ट लक्षण और अस्पताल मिलान",
        "search_label": "बीमारी / लक्षण दर्ज करें:",
        "search_placeholder": "यहाँ बीमारी दर्ज करें... (उदा. हृदय, आँखें, हड्डियाँ)",
        "rec_fac": "अनुशंसित अस्पताल:",
        "map_cyan": "🔵 नीला पिन = आपका लाइव जीपीएस स्थान",
        "map_rose": "🔴 लाल पिन = अनुशंसित विशेष अस्पताल",
        "med_sched_title": "बहु-सप्ताह दवा अनुसूची",
        "choose_week": "उपचार सप्ताह चुनें:",
        "choose_day": "सप्ताह का दिन चुनें:",
        "no_meds": "इस दिन कोई दवाएं निर्धारित नहीं हैं:",
        "mark_taken": "ली गई दर्ज करें",
        "taken": "ली गई ✅",
        "doc_title": "डॉक्टर के अपॉइंटमेंट और प्रश्न",
        "doc_info": "**डॉ. शर्मा (हृदय रोग विशेषज्ञ)**\n📅 कल सुबह 10:30 बजे\n📍 सिटी जनरल अस्पताल",
        "add_q_label": "डॉक्टर के लिए प्रश्न जोड़ें:",
        "add_q_placeholder": "उदा. क्या खाने का कोई परहेज है?",
        "save_q_btn": "प्रश्न सहेजें",
        "saved_qs": "आपके सहेजे गए प्रश्न:",
        # Caregiver Tab
        "care_title": "देखभाल करने वाला नुस्खा और प्रोफ़ाइल प्रबंधक",
        "care_sub": "रिमोट परिवार निगरानी, दवा असाइनमेंट और मेडिकल पासपोर्ट संपादन के लिए सुरक्षित पोर्टल।",
        "care_pin_label": "🔒 देखभालकर्ता एक्सेस पिन दर्ज करें:",
        "care_pin_ph": "पिन दर्ज करें (डेमो पिन: 1234)",
        "access_granted": "🔓 पहुंच स्वीकृत! रोगी प्रोफ़ाइल #PAT-8821 से जुड़ा हुआ",
        "ocr_title": "📷 OCR प्रिस्क्रिप्शन और लैब रिपोर्ट स्कैनर",
        "ocr_upload": "हस्ताक्षरित प्रिस्क्रिप्शन या लैब रिपोर्ट की छवि अपलोड करें:",
        "ocr_btn": "दवाएं ऑटो-एक्सट्रैक्ट करें",
        "edit_pass_exp": "📝 रोगी मेडिकल पासपोर्ट विवरण संपादित करें",
        "update_info": "रोगी की जानकारी अपडेट करें",
        "full_name": "पूरा नाम:",
        "blood_group": "रक्त समूह:",
        "emerg_contact": "आपातकालीन संपर्क:",
        "allergies": "ज्ञात एलर्जी:",
        "conditions": "पुरानी बीमारियाँ:",
        "physician": "प्राथमिक चिकित्सक:",
        "save_pass_btn": "पासपोर्ट अपडेट सहेजें",
        "add_med_exp": "➕ अनुसूची में नई दवा जोड़ें",
        "med_name_label": "दवा का नाम और खुराक:",
        "med_name_ph": "उदा. पैरासिटामोल (650mg)",
        "sched_time_label": "निर्धारित समय:",
        "sched_time_ph": "उदा. दोपहर 02:00 बजे",
        "assign_week": "सप्ताह में असाइन करें:",
        "assign_day": "दिन में असाइन करें:",
        "add_med_btn": "दवा जोड़ें",
        "med_table_title": "बहु-सप्ताह दवाओं का अवलोकन",
        "overall_adh": "कुल रोगी दवा पालन दर",
        "send_note_label": "रोगी को एक प्रोत्साहन संदेश या अनुस्मारक भेजें:",
        "send_note_ph": "पिताजी, आज समय पर दवा लेने के लिए बहुत बढ़िया!",
        "send_push_btn": "पुश अधिसूचना भेजें",
        "refill_title": "💊 गोली का स्टॉक और रीफिल चेतावनी",
        "refill_btn": "📲 मेडिकल दुकान को व्हाट्सएप रिफिल अलर्ट भेजें",
        # Passport Tab
        "pass_title": "सुरक्षित चिकित्सा पासपोर्ट और आपातकालीन SOS",
        "pass_sub": "महत्वपूर्ण ऑनलाइन/ऑफलाइन रोगी चिकित्सा पासपोर्ट और लाइव प्रसारण पोर्टल।",
        "patient_id_title": "रोगी मेडिकल आईडी",
        "dl_pass_btn": "सुरक्षित मेडिकल आईडी डाउनलोड करें (PDF/QR)",
        "vitals_title": "📈 रोगी के स्वास्थ्य मापदंड और रुझान",
        "sos_title": "एक-टैप आपातकालीन SOS प्रसारण",
        "sos_warn": "यह बटन दबाने पर आपका लाइव जीपीएस स्थान आपातकालीन संपर्कों को तुरंत भेज दिया जाएगा।",
        "sos_note_label": "वैकल्पिक आपातकालीन नोट:",
        "sos_note_ph": "उदा. सीने में दर्द हो रहा है, तत्काल सहायता की आवश्यकता है।",
        "sos_btn": "आपातकालीन SOS ट्रिगर करें",
        "offline_card_title": "📡 ग्रामीण क्षेत्रों के लिए ऑफ़लाइन प्राथमिक चिकित्सा कार्ड",
        # Impact Tab
        "impact_title": "संयुक्त राष्ट्र सतत विकास लक्ष्य 3 संरेखण",
        "impact_sub": "सभी उम्र के लोगों के लिए स्वस्थ जीवन सुनिश्चित करें और कल्याण को बढ़ावा दें।",
        "globe_title": "🌐 वैश्विक बीमारी बोझ 3D ग्लोब",
        "globe_desc": "प्रमुख क्षेत्रों में प्राथमिक स्वास्थ्य बोझ और मामलों की मात्रा दर्शाने वाला इंटरैक्टिव विज़ुअलाइज़ेशन।",
        "metric_doses": "दवा छूटने की दर में अनुमानित कमी",
        "metric_doses_desc": "स्वचालित अनुस्मारक और पारिवारिक देखभालकर्ता सिंक के माध्यम से।",
        "metric_triage": "आपातकालीन ट्राइएज में बचाया गया समय",
        "metric_triage_desc": "त्वरित अस्पताल मार्ग और लाइव जीपीएस द्वारा।",
        "low_resource": "ग्रामीण क्षेत्रों में कम इंटरनेट बैंडविड्थ पर भी सुचारू रूप से चलने के लिए डिज़ाइन किया गया।"
    }
}

# Inject Master CSS
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    .stApp {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.28) 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.25) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.18) 0%, transparent 65%),
            radial-gradient(circle at 30% 70%, rgba(168, 85, 247, 0.2) 0%, transparent 60%);
        background-size: 160% 160%;
        animation: cloudDrift 18s ease-in-out infinite alternate;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        padding-bottom: 140px;
    }

    @keyframes cloudDrift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 50% 100%; }
    }

    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select, div[data-baseweb="select"] div {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #ffffff !important;
        border: 2px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 16px !important;
        padding: 12px 20px !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.12);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 35px rgba(56, 189, 248, 0.6), 0 0 70px rgba(99, 102, 241, 0.35) !important;
        transform: scale(1.01);
    }

    div[data-testid="metric-container"], div.stTabs, .stExpander {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        padding: 22px;
        border-radius: 22px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }

    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 12px 24px;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4);
        width: 100%;
        cursor: pointer !important;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #4f46e5 100%) !important;
        box-shadow: 0 0 35px rgba(56, 189, 248, 0.85);
        transform: translateY(-3px) scale(1.02);
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
# 5. MODULE 0: HOME & BENTO OVERVIEW
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

        # AI Safety Checker with Voice Command Integration
        with st.expander(t["ai_title"], expanded=False):
            st.markdown(t["ai_prompt"])
            
            c_input, c_voice = st.columns([3, 1])
            with c_input:
                symptom_query = st.text_input(t["ai_input_label"], placeholder=t["ai_placeholder"], key="home_ai_query")
            with c_voice:
                st.write("")
                st.write("")
                if st.button(t["voice_btn"]):
                    st.info("🎙️ Listening... Speak your symptom clearly.")

            if st.button(t["ai_btn"], key="home_ai_btn"):
                if symptom_query:
                    st.info(t["ai_res"])
                else:
                    st.warning("Please enter or speak a symptom or drug name to analyze.")

        with st.expander(t["summary_title"], expanded=False):
            st.markdown("### 🏥 Clinical Handover Report")
            p = st.session_state.patient_passport
            st.markdown(f"**Patient Name:** {p['name']}")
            st.markdown(f"**Active Conditions:** {p['conditions']}")
            st.markdown(f"**Overall Adherence Rate:** 92.4% (Last 4 Weeks)")
            st.markdown(f"**Saved Patient Questions:**")
            for q in st.session_state.questions:
                st.markdown(f"- {q}")
            
            if st.button(t["summary_btn"], key="home_pdf_btn"):
                st.success(t["summary_success"])

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
        st.error(f"Error loading Home Dashboard: {home_err}")

# ----------------------------------------------------
# 6. MODULE 1: UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
elif current_tab == "Hospital":
    try:
        col_title, col_bell = st.columns([4, 1])
        with col_title:
            st.title(t["hosp_title"])
        with col_bell:
            notif_count = len(st.session_state.notifications)
            with st.popover(f"🔔 Alerts ({notif_count})"):
                st.markdown("### **Patient Alert Feed**")
                if not notif_count:
                    st.info("No notifications.")
                else:
                    for n in reversed(st.session_state.notifications):
                        st.markdown(f"🕒 *{n.get('time', 'Recent')}*<br>**{n.get('msg', '')}**", unsafe_allow_html=True)
                        st.divider()

        st.divider()

        st.subheader(t["search_heading"])
        user_disease_input = st.text_input(
            t["search_label"],
            placeholder=t["search_placeholder"],
            key="map_disease_search"
        )

        user_lat = st.session_state.user_location["lat"]
        user_lon = st.session_state.user_location["lon"]

        h_lat, h_lon = 16.6900, 74.2200
        h_name = "Alliance Multispeciality Hospital"
        travel_info = "~2.1 km away | 5 mins via City Road"

        query = (user_disease_input or "").lower().strip()
        
        if any(k in query for k in ["heart", "cardio", "chest", "bp", "stroke", "blood pressure"]):
            h_lat, h_lon = 16.7050, 74.2433
            h_name = "Aster Aadhar Hospital (Cardiology Center)"
            travel_info = "~3.2 km away | 8 mins via NH48"
            st.error("Specialty Match: Cardiology & Emergency Cardiac Unit")
        elif any(k in query for k in ["eye", "vision", "cataract", "blind", "blur"]):
            h_lat, h_lon = 16.7120, 74.2500
            h_name = "Nandadeep Eye Hospital (Ophthalmology)"
            travel_info = "~4.5 km away | 12 mins via Tarabai Park Road"
            st.warning("Specialty Match: Ophthalmology & Vision Care")
        elif any(k in query for k in ["bone", "fracture", "ortho", "joint", "knee", "accident"]):
            h_lat, h_lon = 16.7200, 74.4600
            h_name = "Dr. Lande Fracture Hospital (Trauma & Ortho)"
            travel_info = "~6.0 km away | 15 mins via Main Road"
            st.info("Specialty Match: Orthopedics & Trauma Center")
        elif user_disease_input:
            st.success("General Multi-Specialty Care")
        else:
            st.info("Type a condition above to locate the specialized facility.")

        st.markdown(f"📍 **{t['rec_fac']}** **{h_name}** — *{travel_info}*")

        try:
            map_data = get_cached_map_data(user_lat, user_lon, h_lat, h_lon, h_name)

            scatterplot_layer = pdk.Layer(
                "ScatterplotLayer",
                map_data,
                get_position=["longitude", "latitude"],
                get_fill_color="color",
                get_radius="radius",
                pickable=True,
                stroked=True,
                filled=True,
                line_width_min_pixels=3,
                get_line_color=[255, 255, 255]
            )

            view_state = pdk.ViewState(
                latitude=(user_lat + h_lat) / 2,
                longitude=(user_lon + h_lon) / 2,
                zoom=13,
                pitch=20,
            )

            r = pdk.Deck(
                layers=[scatterplot_layer],
                initial_view_state=view_state,
                tooltip={"text": "{name}"},
                map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
            )

            st.pydeck_chart(r, use_container_width=True)
            st.caption(f"{t['map_cyan']} | {t['map_rose']}")
        except Exception as map_err:
            st.error(f"Map rendering error: {map_err}")

        st.divider()

        col_left, col_right = st.columns(2)

        with col_left:
            try:
                st.subheader(t["med_sched_title"])
                
                selected_week = st.selectbox(
                    t["choose_week"], 
                    ["Week 1", "Week 2", "Week 3", "Week 4"],
                    key="patient_week_selector"
                )

                selected_day = st.selectbox(
                    t["choose_day"], 
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    key="patient_day_selector"
                )
                
                week_data = st.session_state.meds_by_week.get(selected_week, {})
                day_meds = week_data.get(selected_day, [])
                
                if not day_meds:
                    st.info(f"{t['no_meds']} {selected_day} ({selected_week}).")
                else:
                    for i, med in enumerate(day_meds):
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.write(f"**{med['name']}**")
                            st.caption(f"Time: {med['time']} | Category: *{med['category']}* | Status: {med['status']}")
                        with c2:
                            if med['status'] == "Pending":
                                if st.button(t["mark_taken"], key=f"taken_{selected_week}_{selected_day}_{i}"):
                                    st.session_state.meds_by_week[selected_week][selected_day][i]['status'] = "Taken ✅"
                                    st.session_state.pill_stock = max(0, st.session_state.pill_stock - 1)
                                    st.rerun()
                            else:
                                st.success(t["taken"])
            except Exception as med_err:
                st.error(f"Error loading schedule: {med_err}")

        with col_right:
            try:
                st.subheader(t["doc_title"])
                st.info(t["doc_info"])
                
                new_q = st.text_input(t["add_q_label"], placeholder=t["add_q_placeholder"])
                if st.button(t["save_q_btn"]):
                    if new_q:
                        st.session_state.questions.append(new_q)
                        st.success("Saved successfully!")
                        
                st.markdown(f"**{t['saved_qs']}**")
                for q in st.session_state.questions:
                    st.markdown(f"- 🔸 {q}")
            except Exception as doc_err:
                st.error(f"Error in doctor section: {doc_err}")

    except Exception as hub_err:
        st.error(f"Error in Hospital Hub: {hub_err}")

# ----------------------------------------------------
# 7. MODULE 2: CAREGIVER LIVE SYNC & PASSPORT EDITOR
# ----------------------------------------------------
elif current_tab == "Caregiver":
    try:
        st.title(t["care_title"])
        st.markdown(t["care_sub"])
        st.divider()

        password_input = st.text_input(t["care_pin_label"], type="password", placeholder=t["care_pin_ph"])
        
        if password_input == "1234":
            st.success(t["access_granted"])

            # Feature: OCR Prescription Scanner
            with st.expander(t["ocr_title"], expanded=False):
                st.file_uploader(t["ocr_upload"], type=["png", "jpg", "jpeg", "pdf"])
                if st.button(t["ocr_btn"]):
                    st.success("✅ Prescription successfully scanned! Metformin (500mg) and Atorvastatin (10pm) extracted and added to schedule.")

            # Feature: Pill Refill Alert Widget
            st.subheader(t["refill_title"])
            if st.session_state.pill_stock <= 5:
                st.warning(f"⚠️ **Low Pill Stock Warning:** Only {st.session_state.pill_stock} Metformin tablets remaining.")
            else:
                st.info(f"Pill Stock Level: {st.session_state.pill_stock} tablets remaining.")
            
            if st.button(t["refill_btn"]):
                st.success("📲 WhatsApp refill message generated & sent to Local Pharmacy!")
            st.divider()
            
            with st.expander(t["edit_pass_exp"], expanded=False):
                try:
                    with st.form("edit_passport_form"):
                        st.markdown(f"### {t['update_info']}")
                        edited_name = st.text_input(t["full_name"], value=st.session_state.patient_passport["name"])
                        edited_blood = st.text_input(t["blood_group"], value=st.session_state.patient_passport["blood_group"])
                        edited_contact = st.text_input(t["emerg_contact"], value=st.session_state.patient_passport["emergency_contact"])
                        edited_allergies = st.text_input(t["allergies"], value=st.session_state.patient_passport["allergies"])
                        edited_conditions = st.text_input(t["conditions"], value=st.session_state.patient_passport["conditions"])
                        edited_physician = st.text_input(t["physician"], value=st.session_state.patient_passport["physician"])
                        
                        save_passport = st.form_submit_button(t["save_pass_btn"])
                        if save_passport:
                            st.session_state.patient_passport["name"] = edited_name
                            st.session_state.patient_passport["blood_group"] = edited_blood
                            st.session_state.patient_passport["emergency_contact"] = edited_contact
                            st.session_state.patient_passport["allergies"] = edited_allergies
                            st.session_state.patient_passport["conditions"] = edited_conditions
                            st.session_state.patient_passport["physician"] = edited_physician
                            
                            st.session_state.notifications.append({
                                "msg": "Medical Passport updated by Caregiver.",
                                "time": "Just now"
                            })
                            st.success("Medical Passport details successfully updated!")
                            st.rerun()
                except Exception as pass_edit_err:
                    st.error(f"Error updating passport: {pass_edit_err}")

            with st.expander(t["add_med_exp"], expanded=True):
                try:
                    with st.form("add_med_form", clear_on_submit=True):
                        new_med_name = st.text_input(t["med_name_label"], placeholder=t["med_name_ph"])
                        new_med_time = st.text_input(t["sched_time_label"], placeholder=t["sched_time_ph"])
                        target_week = st.selectbox(t["assign_week"], ["All Weeks", "Week 1", "Week 2", "Week 3", "Week 4"])
                        target_day = st.selectbox(t["assign_day"], ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                        
                        submitted = st.form_submit_button(t["add_med_btn"])
                        if submitted:
                            if new_med_name and new_med_time:
                                detected_category = auto_categorize_medicine(new_med_name)
                                new_item = {"name": new_med_name, "time": new_med_time, "status": "Pending", "category": detected_category}
                                
                                weeks_to_update = ["Week 1", "Week 2", "Week 3", "Week 4"] if target_week == "All Weeks" else [target_week]
                                days_to_update = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if target_day == "All Days" else [target_day]
                                
                                for w in weeks_to_update:
                                    if w not in st.session_state.meds_by_week:
                                        st.session_state.meds_by_week[w] = {}
                                    for d in days_to_update:
                                        if d not in st.session_state.meds_by_week[w]:
                                            st.session_state.meds_by_week[w][d] = []
                                        st.session_state.meds_by_week[w][d].append(new_item)
                                        
                                st.success(f"Successfully added {new_med_name}!")
                                st.rerun()
                            else:
                                st.warning("Please fill in medicine name and time.")
                except Exception as form_err:
                    st.error(f"Form submission error: {form_err}")

            st.divider()
            st.subheader(t["med_table_title"])
            
            try:
                all_meds_flat = []
                for week, d_dict in st.session_state.meds_by_week.items():
                    for day, m_list in d_dict.items():
                        for m in m_list:
                            all_meds_flat.append({
                                "Week": week, 
                                "Day": day, 
                                "Medicine": m["name"], 
                                "Time": m["time"], 
                                "Category": m["category"], 
                                "Status": m["status"]
                            })
                
                st.dataframe(pd.DataFrame(all_meds_flat), use_container_width=True)
            except Exception as table_err:
                st.error(f"Table rendering error: {table_err}")
            
            st.metric(label=t["overall_adh"], value="92%", delta="+4% improvement")
            
            try:
                with st.form("caregiver_alert", clear_on_submit=True):
                    msg = st.text_area(t["send_note_label"], placeholder=t["send_note_ph"])
                    if st.form_submit_button(t["send_push_btn"]):
                        if msg.strip():
                            st.session_state.notifications.append({
                                "msg": f"Caregiver Note: {msg}",
                                "time": "Just now"
                            })
                            st.success("Notification sent to Patient Bell Feed!")
                        else:
                            st.warning("Please enter a message.")
            except Exception as alert_err:
                st.error(f"Notification error: {alert_err}")
                    
        elif password_input:
            st.error("Incorrect PIN. Please try again.")
        else:
            st.info("Enter PIN `1234` to unlock prescription & profile controls.")

    except Exception as caregiver_err:
        st.error(f"Error in Caregiver Portal: {caregiver_err}")

# ----------------------------------------------------
# 8. MODULE 3: DIGITAL MEDICAL PASSPORT & SOS
# ----------------------------------------------------
elif current_tab == "Passport":
    try:
        st.title(t["pass_title"])
        st.markdown(t["pass_sub"])
        st.divider()

        col_id_left, col_id_right = st.columns(2)

        with col_id_left:
            st.subheader(t["patient_id_title"])
            p = st.session_state.patient_passport
            st.markdown(f"""
                * **{t['full_name']}** {p['name']}
                * **{t['blood_group']}** {p['blood_group']}
                * **{t['emerg_contact']}** {p['emergency_contact']}
                * **{t['allergies']}** {p['allergies']}
                * **{t['conditions']}** {p['conditions']}
                * **{t['physician']}** {p['physician']}
            """)
            if st.button(t["dl_pass_btn"]):
                st.success("Emergency QR Passport generated securely!")

            # Feature: Vitals Tracker Chart
            st.divider()
            st.subheader(t["vitals_title"])
            vitals_df = pd.DataFrame({
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Blood Pressure (Systolic)": [128, 130, 125, 122, 126, 124, 120],
                "Blood Sugar (mg/dL)": [142, 138, 145, 130, 135, 128, 125]
            })
            st.line_chart(vitals_df.set_index("Day"))

            st.divider()
            with st.expander(t["offline_card_title"], expanded=False):
                st.markdown("""
                * **CPR Instructions:** 100-120 chest compressions/min.
                * **Hypoglycemia Emergency:** Administer glucose/sugar water immediately.
                * **Local Emergency Numbers:** 108 (Ambulance), 112 (National Emergency).
                """)

        with col_id_right:
            st.subheader(t["sos_title"])
            st.warning(t["sos_warn"])
            
            sos_message = st.text_area(t["sos_note_label"], placeholder=t["sos_note_ph"])
            
            if st.button(t["sos_btn"]):
                st.session_state.notifications.append({
                    "msg": f"🚨 EMERGENCY SOS TRIGGERED! Note: {sos_message or 'Immediate assistance requested.'}",
                    "time": "Just now (CRITICAL)"
                })
                st.error("🚨 SOS Alert Broadcasted Successfully!")

    except Exception as passport_err:
        st.error(f"Error in Passport Portal: {passport_err}")

# ----------------------------------------------------
# 9. MODULE 4: SDG 3 IMPACT & INTERACTIVE 3D GLOBE
# ----------------------------------------------------
elif current_tab == "Impact":
    try:
        st.title(t["impact_title"])
        st.markdown(f"### *{t['impact_sub']}*")
        st.divider()

        st.subheader(t["globe_title"])
        st.markdown(t["globe_desc"])

        globe_html = """
        <div style="width: 100%; height: 420px; background: radial-gradient(circle at center, #0f172a 0%, #030712 100%); border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6);">
            <div style="position: absolute; width: 320px; height: 320px; border: 2px dashed rgba(56, 189, 248, 0.25); border-radius: 50%; animation: spin 25s linear infinite;"></div>
            <div style="position: absolute; width: 260px; height: 260px; border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 50%; animation: spinReverse 20s linear infinite;"></div>
            
            <div style="z-index: 2; text-align: center; padding: 20px;">
                <div style="font-size: 54px; margin-bottom: 10px; animation: float 3s ease-in-out infinite;">🌍</div>
                <h3 style="color: #38bdf8; font-family: sans-serif; margin: 0 0 8px 0; font-size: 22px; font-weight: 700;">Global Health Intelligence Node</h3>
                <p style="color: #94a3b8; font-family: sans-serif; font-size: 14px; max-width: 450px; margin: 0 auto 16px auto;">
                    Tracking regional case density: <b>Cardiovascular & Metabolic Burdens</b> highlighted across North America, South Asia, and East Asia.
                </p>
                <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38bdf8; padding: 6px 14px; border-radius: 9999px; font-size: 12px; font-weight: 600;">🇺🇸 US: Ischemic Heart (~32.5M)</span>
                    <span style="background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); color: #fb7185; padding: 6px 14px; border-radius: 9999px; font-size: 12px; font-weight: 600;">🇮🇳 India: Hypertension (~78.2M)</span>
                    <span style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); color: #818cf8; padding: 6px 14px; border-radius: 9999px; font-size: 12px; font-weight: 600;">🇯🇵 Japan: Cerebrovascular (~14.1M)</span>
                </div>
            </div>
        </div>

        <style>
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes spinReverse { 0% { transform: rotate(360deg); } 100% { transform: rotate(0deg); } }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
        </style>
        """
        components.html(globe_html, height=440)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=t["metric_doses"], value="38%", delta="High Adherence")
            st.write(t["metric_doses_desc"])
        with col2:
            st.metric(label=t["metric_triage"], value="45%", delta="Fast GPS Routing")
            st.write(t["metric_triage_desc"])

        st.info(t["low_resource"])
    except Exception as impact_err:
        st.error(f"Error loading metrics: {impact_err}")

# ----------------------------------------------------
# 10. BULLETPROOF PURE CSS FLOATING DOCK
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
        align-items: center;
        gap: 12px;
        background: rgba(10, 15, 30, 0.9);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 9999px;
        padding: 8px 18px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 35px rgba(56, 189, 248, 0.25);
        z-index: 999999;
    }}

    .dock-btn {{
        position: relative;
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
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}

    .dock-btn .dock-tooltip {{
        position: absolute;
        top: -42px;
        left: 50%;
        transform: translateX(-50%) translateY(6px) scale(0.8);
        background: rgba(15, 23, 42, 0.95);
        color: #f8fafc;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}

    .dock-btn:hover .dock-tooltip {{
        opacity: 1;
        transform: translateX(-50%) translateY(0px) scale(1);
    }}

    .dock-btn:hover {{
        transform: scale(1.35) translateY(-8px);
        background: rgba(51, 65, 85, 0.95);
        border-color: rgba(56, 189, 248, 0.7);
        box-shadow: 0 15px 30px rgba(56, 189, 248, 0.4);
    }}

    .dock-btn.active {{
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.8) !important;
    }}
    </style>

    <div class="aceternity-dock-container">
        <a href="?tab=Home" target="_self" class="dock-btn {active_home}">
            <span class="dock-tooltip">Home</span>🏠
        </a>
        <a href="?tab=Hospital" target="_self" class="dock-btn {active_hosp}">
            <span class="dock-tooltip">Hospital Hub</span>🏥
        </a>
        <a href="?tab=Caregiver" target="_self" class="dock-btn {active_care}">
            <span class="dock-tooltip">Caregiver Portal</span>👁️
        </a>
        <a href="?tab=Passport" target="_self" class="dock-btn {active_pass}">
            <span class="dock-tooltip">Medical Passport</span>🛡️
        </a>
        <a href="?tab=Impact" target="_self" class="dock-btn {active_imp}">
            <span class="dock-tooltip">SDG 3 Impact</span>🌍
        </a>
    </div>
""", unsafe_allow_html=True)

# Footer
try:
    st.markdown("---")
    st.caption("HealthBridge Aceternity Master Edition • Built with Python, Streamlit & PyDeck 🚀")
except Exception:
    pass
