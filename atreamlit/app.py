st.markdown("""
    <style>
    /* Glowing Aura Effect */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #060606 0%, #001a33 100%);
    }
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.8);
        border-right: 1px solid #00d4ff;
    }
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
elif menu == "AI Training Lab":
    st.title("🧠 Aura Neural Training")
    st.write("Train a custom model based on your research parameters.")

    if not df.empty:
        # User selects which columns to analyze
        features = st.multiselect("Select Feature Columns (X)", df.columns)
        target = st.selectbox("Select Target Column to Predict (Y)", df.columns)

        if st.button("Initialize Training"):
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestRegressor
            
            # Prepare Data
            X = df[features].fillna(0)
            y = df[target].fillna(0)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            # Train Model
            model = RandomForestRegressor(n_estimators=100)
            model.fit(X_train, y_train)
            
            # Show Performance
            score = model.score(X_test, y_test)
            st.metric("Model Accuracy (R²)", f"{score:.2%}")
            
            # Save the trained model for future use
            import joblib
            joblib.dump(model, 'aura_model.pkl')
            st.success("Model 'aura_model.pkl' exported to project root.")
