import streamlit as st
import pandas as pd
import pydeck as pdk

# --- 1. APP CONFIG & ELEGANT TYPOGRAPHY STYLING ---
try:
    st.set_page_config(
        page_title="HealthBridge - Unified SDG 3 Companion", 
        page_icon="🏥", 
        layout="wide"
    )
except Exception:
    pass

# Custom CSS for Elegant Fonts, Mobile Visibility, and Glassmorphism
st.markdown("""
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    <style>
    /* Global Font Styling - Elegant SaaS Aesthetic */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #171b38 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling & Mobile Visibility */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #090d16 100%) !important;
        border-right: 1px solid #1f2937;
    }
    
    section[data-testid="stSidebar"] .block-container {
        color: #ffffff !important;
    }

    .stRadio label p {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] span {
        color: #94a3b8 !important;
    }

    /* High-Contrast Mobile Input Field Text Visibility */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, div[data-baseweb="select"] div {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 12px;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    input::placeholder, textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Sleek Modern Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 10px 22px;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
        transform: translateY(-2px);
    }

    /* Glassmorphism Cards */
    div[data-testid="metric-container"], div.stTabs {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 18px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ROBUST HELPER FUNCTIONS & SESSION STATE INITIALIZATION ---
try:
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

    # Initialize Dynamic User Location on App Load
    if "user_location" not in st.session_state:
        st.session_state.user_location = {
            "lat": 16.7010,
            "lon": 74.2390,
            "status": "GPS Synced (Kolhapur Central)"
        }

    # Initialize Notifications State for the Bell Icon
    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            {"msg": "Welcome to HealthBridge! Your caregiver and emergency link are active.", "time": "System Init"}
        ]

    # Initialize Multi-Week & Multi-Day Medication State
    if "meds_by_week" not in st.session_state:
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
        st.session_state.meds_by_week = default_schedule

    if "questions" not in st.session_state:
        st.session_state.questions = ["Are there any food restrictions with this dosage?"]

except Exception as init_error:
    st.error(f"Initialization Warning: {init_error}")

# --- 3. SIDEBAR NAVIGATION DASHBOARD ---
try:
    st.sidebar.title("🌟 HealthBridge")
    st.sidebar.markdown("### Unified Patient Companion")
    app_mode = st.sidebar.radio(
        "Select Navigation Option:", 
        [
            "🏠 Home & Welcome Dashboard",
            "🏥 Unified Health & Hospital Hub", 
            "👁️ Caregiver Live Sync", 
            "🪪 Digital Medical Passport & SOS",
            "🌍 SDG 3 Impact & Metrics"
        ]
    )

    st.sidebar.divider()
    st.sidebar.info("💡 **Demo Tip:** Search 'Heart', 'Eye', or 'Bones' to instantly pinpoint specialized hospitals on the map!")
except Exception:
    app_mode = "🏠 Home & Welcome Dashboard"

# ----------------------------------------------------
# 4. MODULE 0: HOME & WELCOME DASHBOARD
# ----------------------------------------------------
if app_mode == "🏠 Home & Welcome Dashboard":
    try:
        st.title("🌟 Welcome to HealthBridge")
        st.markdown("### *Your Unified SDG 3 Companion for Patient Adherence & Emergency Care*")
        st.divider()

        # Hero Banner Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Active Treatment Plan", value="Week 1 Active", delta="92% Adherence")
        with col2:
            st.metric(label="Emergency Readiness", value="GPS Active", delta="Kolhapur Region")
        with col3:
            st.metric(label="Caregiver Link", value="Connected 🔒", delta="PIN Protected")

        st.divider()

        # Quick Access Feature Cards
        st.subheader("🚀 Quick Actions & Core Modules")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("""
                #### 🏥 Hospital Hub
                Instant disease-to-hospital intelligent routing and live GPS location mapping.
            """)
            st.info("👈 Select 'Unified Health & Hospital Hub' in sidebar.")

        with col_b:
            st.markdown("""
                #### 💊 Medication Suite
                Multi-week day-by-day tracking, independent resets, and auto-categorization.
            """)
            st.info("👈 Access via Hospital Hub.")

        with col_c:
            st.markdown("""
                #### 🪪 Medical Passport & SOS
                Digital medical ID cards and one-tap emergency SOS broadcast.
            """)
            st.info("👈 Select 'Digital Medical Passport & SOS' in sidebar.")

        st.divider()
        st.markdown("### 🏆 SDG 3 Hackathon Alignment")
        st.write("HealthBridge bridges the critical gap between daily preventive care and emergency hospital triage in a single, mobile-responsive web platform designed for low-bandwidth rural and urban communities.")
    except Exception as home_err:
        st.error(f"Error loading Home Dashboard: {home_err}")

# ----------------------------------------------------
# 5. MODULE 1: UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
elif app_mode == "🏥 Unified Health & Hospital Hub":
    try:
        # Top Header Bar with Notification Bell Icon
        col_title, col_bell = st.columns([4, 1])
        with col_title:
            st.title("🌟 HealthBridge: Unified Patient Companion")
        with col_bell:
            notif_count = len(st.session_state.notifications)
            with st.popover(f"🔔 Notifications ({notif_count})"):
                st.markdown("### **Patient Alert Center**")
                if not notif_count:
                    st.info("No notifications at this time.")
                else:
                    for n in reversed(st.session_state.notifications):
                        st.markdown(f"🕒 *{n.get('time', 'Recent')}*<br>**{n.get('msg', '')}**", unsafe_allow_html=True)
                        st.divider()

        st.markdown("*Combining intelligent emergency hospital routing, live GPS geolocation, and multi-week medication adherence.*")
        st.divider()

        st.subheader("🔍 Disease-to-Hospital Intelligent Map Finder")
        
        user_disease_input = st.text_input(
            "Enter disease/symptom:",
            placeholder="Type condition here... (e.g., Heart, Eye, Bones)",
            key="map_disease_search"
        )

        # Retrieve Dynamic User Location from Session State
        user_lat = st.session_state.user_location["lat"]
        user_lon = st.session_state.user_location["lon"]

        # Default Hospital Location (General)
        h_lat, h_lon = 16.6900, 74.2200
        h_name = "Alliance Multispeciality Hospital"
        travel_info = "~2.1 km away | 5 mins via City Road"

        query = (user_disease_input or "").lower().strip()
        
        # Accurate Condition-to-Hospital Matching Logic
        if any(k in query for k in ["heart", "cardio", "chest", "bp", "stroke", "blood pressure"]):
            h_lat, h_lon = 16.7050, 74.2433
            h_name = "Aster Aadhar Hospital (Cardiology Center)"
            travel_info = "~3.2 km away | 8 mins via NH48"
            st.error("⚠️ **Specialty Match: Cardiology & Emergency Cardiac Unit**")
        elif any(k in query for k in ["eye", "vision", "cataract", "blind", "blur"]):
            h_lat, h_lon = 16.7120, 74.2500
            h_name = "Nandadeep Eye Hospital (Ophthalmology)"
            travel_info = "~4.5 km away | 12 mins via Tarabai Park Road"
            st.warning("👁️ **Specialty Match: Ophthalmology & Vision Care**")
        elif any(k in query for k in ["bone", "fracture", "ortho", "joint", "knee", "accident"]):
            h_lat, h_lon = 16.7200, 74.4600
            h_name = "Dr. Lande Fracture Hospital (Trauma & Ortho)"
            travel_info = "~6.0 km away | 15 mins via Main Road"
            st.info("🦴 **Specialty Match: Orthopedics & Trauma Center**")
        elif user_disease_input:
            st.success("🏥 **General Multi-Specialty Care**")
        else:
            st.info("💡 *Type a condition above (e.g., 'Heart', 'Eye', 'Bones') to pinpoint the matching hospital.*")

        st.markdown(f"📍 **Recommended Facility:** **{h_name}** — *{travel_info}*")

        # --- Strict Map Data Frame & Rendering with Try/Catch ---
        try:
            map_data = pd.DataFrame([
                {
                    "latitude": user_lat, 
                    "longitude": user_lon, 
                    "name": "Your Location (Patient - GPS Active)", 
                    "color": [30, 144, 255, 255],  # Strict Blue Pin for User
                    "radius": 75
                },
                {
                    "latitude": h_lat, 
                    "longitude": h_lon, 
                    "name": h_name, 
                    "color": [255, 69, 0, 255],     # Strict Orange-Red Pin for Hospital
                    "radius": 85
                }
            ])

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
            st.caption("🔵 Blue Pin = Your Live GPS Location | 🟠 Orange Pin = Recommended Specialized Hospital")
        except Exception as map_err:
            st.error(f"Map rendering error: {map_err}")

        st.divider()

        # --- Multi-Week Medication Schedule & Question Builder ---
        col_left, col_right = st.columns(2)

        with col_left:
            try:
                st.subheader("💊 Multi-Week Medication Schedule")
                st.markdown("Select the treatment week and day to track adherence:")
                
                selected_week = st.selectbox(
                    "Choose Treatment Week:", 
                    ["Week 1", "Week 2", "Week 3", "Week 4"],
                    key="patient_week_selector"
                )

                selected_day = st.selectbox(
                    "Choose Day of Week:", 
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    key="patient_day_selector"
                )
                
                week_data = st.session_state.meds_by_week.get(selected_week, {})
                day_meds = week_data.get(selected_day, [])
                
                if not day_meds:
                    st.info(f"No medications scheduled for {selected_day} in {selected_week}.")
                else:
                    for i, med in enumerate(day_meds):
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.write(f"**{med['name']}**")
                            st.caption(f"Time: {med['time']} | Category: *{med['category']}* | Status: {med['status']}")
                        with c2:
                            if med['status'] == "Pending":
                                if st.button("Mark Taken", key=f"taken_{selected_week}_{selected_day}_{i}"):
                                    st.session_state.meds_by_week[selected_week][selected_day][i]['status'] = "Taken ✅"
                                    st.rerun()
                            else:
                                st.success("Taken ✅")
            except Exception as med_err:
                st.error(f"Error loading medication schedule: {med_err}")

        with col_right:
            try:
                st.subheader("🏥 Doctor Appointments & Question Builder")
                st.info("**Dr. Sharma (Cardiologist)**\n📅 Tomorrow at 10:30 AM\n📍 City General Hospital")
                
                new_q = st.text_input("Add a question for your doctor:", placeholder="e.g. Any side effects?")
                if st.button("Save Question"):
                    if new_q:
                        st.session_state.questions.append(new_q)
                        st.success("Saved successfully!")
                        
                st.markdown("**Your Saved Questions:**")
                for q in st.session_state.questions:
                    st.markdown(f"- 🔸 {q}")
            except Exception as doc_err:
                st.error(f"Error in doctor section: {doc_err}")

    except Exception as hub_err:
        st.error(f"Critical error in Hospital Hub: {hub_err}")

# ----------------------------------------------------
# 6. MODULE 2: CAREGIVER LIVE SYNC (PASSWORD PROTECTED)
# ----------------------------------------------------
elif app_mode == "👁️ Caregiver Live Sync":
    try:
        st.title("👁️ Caregiver Real-Time Monitor & Prescription Manager")
        st.markdown("Secure portal for family members to manage multi-week patient medications and monitor adherence remotely.")
        st.divider()

        password_input = st.text_input("🔒 Enter Caregiver Access Password:", type="password", placeholder="Enter PIN (Demo PIN: 1234)")
        
        if password_input == "1234":
            st.success("🔓 Access Granted! Connected to Patient Profile #PAT-8821")
            
            # --- Add New Prescription Form with Multi-Week Selection & Try/Except ---
            with st.expander("➕ Add New Medication to Schedule", expanded=True):
                try:
                    with st.form("add_med_form", clear_on_submit=True):
                        new_med_name = st.text_input("Medicine Name & Dosage:", placeholder="e.g., Paracetamol (650mg)")
                        new_med_time = st.text_input("Scheduled Time:", placeholder="e.g., 02:00 PM")
                        target_week = st.selectbox("Assign to Week:", ["All Weeks", "Week 1", "Week 2", "Week 3", "Week 4"])
                        target_day = st.selectbox("Assign to Day of Week:", ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                        
                        submitted = st.form_submit_button("Add Medication")
                        if submitted:
                            if new_med_name and new_med_time:
                                detected_category = auto_categorize_medicine(new_med_name)
                                new_item = {"name": new_med_name, "time": new_med_time, "status": "Pending", "category": detected_category}
                                
                                weeks_to_update = ["Week 1", "Week 2", "Week 3", "Week 4"] if target_week == "All Weeks" else [target_week]
                                days_to_update = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if target_day == "All Days" else [target_day]
                                
                                for w in weeks_to_update:
                                    for d in days_to_update:
                                        st.session_state.meds_by_week[w][d].append(new_item)
                                        
                                st.success(f"Successfully added {new_med_name} to {target_week} ({target_day})!")
                                st.rerun()
                            else:
                                st.warning("Please fill in both the medicine name and scheduled time.")
                except Exception as form_err:
                    st.error(f"Form submission error: {form_err}")

            st.divider()
            st.subheader("📋 Comprehensive Multi-Week Prescriptions Overview")
            
            # Display clean structured table overview across all weeks
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
                st.error(f"Error generating overview table: {table_err}")
            
            st.metric(label="Overall Patient Adherence Rate", value="92%", delta="+4% improvement")
            
            try:
                with st.form("caregiver_alert", clear_on_submit=True):
                    msg = st.text_area("Send an encouraging note or reminder to the patient:", placeholder="Dad, great job taking your medicine today!")
                    if st.form_submit_button("Send Push Notification"):
                        if msg.strip():
                            st.session_state.notifications.append({
                                "msg": f"Caregiver Note: {msg}",
                                "time": "Just now"
                            })
                            st.success("✅ Notification successfully sent and logged in Patient Bell Feed!")
                        else:
                            st.warning("Please enter a message before sending.")
            except Exception as alert_err:
                st.error(f"Error sending notification: {alert_err}")
                    
        elif password_input:
            st.error("❌ Incorrect password. Please check with the patient for the correct PIN.")
        else:
            st.info("ℹ️ Please enter the caregiver PIN to unlock prescription management tools.")

    except Exception as caregiver_err:
        st.error(f"Critical error in Caregiver Portal: {caregiver_err}")

# ----------------------------------------------------
# 7. MODULE 3: DIGITAL MEDICAL PASSPORT & SOS
# ----------------------------------------------------
elif app_mode == "🪪 Digital Medical Passport & SOS":
    try:
        st.title("🪪 Digital Medical Passport & Emergency SOS")
        st.markdown("*Instant offline/online access to critical medical data and emergency broadcasting.*")
        st.divider()

        col_id_left, col_id_right = st.columns(2)

        with col_id_left:
            st.subheader("📋 Patient Medical ID")
            st.markdown("""
                * **Full Legal Name:** Manas S. Abitkar
                * **Blood Group:** O+ Positive
                * **Emergency Contact:** +91 98765 43210 (Father / Caregiver)
                * **Known Allergies:** Penicillin, Peanuts
                * **Chronic Conditions:** Type 2 Diabetes, Hypertension
                * **Primary Physician:** Dr. Sharma (City General Hospital)
            """)
            if st.button("📥 Download Medical ID (PDF/QR)"):
                st.success("Emergency QR Passport generated successfully!")

        with col_id_right:
            st.subheader("🚨 One-Tap Emergency SOS Broadcast")
            st.warning("⚠️ Pressing this button will instantly broadcast your live GPS coordinates and medical ID to your emergency contacts and caregiver portal.")
            
            sos_message = st.text_area("Optional Emergency Note:", placeholder="e.g., Experiencing severe chest pain, need immediate transport.")
            
            if st.button("🚨 TRIGGER EMERGENCY SOS"):
                st.session_state.notifications.append({
                    "msg": f"🚨 EMERGENCY SOS TRIGGERED! Note: {sos_message or 'Immediate assistance requested.'}",
                    "time": "Just now (CRITICAL)"
                })
                st.error("🚨 SOS Alert Broadcasted! Caregiver notified via push notification.")

    except Exception as passport_err:
        st.error(f"Error loading Medical Passport: {passport_err}")

# ----------------------------------------------------
# 8. MODULE 4: SDG 3 IMPACT & METRICS
# ----------------------------------------------------
elif app_mode == "🌍 SDG 3 Impact & Metrics":
    try:
        st.title("🌍 UN Sustainable Development Goal 3 Alignment")
        st.markdown("### *Ensure healthy lives and promote well-being for all at all ages.*")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Projected Reduction in Missed Doses", value="38%", delta="High Adherence")
            st.write("Through intelligent automated multi-week reminders and family caregiver prescription syncing.")
        with col2:
            st.metric(label="Emergency Triage Time Saved", value="45%", delta="Fast GPS Routing")
            st.write("By linking disease searches instantly to specialized local hospitals and utilizing real-time GPS coordinates.")

        st.info("💡 **Low-Resource Scalability:** Designed to operate smoothly on low-bandwidth mobile networks in rural communities.")
    except Exception as impact_err:
        st.error(f"Error loading impact metrics: {impact_err}")

# Footer
try:
    st.markdown("---")
    st.caption("HealthBridge Unified Prototype • Built with Python, Streamlit & PyDeck 🚀")
except Exception:
    pass
