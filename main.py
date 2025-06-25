import streamlit as st
from streamlit_option_menu import option_menu

from auth import init_db, login_form, registration_form
from admin_dashboard import admin_dashboard

from auth import log_scan_result

import brain_cancer_detection, skin_cancer_detection, lung_cancer_detection, alzheimers_detection, chatbot, ecg_analysis

st.set_page_config(page_icon="⚕️", page_title="IntelliMed")

# ✅ Init DB
init_db()






# ✅ Session Init
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None

# ✅ START SCREEN
if not st.session_state['logged_in']:
    st.title("Welcome to IntelliMed")
    st.markdown("### Please choose an option to proceed:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Admin Login", key="admin_btn"):
            st.session_state['login_type'] = 'admin'
    with col2:
        if st.button("User Login", key="user_btn"):
            st.session_state['login_type'] = 'user'
    with col3:
        if st.button("Register", key="register_btn"):
            st.session_state['login_type'] = 'register'

    login_type = st.session_state.get('login_type')
    if login_type == 'admin':
        login_form('admin')
    elif login_type == 'user':
        login_form('user')
    elif login_type == 'register':
        registration_form()

# ✅ AFTER LOGIN
else:
    if st.session_state['role'] == 'admin':
        admin_dashboard()
    else:
        with st.sidebar:
            app = option_menu(
                menu_title="IntelliMed",
                options=['HealthBot', 'Brain Tumor Detection', 'Skin Cancer Detection', 'Lung Cancer Detection', 'Alzheimer\'s Detection', "ECG Analysis"],
                icons=['robot','headset-vr','droplet-fill','lungs-fill','alexa', 'heart-pulse-fill'],
                menu_icon='hospital-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color":"black"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color":"white", "font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "HealthBot":
            chatbot.run_chatbot()
        if app == "Brain Tumor Detection":
            brain_cancer_detection.app()
        if app == "Skin Cancer Detection":
            skin_cancer_detection.app()
        if app == "Lung Cancer Detection":
            lung_cancer_detection.app()
        if app == "Alzheimer's Detection":
            alzheimers_detection.app()
        if app == "ECG Analysis":
            ecg_analysis.app()
