import streamlit as st
import pandas as pd
import plotly.express as px
from auth import connect_db

def admin_dashboard():
    st.title("📊 Admin Dashboard – IntelliMed")
    st.markdown("Welcome Admin! Here's a real-time overview of user activity and scan history.")

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Users
    cursor.execute("SELECT username, role, created_at FROM users ORDER BY created_at DESC")
    users_data = pd.DataFrame(cursor.fetchall())

    # Scan Logs
    cursor.execute("SELECT username, scan_type, result, confidence, timestamp FROM scan_logs ORDER BY timestamp DESC")
    logs_data = pd.DataFrame(cursor.fetchall())

    conn.close()

    st.subheader("👥 Registered Users")
    if not users_data.empty:
        st.dataframe(users_data)
    else:
        st.info("No users yet.")

    st.subheader("🧪 Scan Activity")
    if not logs_data.empty:
        st.dataframe(logs_data)

        # Bar: scans per user
        st.markdown("### 👤 Scans per User")
        scan_count = logs_data['username'].value_counts().reset_index()
        scan_count.columns = ['Username', 'Total Scans']
        st.plotly_chart(px.bar(scan_count, x='Username', y='Total Scans', color='Username'))

        # Pie: scan type distribution
        st.markdown("### 🔬 Scan Types")
        scan_types = logs_data['scan_type'].value_counts().reset_index()
        scan_types.columns = ['Scan Type', 'Count']
        st.plotly_chart(px.pie(scan_types, names='Scan Type', values='Count'))

        # Line: scan volume over time
        st.markdown("### 📆 Scans Over Time")
        logs_data['timestamp'] = pd.to_datetime(logs_data['timestamp'])
        time_series = logs_data.groupby(logs_data['timestamp'].dt.date).size().reset_index(name='Scan Count')
        st.plotly_chart(px.line(time_series, x='timestamp', y='Scan Count', markers=True))
    else:
        st.info("No scans yet.")
