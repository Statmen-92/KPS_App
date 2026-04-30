import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM & ORIENTATION FIX ---
st.markdown("""
    <script>
    const fixViewport = () => {
        var meta = document.querySelector('meta[name="viewport"]');
        if (!meta) {
            meta = document.createElement('meta');
            meta.name = 'viewport';
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
        meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
    };
    fixViewport();
    window.addEventListener('orientationchange', () => { setTimeout(fixViewport, 500); });
    </script>
    """, unsafe_allow_html=True)

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    div.stButton > button {
        height: 70px !important; border-radius: 12px !important; 
        font-weight: bold; border: 2px solid #28a745 !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PERSISTENT NAVIGATION (URL SYNC) ---
# ഈ സെക്ഷനാണ് ഫോൺ റൊട്ടേറ്റ് ചെയ്യുമ്പോൾ പേജ് ഹോം സ്ക്രീനിലേക്ക് പോകുന്നത് തടയുന്നത്.
if 'page' not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_exam = params.get("ex", "Research Officer")
    st.session_state.current_sub = params.get("sub", "Statistics")

def navigate_to(page, exam=None, sub=None):
    st.session_state.page = page
    st.query_params["p"] = page
    if exam: 
        st.session_state.current_exam = exam
        st.query_params["ex"] = exam
    if sub: 
        st.session_state.current_sub = sub
        st.query_params["sub"] = sub
    st.rerun()

# --- 5. DATA (NO SKIPPING) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1-5": "Sampling, Probability, Distributions, Estimation.",
            "MODULE 6-10": "Testing, Regression, Time Series, Index Numbers, Vital Stats."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory": "Indifference Curve, Consumer's Surplus, Production Function.",
            "Module II-VII": "Macro, Fiscal, Indian & Kerala Economy, Econometrics."
        }
    }
}

QUIZ_DATA = {
    "Economics": {
        "Set 1": [("Q1.png", "B"), ("Q2.png", "B")], # (താങ്കളുടെ ബാക്കി ചോദ്യങ്ങൾ ഇവിടെ ചേർക്കാവുന്നതാണ്)
        "Set 2": [("Q10.png", "C"), ("Q11.png", "B")]
    }
}

# --- 6. NAVIGATION LOGIC ---
# AttributeError ഒഴിവാക്കാൻ get() മെത്തേഡ് ഉപയോഗിക്കുന്നു.
curr_page = st.session_state.get('page', 'home')
curr_exam = st.session_state.get('current_exam', 'Research Officer')
curr_sub = st.session_state.get('current_sub', 'Statistics')

if curr_page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate_to("exam_detail", exam="Research Officer")

elif curr_page == "exam_detail":
    if st.button("⬅ Back Home"): navigate_to("home")
    st.markdown(f"<div class='welcome-banner'><h3>📍 {curr_exam}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"nav_{s}", use_container_width=True):
            navigate_to("subject_options", sub=s)

elif curr_page == "subject_options":
    if st.button("⬅ Back"): navigate_to("exam_detail")
    st.markdown(f"<div class='welcome-banner'><h3>📚 {curr_sub}</h3></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Syllabus", use_container_width=True): navigate_to("syllabus_view")
    with col2:
        if st.button("🎯 Test Practice", use_container_width=True): navigate_to("quiz_setup")

elif curr_page == "syllabus_view":
    if st.button("⬅ Back"): navigate_to("subject_options")
    data = FULL_SYLLABUS.get(curr_sub, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod): st.write(detail)

elif curr_page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate_to("subject_options")
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World</p>", unsafe_allow_html=True)