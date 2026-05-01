import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. THE ULTIMATE ROTATION FIX (QUERY PARAMS) ---
# ഈ സെക്ഷനാണ് താങ്കളുടെ ആപ്പിനെ സ്ക്രീൻ റൊട്ടേഷനിൽ നിന്ന് സംരക്ഷിക്കുന്നത്.
# ഇത് ഓരോ സെക്കൻഡിലും URL പരിശോധിക്കുകയും നിങ്ങൾ നിന്നിരുന്ന പേജ് തിരിച്ചുപിടിക്കുകയും ചെയ്യും.

def get_current_page():
    # URL-ൽ നിന്ന് നിലവിലെ പേജ് വിവരം എടുക്കുന്നു
    params = st.query_params
    return params.get("page", "home")

def navigate_to(page_name, extra_params=None):
    # പുതിയ പേജിലേക്ക് പോകുമ്പോൾ URL അഡ്രസ് മാറ്റുന്നു
    new_params = {"page": page_name}
    if extra_params:
        new_params.update(extra_params)
    st.query_params.from_dict(new_params)
    st.session_state.page = page_name
    st.rerun()

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    div.stButton > button {
        height: 70px !important; border-radius: 12px !important; 
        font-weight: bold; border: 2px solid #28a745 !important;
        background-color: white !important;
    }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA (SYLLABUS & QUIZ) ---
FULL_SYLLABUS = {
    "Statistics": {"Modules": {"MODULE 1-10": "Sampling, Probability, Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Stats."}},
    "Economics": {"Modules": {"Module I: Micro Theory": "Indifference Curve, Consumer's Surplus, Production Function.", "Module II-VII": "Macro, Fiscal, Indian & Kerala Economy, Econometrics."}}
}

# --- 5. UI RENDERER BASED ON URL ---
current_page = get_current_page()

if current_page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate_to("exam_detail")

elif current_page == "exam_detail":
    if st.button("⬅ Back Home"):
        navigate_to("home")
    st.markdown("<div class='welcome-banner'><h3>📍 Select Subject</h3></div>", unsafe_allow_html=True)
    for s in FULL_SYLLABUS.keys():
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate_to("sub_options", extra_params={"sub": s})

elif current_page == "sub_options":
    selected_sub = st.query_params.get("sub", "Statistics")
    if st.button("⬅ Back"):
        navigate_to("exam_detail")
    st.markdown(f"<div class='welcome-banner'><h3>📚 {selected_sub}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True):
        navigate_to("syllabus_view", extra_params={"sub": selected_sub})
    if st.button("🎯 Test Practice", use_container_width=True):
        navigate_to("quiz_setup", extra_params={"sub": selected_sub})

elif current_page == "syllabus_view":
    selected_sub = st.query_params.get("sub", "Statistics")
    if st.button("⬅ Back"):
        navigate_to("sub_options", extra_params={"sub": selected_sub})
    st.markdown(f"### {selected_sub} Syllabus")
    st.write(FULL_SYLLABUS.get(selected_sub, {}).get("Modules", {}))

elif current_page == "quiz_setup":
    selected_sub = st.query_params.get("sub", "Statistics")
    if st.button("⬅ Exit Quiz"):
        navigate_to("sub_options", extra_params={"sub": selected_sub})
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Shakeelurahman OP</p>", unsafe_allow_html=True)