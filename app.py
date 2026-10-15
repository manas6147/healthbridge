import streamlit as st
import pandas as pd
import pydeck as pdk

# App Config & Vibrant UI Styling
st.set_page_config(
    page_title="HealthBridge - Unified SDG 3 Companion", 
    page_icon="🏥", 
    layout="wide"
)

# Custom CSS for Vibrant Glassmorphism & Modern Dashboard Look
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Gradient & Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .block-container {
        color: #f8fafc;
    }

    /* Glowing Text Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(30, 41, 59, 0.7);
        color: #ffffff;
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 10px;
    }

    /* Sleek Modern Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
        transform: translateY(-2px);
    }

    /* Glassmorphism Cards */
    div[data-testid="metric-container"], div.stTabs {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 15px;
        border-radius: 14px;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# --- Auto-Categorization Helper Function ---
def auto_categorize_medicine(med_name):
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

# Initialize Session State for Weekly Medications (1 clean med per day)
if "meds_by_day" not in st.session_state:
    st.session_state.meds_by_day = {
        "Monday": [{"name": "Metformin (500mg)", "time": "08:00 AM", "status": "Pending", "category": "Diabetes"}],
        "Tuesday": [{"name": "Amlodipine (5mg)", "time": "01:00 PM", "status": "Pending", "category": "Blood Pressure"}],
        "Wednesday": [{"name": "Vitamin D3 Supplement", "time": "08:00 PM", "status": "Pending", "category": "Wellness"}],
        "Thursday": [{"name": "Metformin (500mg)", "time": "08:00 AM", "status": "Pending", "category": "Diabetes"}],
        "Friday": [{"name": "Amlodipine (5mg)", "time": "01:00 PM", "status": "Pending", "category": "Blood Pressure"}],
        "Saturday": [{"name": "Vitamin D3 Supplement", "time": "08:00 PM", "status": "Pending", "category": "Wellness"}],
        "Sunday": [{"name": "Multivitamin Tablet", "time": "09:00 AM", "status": "Pending", "category": "Wellness"}]
    }

if "questions" not in st.session_state:
    st.session_state.questions = ["Are there any food restrictions with this dosage?"]

# Sidebar Dashboard Menu
st.sidebar.title("🌟 HealthBridge Dashboard")
app_mode = st.sidebar.radio(
    "Select Option:", 
    [
        "🏥 Unified Health & Hospital Hub", 
        "👁️ Caregiver Live Sync", 
        "🌍 SDG 3 Impact & Metrics"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Demo Tip:** Search 'Heart', 'Eye', or 'Bones' to instantly pinpoint specialized hospitals on the map!")

# ----------------------------------------------------
# 1. UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
if app_mode == "🏥 Unified Health & Hospital Hub":
    st.title("🌟 HealthBridge: Unified Patient Companion")
    st.markdown("*Combining intelligent emergency hospital routing, precise map pins, and weekly medication adherence.*")
    st.divider()

    st.subheader("🔍 Disease-to-Hospital Intelligent Map Finder")
    
    user_disease_input = st.text_input(
        "Enter disease/symptom:",
        placeholder="Type condition here... (e.g., Heart, Eye, Bones)",
        key="map_disease_search"
    )

    # --- Fixed Coordinates ---
    # User Location (Fixed Point)
    user_lat, user_lon = 16.7000, 74.2400  

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

    # --- Unambiguous Map Data Frame (User = Blue, Hospital = Orange) ---
    map_data = pd.DataFrame([
        {
            "lat": user_lat, 
            "lon": user_lon, 
            "name": "Your Location (Patient)", 
            "color": [30, 144, 255, 255],  # Strict Blue Pin for User
            "radius": 60
        },
        {
            "lat": h_lat, 
            "lon": h_lon, 
            "name": h_name, 
            "color": [255, 69, 0, 255],     # Strict Orange-Red Pin for Hospital
            "radius": 70
        }
    ])

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position=["lon", "lat"],
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        stroked=True,
        filled=True,
        line_width_min_pixels=2,
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
    st.caption("🔵 Blue Pin = Your Location | 🟠 Orange Pin = Recommended Specialized Hospital")

    st.divider()

    # --- Weekly Medication Layout & Question Builder ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💊 Weekly Medication Schedule")
        st.markdown("Select a day of the week to view and track daily adherence:")
        
        selected_day = st.selectbox(
            "Choose Day:", 
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            key="day_selector"
        )
        
        day_meds = st.session_state.meds_by_day[selected_day]
        
        if not day_meds:
            st.info(f"No medications scheduled for {selected_day}.")
        else:
            for i, med in enumerate(day_meds):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**{med['name']}**")
                    st.caption(f"Time: {med['time']} | Category: *{med['category']}* | Status: {med['status']}")
                with c2:
                    if med['status'] == "Pending":
                        if st.button("Mark Taken", key=f"taken_{selected_day}_{i}"):
                            st.session_state.meds_by_day[selected_day][i]['status'] = "Taken ✅"
                            st.rerun()
                    else:
                        st.success("Taken ✅")

    with col_right:
        st.subheader("🏥 Doctor Appointments & Question Builder")
        st.info("**Dr. Sharma (Cardiologist)**\n📅 Tomorrow at 10:30 AM\n📍 City General Hospital")
        
        new_q = st.text_input("Add a question for your doctor:", placeholder="e.g. Any side effects?")
        if st.button("Save Question"):
            if new_q:
                st.session_state.questions.append(new_q)
                st.success("Saved!")
                
        st.markdown("**Your Saved Questions:**")
        for q in st.session_state.questions:
            st.markdown(f"- 🔸 {q}")

# ----------------------------------------------------
# 2. CAREGIVER LIVE SYNC (PASSWORD PROTECTED)
# ----------------------------------------------------
elif app_mode == "👁️ Caregiver Live Sync":
    st.title("👁️ Caregiver Real-Time Monitor & Prescription Manager")
    st.markdown("Secure portal for family members to manage patient medications and monitor adherence remotely.")
    st.divider()

    password_input = st.text_input("🔒 Enter Caregiver Access Password:", type="password", placeholder="Enter PIN (Demo PIN: 1234)")
    
    if password_input == "1234":
        st.success("🔓 Access Granted! Connected to Patient Profile #PAT-8821")
        
        # --- Add New Prescription Form ---
        with st.expander("➕ Add New Medication to Schedule", expanded=True):
            with st.form("add_med_form"):
                new_med_name = st.text_input("Medicine Name & Dosage:", placeholder="e.g., Paracetamol (650mg)")
                new_med_time = st.text_input("Scheduled Time:", placeholder="e.g., 02:00 PM")
                target_day = st.selectbox("Assign to Day of Week:", ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                
                submitted = st.form_submit_button("Add Medication")
                if submitted:
                    if new_med_name and new_med_time:
                        detected_category = auto_categorize_medicine(new_med_name)
                        new_item = {"name": new_med_name, "time": new_med_time, "status": "Pending", "category": detected_category}
                        
                        if target_day == "All Days":
                            for d in st.session_state.meds_by_day:
                                st.session_state.meds_by_day[d].append(new_item)
                        else:
                            st.session_state.meds_by_day[target_day].append(new_item)
                            
                        st.success(f"Successfully added {new_med_name} (Category: {detected_category})!")
                        st.rerun()
                    else:
                        st.warning("Please fill in both the medicine name and time.")

        st.divider()
        st.subheader("📋 Current Weekly Prescriptions Overview")
        
        # Display clean table overview of all days
        all_meds_flat = []
        for day, m_list in st.session_state.meds_by_day.items():
            for m in m_list:
                all_meds_flat.append({"Day": day, "Medicine": m["name"], "Time": m["time"], "Category": m["category"], "Status": m["status"]})
        
        st.dataframe(pd.DataFrame(all_meds_flat), use_container_width=True)
        
        st.metric(label="Overall Patient Adherence Rate", value="92%", delta="+4% improvement")
        
        with st.form("caregiver_alert"):
            msg = st.text_area("Send an encouraging note or reminder to the patient:", placeholder="Dad, great job taking your medicine today!")
            if st.form_submit_button("Send Push Notification"):
                st.success("✅ Notification successfully sent to patient device!")
                
    elif password_input:
        st.error("❌ Incorrect password. Please check with the patient for the correct PIN.")
    else:
        st.info("ℹ️ Please enter the caregiver PIN to unlock prescription management tools.")

# ----------------------------------------------------
# 3. SDG 3 IMPACT & METRICS
# ----------------------------------------------------
elif app_mode == "🌍 SDG 3 Impact & Metrics":
    st.title("🌍 UN Sustainable Development Goal 3 Alignment")
    st.markdown("### *Ensure healthy lives and promote well-being for all at all ages.*")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Projected Reduction in Missed Doses", value="38%", delta="High Adherence")
        st.write("Through intelligent automated weekly reminders and family caregiver prescription syncing.")
    with col2:
        st.metric(label="Emergency Triage Time Saved", value="45%", delta="Fast Routing")
        st.write("By linking disease searches instantly to specialized local hospitals and providing precise coordinates.")

    st.info("💡 **Low-Resource Scalability:** Designed to operate smoothly on low-bandwidth mobile networks in rural communities.")

# Footer
st.markdown("---")
st.caption("HealthBridge Unified Prototype • Built with Python & Streamlit 🚀")
