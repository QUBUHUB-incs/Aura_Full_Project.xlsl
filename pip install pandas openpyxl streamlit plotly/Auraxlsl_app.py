import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (The "Aura" Aesthetic)
st.set_page_config(page_title="AURA Full Project", layout="wide", initial_sidebar_state="expanded")

# 2. Data Connection (Replacing the old NaCl complexity)
@st.cache_data
def load_data():
    # Replace with your actual filename
    return pd.read_excel("Aura_Full_Project.xlsx")

try:
    df = load_data()
except:
    st.error("Please ensure 'Aura_Full_Project.xlsx' is in the same folder as this script.")
    st.stop()

# 3. Sidebar Navigation
st.sidebar.title("AURA CONTROL")
menu = st.sidebar.radio("Modules", ["Research Overview", "Data Analytics", "Update Database"])

# 4. Main UI Logic
if menu == "Research Overview":
    st.title("🌌 Aura Research Suite")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodes Active", len(df))
    col2.metric("Project Status", "Stable")
    col3.metric("Data Sync", "Live")
    
    st.subheader("Raw Research Data")
    st.dataframe(df, use_container_width=True)

elif menu == "Data Analytics":
    st.title("📊 Computational Analytics")
    # Automatically generates a chart based on your spreadsheet columns
    if not df.empty:
        fig = px.area(df, template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Update Database":
    st.title("⚙️ System Configuration")
    st.info("Edit your research data below. Changes are saved directly to the .xlsl source.")
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("Commit Changes to Aura"):
        edited_df.to_excel("Aura_Full_Project.xlsx", index=False)
        st.success("Aura Database Updated!")
