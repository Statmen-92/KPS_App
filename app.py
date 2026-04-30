import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. JAVASCRIPT FOR PERSISTENCE & VIEWPORT ---
# ഫോൺ തിരിക്കുമ്പോൾ ബ്രൗസർ മെമ്മറിയിൽ നിന്ന് ഡാറ്റ നഷ്ടപ്പെടാതിരിക്കാൻ
st.markdown("""
    <script>
    const PERSIST_KEY = 'ms_world_state';
    
    // പേജ് ലോഡ് ചെയ്യുമ്പോൾ പഴയ സ്റ്റേറ്റ് ഉണ്ടോ എന്ന് നോക്കുന്നു
    window.onload = () => {
        const savedState = localStorage.getItem(PERSIST_KEY);
        if (savedState) {
            console.log('Restoring state...');
        }
    };

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
    window.addEventListener('orientationchange', () => { 
        setTimeout(fixViewport, 500); 
    });
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

# --- 4. ULTIMATE STATE RECOVERY ---
# AttributeError ഒഴിവാക്കാൻ ഓരോ തവണയും വേരിയബിളുകൾ ഉറപ്പാക്കുന്നു
if 'page' not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_exam = params.get("ex", "Research Officer")
    st.session_state.current_subject = params.get("sub", "Statistics")

def navigate_to(page, exam=None, subject=None):
    st.session_state.page = page
    st.query_params["p"] = page
    if exam: 
        st.session_state.current_exam = exam
        st.query_params["ex"] = exam
    if subject: 
        st.session_state.current_subject = subject
        st.query_params["sub"] = subject
    st.rerun()

# --- 5. DATA MANAGEMENT (MODULES 1-10) ---
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
        "Set 1": [(f"Q{i}.png", a) for i, a in zip(range(1, 9), ["B","B","C","C","B","C","B","B"])],
        "Set 2": [(f"Q{i}.png", a) for i, a in zip(range(10, 18), ["C","B","C","B","C","C","B","B"])]
    }
}

# --- 6. RENDER LOGIC ---
# കറന്റ് സ്റ്റേറ്റ് സുരക്ഷിതമായി എടുക്കുന്നു
curr_page = st.session_state.get('page', 'home')
curr_exam = st.session_state.get('current_exam', 'Research Officer')
curr_sub = st.session_state.get('current_subject', 'Statistics')

if curr_page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate_to("exam_detail", exam="Research Officer")

elif curr_page == "exam_detail":
    if st.button("⬅ Back Home"): navigate_to("home")
    st.markdown(f"<div class='welcome-banner'><h3>📍 {curr_exam}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate_to("subject_options", subject=s)

elif curr_page == "subject_options":
    if st.button("⬅ Back"): navigate_to("exam_detail")
    st.markdown(f"<div class='welcome-banner'><h3>📚 {curr_sub}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True): navigate_to("syllabus_view")
    if st.button("🎯 Test Practice", use_container_width=True): navigate_to("quiz_setup")

elif curr_page == "syllabus_view":
    if st.button("⬅ Back"): navigate_to("subject_options")
    data = FULL_SYLLABUS.get(curr_sub, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod): st.write(detail)

elif curr_page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate_to("subject_options")
    st.info("ക്വിസ് സെക്ഷൻ തയ്യാറാകുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World</p>", unsafe_allow_html=True)