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
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.7);
        color: #ffffff;
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 12px;
    }
    .stTextInput input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
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

    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 18px;
        border-radius: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "meds" not in st.session_state:
    st.session_state.meds = [
        {"name": "Metformin (500mg)", "time": "08:00 AM", "status": "Pending", "category": "Diabetes"},
        {"name": "Amlodipine (5mg)", "time": "01:00 PM", "status": "Pending", "category": "Blood Pressure"},
        {"name": "Vitamin D3 Supplement", "time": "08:00 PM", "status": "Pending", "category": "Wellness"}
    ]

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
st.sidebar.info("💡 **Demo Tip:** Search 'Heart', 'Eye', or 'Bones' to see custom hospital pins and live route animations!")

# ----------------------------------------------------
# 1. UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
if app_mode == "🏥 Unified Health & Hospital Hub":
    st.title("🌟 HealthBridge: Unified Patient Companion")
    st.markdown("*Combining intelligent emergency hospital routing, live map pins, custom routes, and medication tracking.*")
    st.divider()

    st.subheader("🔍 Disease-to-Hospital Intelligent Map & Route Finder")
    
    user_disease_input = st.text_input(
        "Enter disease/symptom:",
        placeholder="Type condition here... (e.g., Heart, Eye, Bones)",
        key="map_disease_search"
    )

    # Default coordinates (Kolhapur Region)
    user_lon, user_lat = 74.2400, 16.7000  # User simulated location
    h_lat, h_lon = 16.7050, 74.2433
    h_name = "Aster Aadhar Hospital (Cardiology)"
    travel_info = "~3.2 km away | 8 mins via NH48"

    query = (user_disease_input or "").lower().strip()
    
    if "heart" in query or "cardio" in query or "chest" in query or "stroke" in query:
        h_lat, h_lon = 16.7050, 74.2433
        h_name = "Aster Aadhar Hospital (Cardiology)"
        travel_info = "~3.2 km away | 8 mins via NH48"
        st.error("⚠️ **Specialty Match: Cardiology & Emergency Cardiac Unit**")
    elif "eye" in query or "vision" in query or "cataract" in query:
        h_lat, h_lon = 16.7120, 74.2500
        h_name = "Nandadeep Eye Hospital"
        travel_info = "~4.5 km away | 12 mins via Tarabai Park Road"
        st.warning("👁️ **Specialty Match: Ophthalmology & Vision Care**")
    elif "bone" in query or "fracture" in query or "ortho" in query or "joint" in query:
        h_lat, h_lon = 16.7200, 74.4600
        h_name = "Dr. Lande Fracture Hospital"
        travel_info = "~6.0 km away | 15 mins via Main Road"
        st.info("🦴 **Specialty Match: Orthopedics & Trauma Center**")
    else:
        h_lat, h_lon = 16.6900, 74.2200
        h_name = "Alliance Multispeciality Hospital"
        travel_info = "~2.1 km away | 5 mins via City Road"
        if user_disease_input:
            st.success("🏥 **General Multi-Specialty Care**")

    st.info(f"🚗 **Selected Route to {h_name}:** {travel_info}")

    # --- Fixed PyDeck Map Layer Configuration ---
    # User location pin (Blue) and Hospital pin (Orange-Red) with explicit sizes and RGB colors
    map_data = pd.DataFrame([
        {
            "latitude": user_lat, 
            "longitude": user_lon, 
            "name": "Your Location (Patient)", 
            "color": [30, 144, 255, 220],  # Dodger Blue
            "radius": 180
        },
        {
            "latitude": h_lat, 
            "longitude": h_lon, 
            "name": h_name, 
            "color": [255, 69, 0, 220],     # Orange Red
            "radius": 220
        }
    ])

    route_data = pd.DataFrame([
        {
            "path": [[user_lon, user_lat], [h_lon, h_lat]]
        }
    ])

    # Layers for PyDeck
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

    path_layer = pdk.Layer(
        "PathLayer",
        route_data,
        get_path="path",
        get_color=[255, 140, 0],  # Vibrant orange route line
        width_scale=20,
        width_min_pixels=6,
    )

    view_state = pdk.ViewState(
        latitude=(user_lat + h_lat) / 2,
        longitude=(user_lon + h_lon) / 2,
        zoom=13.5,
        pitch=25,
    )

    r = pdk.Deck(
        layers=[path_layer, scatterplot_layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"},
        map_style="mapbox://styles/mapbox/dark-v10"
    )

    st.pydeck_chart(r, use_container_width=True)
    st.caption("📍 Blue Pin = Your Location | 🟠 Orange Pin = Recommended Hospital | 🟠 Orange Line = Live Travel Route")

    st.divider()

    # Medication & Questions Section
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💊 Today's Medication Reminders")
        for i, med in enumerate(st.session_state.meds):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write(f"**{med['name']}**")
                st.caption(f"Time: {med['time']} | {med['status']}")
            with c2:
                if med['status'] == "Pending":
                    if st.button("Mark Taken", key=f"med_taken_{i}"):
                        st.session_state.meds[i]['status'] = "Taken ✅"
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
    st.title("👁️ Caregiver Real-Time Monitor Link")
    st.markdown("Secure portal for family members to monitor patient adherence and health status remotely.")
    st.divider()

    password_input = st.text_input("🔒 Enter Caregiver Access Password:", type="password", placeholder="Enter PIN (Demo PIN: 1234)")
    
    if password_input == "1234":
        st.success("🔓 Access Granted! Connected to Patient Profile #PAT-8821")
        
        df_caregiver = pd.DataFrame(st.session_state.meds)
        st.table(df_caregiver)
        
        st.metric(label="Patient Adherence Rate (Past 7 Days)", value="92%", delta="+4% improvement")
        
        with st.form("caregiver_alert"):
            msg = st.text_area("Send an encouraging note or reminder to the patient:", placeholder="Dad, great job taking your medicine today!")
            if st.form_submit_button("Send Push Notification"):
                st.success("✅ Notification successfully sent to patient device!")
    elif password_input:
        st.error("❌ Incorrect password. Please check with the patient for the correct PIN.")
    else:
        st.info("ℹ️ Please enter the caregiver PIN to unlock live tracking data.")

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
        st.write("Through intelligent automated reminders and family caregiver syncing.")
    with col2:
        st.metric(label="Emergency Triage Time Saved", value="45%", delta="Fast Routing & Distance Calc")
        st.write("By linking disease searches instantly to specialized local hospitals and providing direct transit routes.")

    st.info("💡 **Low-Resource Scalability:** Designed to operate smoothly on low-bandwidth mobile networks in rural communities.")

# Footer
st.markdown("---")
st.caption("HealthBridge Unified Prototype • Built with Python & Streamlit 🚀")
