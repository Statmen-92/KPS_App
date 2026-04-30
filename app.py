import streamlit as st
import os

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
        height: 75px !important;
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #28a745 !important;
        border-radius: 12px !important;
        font-weight: bold;
    }
    .q-header {
        background-color: #1e3c72;
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PERSISTENT NAVIGATION (URL LOCK) ---
if 'page' not in st.session_state:
    params = st.query_params
    st.session_state.page = params.get("p", "home")
    st.session_state.current_exam = params.get("ex", None)
    st.session_state.current_subject = params.get("sub", None)
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False

def navigate_to(page, exam=None, subject=None):
    st.session_state.page = page
    st.query_params["p"] = page
    if exam: st.query_params["ex"] = exam
    if subject: st.query_params["sub"] = subject
    st.rerun()

# --- 5. COMPLETE SYLLABUS DATA (MODULES 1-10) ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling methods, Simple random sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF.",
            "MODULE 3: DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Exponential, Normal.",
            "MODULE 4-10": "Sampling Distributions, Estimation, Testing of Hypothesis, Linear Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function (Cobb-Douglas, CES).",
            "Module II-VII": "Macro Economics, Fiscal Federalism, Indian Economy, Kerala Economy, Econometrics."
        }
    }
}

# --- 6. COMPLETE QUIZ BANK (SET 1 & 2) ---
QUIZ_BANK = {
    "Statistics": {
        "MODULE 2: PROBABILITY (3 marks)": {
            "Set 1": [(os.path.join("Research Officer", "Statistics", "Module 2", "Set 1", "Questions", f"{i}.png"), ans, "") for i, ans in zip(range(1, 11), ["C", "A", "C", "D", "B", "C", "A", "B", "A", "A"])]
        }
    },
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(os.path.join("Research Officer", "Economics", "Module 1", "Set 1", "Questions", f"{i}.png"), ans, "") for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(os.path.join("Research Officer", "Economics", "Module 1", "Set 2", "Questions", f"{i}.png"), ans, "") for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 7. UI RENDERER ---
if st.session_state.page == "home":
    st.markdown("<div class='welcome-banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    exams = ["Research Officer", "HSST Stat", "CSIR NET", "HSST Maths", "HSA Maths"]
    cols = st.columns(2)
    for i, ex in enumerate(exams):
        with cols[i % 2]:
            if st.button(ex, key=f"btn_{ex}", use_container_width=True):
                navigate_to("exam_detail", exam=ex)

elif st.session_state.page == "exam_detail":
    if st.button("⬅ Back Home"): navigate_to("home")
    st.markdown(f"<div class='welcome-banner'><h3>📍 {st.session_state.current_exam}</h3></div>", unsafe_allow_html=True)
    for s in ["Statistics", "Economics", "Mathematics", "Commerce"]:
        if st.button(s, key=f"sub_{s}", use_container_width=True):
            navigate_to("subject_options", subject=s)

elif st.session_state.page == "subject_options":
    if st.button("⬅ Back"): navigate_to("exam_detail", exam=st.session_state.current_exam)
    st.markdown(f"<div class='welcome-banner'><h3>📚 {st.session_state.current_subject}</h3></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        if st.button("📖 Syllabus", use_container_width=True): navigate_to("syllabus_view", subject=st.session_state.current_subject)
    with cols[1]:
        if st.button("🎯 Test Practice", use_container_width=True): navigate_to("quiz_setup", subject=st.session_state.current_subject)

elif st.session_state.page == "syllabus_view":
    if st.button("⬅ Back"): navigate_to("subject_options", subject=st.session_state.current_subject)
    data = FULL_SYLLABUS.get(st.session_state.current_subject, {"Modules": {}})
    for section, detail in data['Modules'].items():
        with st.expander(section): st.write(detail)

elif st.session_state.page == "quiz_setup":
    if st.button("⬅ Exit Quiz"): navigate_to("subject_options", subject=st.session_state.current_subject)
    mod_opts = list(FULL_SYLLABUS.get(st.session_state.current_subject, {"Modules": {}})["Modules"].keys())
    sel_mod = st.selectbox("Select Module:", mod_opts)
    sel_set = st.radio("Set:", ["Set 1", "Set 2"], horizontal=True)
    
    active_data = QUIZ_BANK.get(st.session_state.current_subject, {}).get(sel_mod, {}).get(sel_set)
    if active_data:
        for i, (q_img, cor, _) in enumerate(active_data):
            st.markdown(f"<div class='q-header'>Question {i + 1}</div>", unsafe_allow_html=True)
            if os.path.exists(q_img): st.image(q_img, use_container_width=True)
            st.radio("Answer:", ["A", "B", "C", "D"], index=None, key=f"q_{sel_mod}_{sel_set}_{i}")
    else:
        st.warning("Materials coming soon!")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)