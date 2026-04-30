import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. GLOBAL MOBILE ZOOM & ROTATION FIX ---
# പേജ് റൊട്ടേറ്റ് ചെയ്യുമ്പോൾ സ്റ്റേറ്റ് നഷ്ടപ്പെടാതിരിക്കാൻ ഇത് സഹായിക്കും
st.markdown("""
    <script>
    var meta = document.querySelector('meta[name="viewport"]');
    if (meta) {
        meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
    }
    </script>
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    div.stButton > button {
        height: 75px !important;
        background-color: white !important;
        color: #1e3c72 !important;
        border: 2px solid #28a745 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }
    .q-header {
        background-color: #1e3c72;
        color: white;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state: st.session_state.quiz_submitted = False

# --- 4. FULL SYLLABUS DATA ---
FULL_SYLLABUS = {
    "Statistics": {
        "Modules": {
            "MODULE 1: SAMPLING (6 marks)": "Random Sampling, Stratified sampling, Ratio/Regression estimator.",
            "MODULE 2: PROBABILITY (3 marks)": "Probability measure, Independence, Bayes theorem, CDF, PDF, MGF.",
            "MODULE 3: STANDARD DISTRIBUTIONS (2 marks)": "Uniform, Bernoulli, Binomial, Poisson, Exponential, Normal.",
            "MODULE 4-10": "Estimation, Testing, Regression, Time Series, Index Numbers, Vital Statistics."
        }
    },
    "Economics": {
        "Modules": {
            "Module I: Micro Theory (4 marks)": "Indifference Curve, Consumer's Surplus, Production Function (Cobb-Douglas, CES).",
            "Module II-VII": "Macro, Fiscal federalism, Indian & Kerala Economy, Econometrics."
        }
    }
}

# --- 5. FULL QUIZ BANK ---
QUIZ_BANK = {
    "Economics": {
        "Module I: Micro Theory (4 marks)": {
            "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
            "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
        }
    }
}

# --- 6. APP LOGIC ---

if st.session_state.page == "home":
    st.markdown("<h2 style='text-align: center;'>🎓 MATHS-STAT WORLD</h2>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        st.session_state.page = "subject_options"
        st.rerun()

elif st.session_state.page == "subject_options":
    if st.button("⬅ Back Home"):
        st.session_state.page = "home"
        st.rerun()
    
    st.subheader("Select Subject")
    for sub in FULL_SYLLABUS.keys():
        if st.button(sub, use_container_width=True):
            st.session_state.current_sub = sub
            st.session_state.page = "sub_menu"
            st.rerun()

elif st.session_state.page == "sub_menu":
    if st.button("⬅ Back"):
        st.session_state.page = "subject_options"
        st.rerun()
    
    st.title(f"📚 {st.session_state.current_sub}")
    if st.button("📖 Syllabus", use_container_width=True):
        st.session_state.page = "syllabus"
        st.rerun()
    if st.button("🎯 Test Practice", use_container_width=True):
        st.session_state.page = "practice"
        st.rerun()

elif st.session_state.page == "syllabus":
    if st.button("⬅ Back"):
        st.session_state.page = "sub_menu"
        st.rerun()
    
    data = FULL_SYLLABUS[st.session_state.current_sub]
    for mod, detail in data["Modules"].items():
        with st.expander(mod):
            st.write(detail)

elif st.session_state.page == "practice":
    if st.button("⬅ Exit Quiz"):
        st.session_state.page = "sub_menu"
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.rerun()
    
    # Quiz logic here
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center; color: grey;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)