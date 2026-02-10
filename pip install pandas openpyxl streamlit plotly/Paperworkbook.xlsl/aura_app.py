import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aura Research Suite", layout="wide")

st.title("Aura Full Project | STEM Research Portal")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a Module", ["Dashboard", "Data Entry", "AI Analytics"])

# Load Data
df = pd.read_excel("Aura_Full_Project.xlsx")

if page == "Dashboard":
    st.subheader("Live Research Metrics")
    # Create an interactive chart instantly
    fig = px.line(df, x=df.columns[0], y=df.columns[1], template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Data Entry":
    st.subheader("Update Project Data")
    edited_df = st.data_editor(df) # Allows live editing in the UI
    if st.button("Save Changes to Aura System"):
        edited_df.to_excel("Aura_Full_Project.xlsx", index=False)
        st.success("Data Synchronized!")
