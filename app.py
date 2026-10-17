import streamlit as st
import pandas as pd
import pydeck as pdk

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

# --- 2. SESSION STATE & HELPER FUNCTIONS ---
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
    st.error(f"Initialization Notice: {init_error}")

# Inject Master CSS (Cloud Shader & Pure CSS Centered Floating Dock)
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

# ----------------------------------------------------
# 3. MODULE 0: HOME & BENTO OVERVIEW
# ----------------------------------------------------
if current_tab == "Home":
    try:
        st.title("Next-Gen Patient Companion")
        st.markdown("##### *Precision Healthcare, Atmospheric Cloud Triage & Family Caregiving for SDG 3*")
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Active Treatment Plan", value="Week 1 Active", delta="92% Adherence")
        with col2:
            st.metric(label="Emergency Readiness", value="GPS Online", delta="Kolhapur Region")
        with col3:
            st.metric(label="Caregiver Link", value="Connected 🔒", delta="PIN Protected")

        st.divider()

        st.subheader("Quick Access Bento Modules")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("### Hospital Hub\nIntelligent disease-to-hospital routing with dynamic dark-mode PyDeck maps.")
            if st.button("Open Hospital Hub", key="home_btn_hosp"):
                st.query_params["tab"] = "Hospital"
                st.rerun()

        with col_b:
            st.markdown("### Medication Suite\nMulti-week medication schedules, independent daily resets, and smart categorization.")
            if st.button("Open Medication Hub", key="home_btn_med"):
                st.query_params["tab"] = "Hospital"
                st.rerun()

        with col_c:
            st.markdown("### Secure Passport\nDigital Medical ID with single-tap emergency SOS broadcasting.")
            if st.button("Open Medical Passport", key="home_btn_pass"):
                st.query_params["tab"] = "Passport"
                st.rerun()

    except Exception as home_err:
        st.error(f"Error loading Home Dashboard: {home_err}")

# ----------------------------------------------------
# 4. MODULE 1: UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
elif current_tab == "Hospital":
    try:
        col_title, col_bell = st.columns([4, 1])
        with col_title:
            st.title("Intelligent Hospital Finder & Schedule")
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

        st.subheader("Gooey Disease-to-Hospital Search")
        user_disease_input = st.text_input(
            "Type condition / symptom:",
            placeholder="Type condition here... (e.g., Heart, Eye, Bones)",
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
            st.info("Type a condition above (e.g., 'Heart', 'Eye', 'Bones') to locate the specialized facility.")

        st.markdown(f"📍 **Recommended Facility:** **{h_name}** — *{travel_info}*")

        try:
            map_data = pd.DataFrame([
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
            st.caption("🔵 Cyan Pin = Live GPS Location | 🔴 Rose Pin = Recommended Specialized Hospital")
        except Exception as map_err:
            st.error(f"Map rendering error: {map_err}")

        st.divider()

        col_left, col_right = st.columns(2)

        with col_left:
            try:
                st.subheader("Multi-Week Medication Schedule")
                
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
                st.error(f"Error loading schedule: {med_err}")

        with col_right:
            try:
                st.subheader("Doctor Appointments & Questions")
                st.info("**Dr. Sharma (Cardiologist)**\n📅 Tomorrow at 10:30 AM\n📍 City General Hospital")
                
                new_q = st.text_input("Add a question for your doctor:", placeholder="e.g. Any food restrictions?")
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
        st.error(f"Error in Hospital Hub: {hub_err}")

# ----------------------------------------------------
# 5. MODULE 2: CAREGIVER LIVE SYNC
# ----------------------------------------------------
elif current_tab == "Caregiver":
    try:
        st.title("Caregiver Prescription Manager")
        st.markdown("Secure portal for remote family monitoring and prescription assignment.")
        st.divider()

        password_input = st.text_input("🔒 Enter Caregiver Access PIN:", type="password", placeholder="Enter PIN (Demo PIN: 1234)")
        
        if password_input == "1234":
            st.success("🔓 Access Granted! Connected to Patient Profile #PAT-8821")
            
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
            st.subheader("Multi-Week Prescriptions Overview")
            
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
            
            st.metric(label="Overall Patient Adherence Rate", value="92%", delta="+4% improvement")
            
            try:
                with st.form("caregiver_alert", clear_on_submit=True):
                    msg = st.text_area("Send an encouraging note or reminder to patient:", placeholder="Dad, great job taking your medicine today!")
                    if st.form_submit_button("Send Push Notification"):
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
            st.info("Enter PIN `1234` to unlock prescription controls.")

    except Exception as caregiver_err:
        st.error(f"Error in Caregiver Portal: {caregiver_err}")

# ----------------------------------------------------
# 6. MODULE 3: DIGITAL MEDICAL PASSPORT & SOS
# ----------------------------------------------------
elif current_tab == "Passport":
    try:
        st.title("Secure Medical Passport & Emergency SOS")
        st.markdown("Critical offline/online patient medical passport and live broadcast portal.")
        st.divider()

        col_id_left, col_id_right = st.columns(2)

        with col_id_left:
            st.subheader("Patient Medical ID")
            st.markdown("""
                * **Full Legal Name:** Manas S. Abitkar
                * **Blood Group:** O+ Positive
                * **Emergency Contact:** +91 98765 43210 (Caregiver)
                * **Known Allergies:** Penicillin, Peanuts
                * **Chronic Conditions:** Type 2 Diabetes, Hypertension
                * **Primary Physician:** Dr. Sharma (City General Hospital)
            """)
            if st.button("Download Secure Medical ID (PDF/QR)"):
                st.success("Emergency QR Passport generated securely!")

        with col_id_right:
            st.subheader("One-Tap Emergency SOS Broadcast")
            st.warning("Pressing this button instantly broadcasts your live GPS coordinates to emergency contacts.")
            
            sos_message = st.text_area("Optional Emergency Note:", placeholder="e.g., Experiencing chest pain, need immediate assistance.")
            
            if st.button("TRIGGER EMERGENCY SOS"):
                st.session_state.notifications.append({
                    "msg": f"🚨 EMERGENCY SOS TRIGGERED! Note: {sos_message or 'Immediate assistance requested.'}",
                    "time": "Just now (CRITICAL)"
                })
                st.error("🚨 SOS Alert Broadcasted Successfully!")

    except Exception as passport_err:
        st.error(f"Error in Passport Portal: {passport_err}")

# ----------------------------------------------------
# 7. MODULE 4: SDG 3 IMPACT & METRICS
# ----------------------------------------------------
elif current_tab == "Impact":
    try:
        st.title("UN Sustainable Development Goal 3 Alignment")
        st.markdown("### *Ensure healthy lives and promote well-being for all at all ages.*")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Projected Reduction in Missed Doses", value="38%", delta="High Adherence")
            st.write("Through intelligent automated multi-week reminders and family caregiver prescription syncing.")
        with col2:
            st.metric(label="Emergency Triage Time Saved", value="45%", delta="Fast GPS Routing")
            st.write("By linking disease searches instantly to specialized local hospitals and utilizing real-time GPS coordinates.")

        st.info("Low-Resource Scalability: Designed to operate smoothly on low-bandwidth mobile networks in rural communities.")
    except Exception as impact_err:
        st.error(f"Error loading metrics: {impact_err}")

# ----------------------------------------------------
# 8. BULLETPROOF PURE CSS FLOATING DOCK (ZERO SCATTERING)
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

    /* Tooltip Bubble */
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
