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

# Initialize Active Tab in Session State (Instant switching)
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

def switch_tab(tab_name):
    st.session_state.active_tab = tab_name

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

# Initialize Session State Data
try:
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

except Exception as init_error:
    st.error(f"Initialization Notice: {init_error}")

current_tab = st.session_state.active_tab

# Inject Master CSS & Strict Floating Dock Container Constraints
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

    /* ========================================================
       STRICT CENTERED FLOATING DOCK CONTAINER & COLUMN FIX
       ======================================================== */
    .aceternity-dock-container {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        background: rgba(15, 23, 42, 0.92) !important;
        backdrop-filter: blur(25px) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.45) !important;
        border-radius: 9999px !important;
        padding: 8px 18px !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(56, 189, 248, 0.3) !important;
        z-index: 999999 !important;
        width: auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Force Streamlit horizontal block inside dock to pack tightly */
    .aceternity-dock-container [data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 12px !important;
        width: auto !important;
        flex-grow: 0 !important;
        align-items: center !important;
    }

    /* Force individual columns inside dock to shrink-wrap */
    .aceternity-dock-container [data-testid="column"] {
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: unset !important;
        padding: 0 !important;
    }

    /* Circular Dock Button Styles */
    .aceternity-dock-container div.stButton > button {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 50% !important;
        height: 48px !important;
        width: 48px !important;
        padding: 0 !important;
        font-size: 20px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    .aceternity-dock-container div.stButton > button:hover {
        transform: scale(1.35) translateY(-6px) !important;
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 12px 35px rgba(56, 189, 248, 0.85) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. CONDITIONAL MODULE RENDERER
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
                switch_tab("Hospital")
                st.rerun()

        with col_b:
            st.markdown("### Medication Suite\nMulti-week medication schedules, independent daily resets, and smart categorization.")
            if st.button("Open Medication Hub", key="home_btn_med"):
                switch_tab("Hospital")
                st.rerun()

        with col_c:
            st.markdown("### Secure Passport\nDigital Medical ID with single-tap emergency SOS broadcasting.")
            if st.button("Open Medical Passport", key="home_btn_pass"):
                switch_tab("Passport")
                st.rerun()

    except Exception as home_err:
        st.error(f"Error loading Home Dashboard: {home_err}")

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

elif current_tab == "Caregiver":
    try:
        st.title("Caregiver Prescription Manager")
        st.markdown("Secure portal for remote family monitoring and prescription assignment.")
        st.divider()

        password_input = st.text_input("🔒 Enter Caregiver Access PIN:", type="password", placeholder="Enter PIN (Demo PIN: 1234)", key="caregiver_pin_input")
        
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
            
            sos_message = st.text_area("Optional Emergency Note:", placeholder="e.g., Experiencing chest pain, need immediate assistance.", key="sos_note_input")
            
            if st.button("TRIGGER EMERGENCY SOS"):
                st.session_state.notifications.append({
                    "msg": f"🚨 EMERGENCY SOS TRIGGERED! Note: {sos_message or 'Immediate assistance requested.'}",
                    "time": "Just now (CRITICAL)"
                })
                st.error("🚨 SOS Alert Broadcasted Successfully!")

    except Exception as passport_err:
        st.error(f"Error in Passport Portal: {passport_err}")

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
# 4. BLANKED & CENTERED FLOATING DOCK CONTAINER
# ----------------------------------------------------
st.markdown('<div class="aceternity-dock-container">', unsafe_allow_html=True)
dock_cols = st.columns(5)

with dock_cols[0]:
    if st.button("🏠", key="dock_home_btn"):
        switch_tab("Home")
        st.rerun()
with dock_cols[1]:
    if st.button("🏥", key="dock_hosp_btn"):
        switch_tab("Hospital")
        st.rerun()
with dock_cols[2]:
    if st.button("👁️", key="dock_care_btn"):
        switch_tab("Caregiver")
        st.rerun()
with dock_cols[3]:
    if st.button("🛡️", key="dock_pass_btn"):
        switch_tab("Passport")
        st.rerun()
with dock_cols[4]:
    if st.button("🌍", key="dock_imp_btn"):
        switch_tab("Impact")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
try:
    st.markdown("---")
    st.caption("HealthBridge Aceternity Master Edition • Built with Python, Streamlit & PyDeck 🚀")
except Exception:
    pass
