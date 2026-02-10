import streamlit as st
import pandas as pd
import plotly.express as px
from qiskit import QuantumCircuit, Aer, execute # Quantum Engine
from qiskit.visualization import plot_histogram

st.set_page_config(page_title="AURA Standalone Suite", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚛️ AURA CORE")
menu = st.sidebar.selectbox("Select Module", ["Research Dashboard", "Aura AI Chatbot", "Quantum Lab"])

# --- DATA ENGINE ---
@st.cache_data
def get_data():
    return pd.read_excel("Aura_Full_Project.xlsx")

df = get_data()

# --- MODULE 1: AI CHATBOT ---
if menu == "Aura AI Chatbot":
    st.title("🤖 Aura Research Intelligence")
    st.info("This AI analyzes your .xlsl data to provide research insights.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your research data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simple Logic: AI context from your spreadsheet
        response = f"Aura Analysis: Based on your {len(df)} data rows, I suggest focusing on the highest variance trends."
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- MODULE 2: QUANTUM LAB ---
elif menu == "Quantum Lab":
    st.title("🌌 Quantum Simulation Environment")
    st.write("Simulate advanced STEM algorithms directly within Aura.")
    
    qubits = st.slider("Select Number of Qubits", 1, 5, 2)
    gate = st.selectbox("Apply Initial Gate", ["Hadamard (Superposition)", "X (Flip)"])
    
    if st.button("Run Quantum Circuit"):
        qc = QuantumCircuit(qubits, qubits)
        if gate == "Hadamard (Superposition)":
            qc.h(0) # Apply H-gate to first qubit
        else:
            qc.x(0)
        
        qc.measure(range(qubits), range(qubits))
        
        # Execute on local simulator
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1024)
        result = job.result()
        counts = result.get_counts(qc)
        
        st.write("### Simulation Results")
        st.bar_chart(counts)
        st.success("Quantum state collapsed successfully.")

# --- MODULE 3: DASHBOARD (Original) ---
else:
    st.title("📊 Aura Main Research Dashboard")
    st.dataframe(df, use_container_width=True)
    fig = px.scatter(df, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
