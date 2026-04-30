import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. CSS FOR STABILITY ---
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
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ERROR-PROOF SESSION INITIALIZATION ---
# പേജ് ലോഡ് ചെയ്യുമ്പോൾ തന്നെ എല്ലാ വേരിയബിളുകളും ഉറപ്പാക്കുന്നു
if 'page' not in st.session_state: st.session_state.page = "home"
if 'current_exam' not in st.session_state: st.session_state.current_exam = "Research Officer"
if 'current_subject' not in st.session_state: st.session_state.current_subject = "Statistics"

# --- 4. COMPLETE SYLLABUS DATA (NO SKIPPING) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF, Characteristic function.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Exponential, Normal.",
            "MODULE 4-10": "Estimation, Testing, Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function (Cobb-Douglas, CES), Welfare Economics.",
            "Module II-VII": "Macro, Fiscal federalism, Indian Economy, Kerala Economy, Econometrics."
        }
    }
}

# --- 5. COMPLETE QUIZ BANK (SET 1 & 2) ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 6. NAVIGATION LOGIC ---
def navigate(target_page, exam=None, sub=None):
    st.session_state.page = target_page
    if exam: st.session_state.current_exam = exam
    if sub: st.session_state.current_subject = sub
    st.rerun()

# --- 7. UI RENDERER ---
# AttributeError തടയാൻ safe access ഉപയോഗിക്കുന്നു
page = st.session_state.get('page', 'home')
exam = st.session_state.get('current_exam', 'Research Officer')
subject = st.session_state.get('current_subject', 'Statistics')

if page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        navigate("exam_detail", exam="Research Officer")

elif page == "exam_detail":
    if st.button("⬅ Back Home"): navigate("home")
    st.markdown(f"<div class='welcome-banner'><h3>📍 {exam}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            navigate("subject_options", sub=s)

elif page == "subject_options":
    if st.button("⬅ Back"): navigate("exam_detail")
    st.markdown(f"<div class='welcome-banner'><h3>📚 {subject}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True): navigate("syllabus_view")
    if st.button("🎯 Test Practice", use_container_width=True): navigate("quiz_setup")

elif page == "syllabus_view":
    if st.button("⬅ Back"): navigate("subject_options")
    st.markdown(f"<div class='welcome-banner'><h3>📖 {subject} Syllabus</h3></div>", unsafe_allow_html=True)
    data = FULL_SYLLABUS.get(subject, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod): st.write(detail)

elif page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate("subject_options")
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)