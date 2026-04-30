import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide")

# --- 2. MOBILE ZOOM FIX ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f0f2f6; }
    div.stButton > button {
        height: 70px !important;
        border-radius: 12px !important;
        font-weight: bold;
        border: 2px solid #28a745 !important;
    }
    </style>
    <script>
    var meta = document.querySelector('meta[name="viewport"]');
    meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
    </script>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
# റൊട്ടേഷൻ സമയത്ത് പേജ് മാറാതെ ഇരിക്കാൻ ഇത് സഹായിക്കും
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

# --- 4. DATA ---
SYLLABUS = {
    "Statistics": {
        "Module 1-10": "Sampling, Probability, Distributions, Estimation, Testing, Regression, Time Series, Index Numbers, Vital Stats."
    },
    "Economics": {
        "Module 1-7": "Micro, Macro, Growth, Fiscal, Indian Economy, Kerala Economy, Econometrics."
    }
}

QUIZ_DATA = {
    "Economics": {
        "Set 1": [(f"Q{i}.png", ans) for i, ans in zip(range(1, 9), ["B", "B", "C", "C", "B", "C", "B", "B"])],
        "Set 2": [(f"Q{i}.png", ans) for i, ans in zip(range(10, 18), ["C", "B", "C", "B", "C", "C", "B", "B"])]
    }
}

# --- 5. APP LOGIC ---

# HOME PAGE
if st.session_state.page == "home":
    st.title("🎓 MATHS-STAT WORLD")
    if st.button("Research Officer", use_container_width=True):
        st.session_state.page = "subject_selection"
        st.rerun()

# SUBJECT SELECTION
elif st.session_state.page == "subject_selection":
    if st.button("⬅ Back Home"):
        st.session_state.page = "home"
        st.rerun()
    
    st.subheader("Select Subject")
    for sub in SYLLABUS.keys():
        if st.button(sub, use_container_width=True):
            st.session_state.current_sub = sub
            st.session_state.page = "options"
            st.rerun()

# OPTIONS PAGE
elif st.session_state.page == "options":
    if st.button("⬅ Back"):
        st.session_state.page = "subject_selection"
        st.rerun()
    
    st.title(f"📚 {st.session_state.current_sub}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Syllabus", use_container_width=True):
            st.session_state.page = "syllabus"
            st.rerun()
    with col2:
        if st.button("🎯 Practice", use_container_width=True):
            st.session_state.page = "practice"
            st.rerun()

# SYLLABUS PAGE
elif st.session_state.page == "syllabus":
    if st.button("⬅ Back"):
        st.session_state.page = "options"
        st.rerun()
    st.write(SYLLABUS[st.session_state.current_sub])

# PRACTICE PAGE
elif st.session_state.page == "practice":
    if st.button("⬅ Exit Quiz"):
        st.session_state.page = "options"
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        st.rerun()
    
    # Quiz rendering logic goes here using session_state to prevent reset
    st.info("ക്വിസ് ചോദ്യങ്ങൾ ലോഡ് ചെയ്യുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Maths-Stat World Hub</p>", unsafe_allow_html=True)