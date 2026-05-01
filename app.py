import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Maths-Stat World Pro", layout="wide", page_icon="🎓")

# --- 2. THE ULTIMATE FIX: URL PARAMETER ROUTING ---
# ഈ സെക്ഷൻ ബ്രൗസർ ലിങ്കിനെ (URL) അടിസ്ഥാനമാക്കി മാത്രം പ്രവർത്തിക്കുന്നു.
# അതിനാൽ ഫോൺ എത്ര തവണ തിരിച്ച് റീലോഡ് ആയാലും ബ്രൗസർ ലിങ്കിലെ അഡ്രസ് വഴി അതേ പേജ് തന്നെ ലോഡ് ചെയ്യും.

def get_status():
    # URL-ൽ നിന്ന് നിലവിലെ പേജും സബ്ജക്റ്റും എടുക്കുന്നു
    p = st.query_params.get("p", "home")
    s = st.query_params.get("s", "Statistics")
    return p, s

def go_to(page_name, subject_name=None):
    # പുതിയ പേജിലേക്ക് പോകുമ്പോൾ URL മാറ്റുന്നു
    st.query_params["p"] = page_name
    if subject_name:
        st.query_params["s"] = subject_name
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
    .banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA MANAGEMENT (NO SKIPPING) ---
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

QUIZ_BANK = {
    "Economics": {
        "Set 1": [(f"Q{i}.png", "Ans") for i in range(1, 9)],
        "Set 2": [(f"Q{i}.png", "Ans") for i in range(10, 18)]
    }
}

# --- 5. PAGE RENDERING LOGIC ---
current_p, current_s = get_status()

if current_p == "home":
    st.markdown("<div class='banner'><h2>🎓 MATHS-STAT WORLD</h2></div>", unsafe_allow_html=True)
    if st.button("Research Officer", use_container_width=True):
        go_to("exam_detail")

elif current_p == "exam_detail":
    if st.button("⬅ Back Home"): go_to("home")
    st.markdown("### 📍 Select Subject")
    for subject in FULL_SYLLABUS.keys():
        if st.button(subject, key=f"btn_{subject}", use_container_width=True):
            go_to("sub_options", subject_name=subject)

elif current_p == "sub_options":
    if st.button("⬅ Back"): go_to("exam_detail")
    st.markdown(f"<div class='banner'><h3>📚 {current_s}</h3></div>", unsafe_allow_html=True)
    if st.button("📖 Syllabus", use_container_width=True):
        go_to("syllabus_view", subject_name=current_s)
    if st.button("🎯 Test Practice", use_container_width=True):
        go_to("quiz_setup", subject_name=current_s)

elif current_p == "syllabus_view":
    if st.button("⬅ Back"): go_to("sub_options", subject_name=current_s)
    st.markdown(f"### {current_s} Syllabus")
    data = FULL_SYLLABUS.get(current_s, {"Modules": {}})
    for mod, detail in data["Modules"].items():
        with st.expander(mod):
            st.write(detail)

elif current_p == "quiz_setup":
    if st.button("⬅ Exit Quiz"): go_to("sub_options", subject_name=current_s)
    st.info(f"{current_s} ക്വിസ് ചോദ്യങ്ങൾ തയ്യാറാകുന്നു...")

st.markdown("<br><hr><p style='text-align: center;'>© 2026 Shakeelurahman OP</p>", unsafe_allow_html=True)