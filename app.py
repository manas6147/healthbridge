import streamlit as st
import pandas as pd

# App Config & Custom Styling for Background
st.set_page_config(
    page_title="HealthBridge - Unified SDG 3 Companion", 
    page_icon="🏥", 
    layout="wide"
)

# Custom CSS for styling the dashboard and background feel
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stSidebar {
        background-color: #e9ecef;
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
st.sidebar.info("💡 **Demo Tip:** Search 'Heart', 'Eye', or 'Bones' to find specialized hospitals, routes, and distance estimates!")

# ----------------------------------------------------
# 1. UNIFIED HEALTH & HOSPITAL HUB
# ----------------------------------------------------
if app_mode == "🏥 Unified Health & Hospital Hub":
    st.title("🌟 HealthBridge: Unified Patient Companion")
    st.markdown("*Combining intelligent emergency hospital routing, live distance tracking, and daily medication adherence.*")
    st.divider()

    st.subheader("🔍 Disease-to-Hospital Intelligent Map & Route Finder")
    
    user_disease_input = st.text_input(
        "Enter disease/symptom:",
        placeholder="Type condition here... (e.g., Heart, Eye, Bones)",
        key="map_disease_search"
    )

    # Default coordinates (Kolhapur region)
    lat_list = [16.7050, 16.6900, 16.7120, 16.7200]
    lon_list = [74.2433, 74.2200, 74.2500, 74.4600]
    name_list = [
        "Aster Aadhar Hospital (Cardiology)", 
        "Alliance Multispeciality Hospital", 
        "Nandadeep Eye Hospital", 
        "Dr. Lande Fracture Hospital"
    ]

    if user_disease_input:
        query = user_disease_input.lower().strip()
        st.markdown(f"### 🏥 Best Specialized Recommendations & Routes for: *'{user_disease_input}'*")
        
        if any(k in query for k in ["heart", "cardio", "chest", "bp", "stroke"]):
            st.error("⚠️ **Specialty Match: Cardiology & Emergency Cardiac Unit**")
            st.write("1. **Aster Aadhar Hospital** (Kolhapur)")
            st.info("🚗 **Route & Distance:** ~3.2 km away | Estimated Travel Time: **8 mins** via NH48 | 📍 *Building Type: Multi-story Modern Medical Center*")
            lat_list, lon_list, name_list = [16.7050], [74.2433], ["Aster Aadhar Hospital (Cardiology Center)"]
            
        elif any(k in query for k in ["eye", "vision", "cataract", "blur"]):
            st.warning("👁️ **Specialty Match: Ophthalmology & Vision Care**")
            st.write("1. **Nandadeep Eye Hospital** (Kolhapur)")
            st.info("🚗 **Route & Distance:** ~4.5 km away | Estimated Travel Time: **12 mins** via Tarabai Park Road | 📍 *Building Type: Specialized Eye Care Clinic*")
            lat_list, lon_list, name_list = [16.7120], [74.2500], ["Nandadeep Eye Hospital (Vision Center)"]
            
        elif any(k in query for k in ["bone", "fracture", "ortho", "joint", "knee"]):
            st.info("🦴 **Specialty Match: Orthopedics & Trauma Center**")
            st.write("1. **Dr. Lande Fracture Hospital** (Ichalkaranji)")
            st.info("🚗 **Route & Distance:** ~6.0 km away | Estimated Travel Time: **15 mins** via Main Road | 📍 *Building Type: Dedicated Trauma & Orthopedic Wing*")
            lat_list, lon_list, name_list = [16.7200], [74.4600], ["Dr. Lande Fracture Hospital"]
            
        else:
            st.success("🏥 **General Multi-Specialty Care**")
            st.write("1. **Alliance Multispeciality Hospital** (Ichalkaranji)")
            st.info("🚗 **Route & Distance:** ~2.1 km away | Estimated Travel Time: **5 mins** | 📍 *Building Type: General Hospital Complex*")
    else:
        st.caption("💡 *Type a condition above to view precise routes, distance, and specialized hospital pins on the map.*")

    # Render Live Interactive Map
    df_map = pd.DataFrame({"lat": lat_list, "lon": lon_list, "Location": name_list})
    st.map(df_map, zoom=12, use_container_width=True)

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

    # Password protection check
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
