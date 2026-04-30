import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM & ROTATION SCRIPT ---
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
    .block-container { padding: 1rem; }
    .stApp { background-color: #f0f2f6; }
    .welcome-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    div.stButton > button {
        height: 70px !important;
        border-radius: 12px !important;
        font-weight: bold;
        border: 2px solid #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SAFE SESSION STATE INITIALIZATION ---
# ഫോൺ തിരിക്കുമ്പോൾ വേരിയബിളുകൾ നഷ്ടപ്പെടാതിരിക്കാൻ ഇത് നിർബന്ധമാണ്.
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = "Research Officer"
if 'current_subject' not in st.session_state: st.session_state.current_subject = "Statistics"
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False

# --- 5. COMPLETE SYLLABUS DATA ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF.",
            "MODULE 3: DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Normal.",
            "MODULE 4-10": "Estimation, Testing, Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function.",
            "Module II-VII": "Macro, Fiscal federalism, Indian Economy, Kerala Economy, Econometrics."
        }
    }
}

# --- 6. COMPLETE QUIZ BANK ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 7. NAVIGATION RENDERER ---

if st.session_state.page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        st.session_state.page = "exam_detail"
        st.rerun()

elif st.session_state.page == "exam_detail":
    if st.button("⬅ Back Home"):
        st.session_state.page = "home"
        st.rerun()
    
    # Safe value access to prevent AttributeError
    exam = st.session_state.get('current_exam', 'Research Officer')
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam}</h3></div>", unsafe_allow_html=True)
    
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"nav_{s}", use_container_width=True):
            st.session_state.current_subject = s
            st.session_state.page = "subject_options"
            st.rerun()

elif st.session_state.page == "subject_options":
    if st.button("⬅ Back"):
        st.session_state.page = "exam_detail"
        st.rerun()
    
    subject = st.session_state.get('current_subject', 'Statistics')
    st.markdown(f"<div class='welcome-banner'><h3>📚 {subject}</h3></div>", unsafe_allow_html=True)
    
    if st.button("📖 Syllabus", use_container_width=True):
        st.session_state.page = "syllabus_view"
        st.rerun()
    if st.button("🎯 Test Practice", use_container_width=True):
        st.session_state.page = "quiz_setup"
        st.rerun()

elif st.session_state.page == "syllabus_view":
    if st.button("⬅ Back"):
        st.session_state.page = "subject_options"
        st.rerun()
    
    subject = st.session_state.get('current_subject', 'Statistics')
    data = FULL_SYLLABUS.get(subject, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod):
            st.write(detail)

elif st.session_state.page == "quiz_setup":
    if st.button("⬅ Exit Quiz"):
        st.session_state.page = "subject_options"
        st.rerun()
    st.info("ക്വിസ് ചോദ്യങ്ങൾ തയ്യാറാകുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World</p>", unsafe_allow_html=True)