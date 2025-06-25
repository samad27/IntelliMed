import streamlit as st
import pandas as pd
import test 
import numpy as np
from test import predict_ecg
from auth import log_scan_result

def app():
    st.title('❤️ ECG Arrhythmia Classification')
    st.write('Upload your ECG data in CSV format')

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        ecg_data = df.values

        predictions = predict_ecg(ecg_data)
        pred_df = pd.DataFrame({"Predicted Classes": predictions})
        
        st.write("Predicted Classes:")
        st.table(pred_df)

        st.write("🔐 Current User:", st.session_state.get('username'))

        if 'username' in st.session_state and st.session_state['username']:
            try:
                for result in predictions:
                    log_scan_result(
                        st.session_state['username'],
                        "ECG Analysis",
                        result,
                        0.0  # No confidence available
                    )
                st.success("✅ ECG scan results logged to dashboard.")
            except Exception as e:
                st.error(f"❌ Failed to log ECG scan: {e}")
        else:
            st.warning("⚠️ No user session found. Please log in before scanning.")
