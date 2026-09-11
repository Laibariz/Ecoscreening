import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration & Theme
st.set_page_config(page_title="Pakistan Climate Resilience Hub", page_icon="🌿", layout="wide")

st.title("🇵🇰 Pakistan Climate Change Monitoring & Mitigation Engine")
st.markdown("""
This dashboard monitors the primary geographic drivers of Pakistan's climate, evaluates real-time anomalies, 
and simulates structural measures to mitigate climate risks.
""")

# 2. Sidebar - Parameter Configuration
st.sidebar.header("🕹️ Climate Factor & Mitigation Controls")
region = st.sidebar.selectbox(
    "Select Risk Zone / Territory:",
    ["Northern Highlands (Glacial Melt)", "Indus Basin (Flooding)", "Thar/Cholistan (Desertification)", "Coastal Delta (Salinity)"]
)

timeline = st.sidebar.slider("Projection Horizon (Years from current baseline):", 5, 30, 15)
mitigation_investment = st.sidebar.slider("Afforestation & Infrastructure Scale (%)", 0, 100, 40)

# 3. Main Layout Tabs
tab1, tab2, tab3 = st.tabs(["📊 Climate Factors", "📡 Monitoring Metrics", "🛡️ Mitigation Planning"])

with tab1:
    st.subheader(f"Dominant Drivers: {region}")
    if "Northern" in region:
        st.info("**Primary Drivers:** Altitude, Relief Rainfall, and Western Disturbances. **Threat:** Rapid glacial lake outburst floods (GLOF).")
    elif "Indus" in region:
        st.info("**Primary Drivers:** Southwest Monsoon cycles and river runoff. **Threat:** Heavy flash and riverine flooding downstream.")
    else:
        st.info("**Primary Drivers:** Continentality and high heat index loops. **Threat:** Deep groundwater depletion and crop failures.")

with tab2:
    st.subheader("📡 Real-Time Environmental Anomaly Tracking")
    col1, col2 = st.columns(2)
    
    # Simulating data for visualization
    years = np.arange(2000, 2026 + timeline)
    base_temp = 24.5 + (years - 2000) * 0.03
    # If investment is high, mitigate temperature delta slightly in simulation
    mitigated_temp = base_temp - (mitigation_investment * 0.005)

    with col1:
        st.metric(label="Historical Temperature Rise Trend", value="+0.5 °C", delta="Accelerating since 1960s")
        
        # Plotting trend using matplotlib
        fig, ax = plt.subplots()
        ax.plot(years, base_temp, label="Unmitigated Path", color="red", linestyle="--")
        ax.plot(years, mitigated_temp, label="Mitigated Projection", color="green")
        ax.set_ylabel("Mean Air Temp (°C)")
        ax.set_xlabel("Year")
        ax.legend()
        st.pyplot(fig)
        
    with col2:
        st.write("**Key Indicators Flagged:**")
        st.warning("⚠️ Critical Water Scarcity Line approaching absolute threshold (<500 m³ per capita).")
        st.error("🚨 Monsoon intensity variation exceeds baseline limits by +18%.")

with tab3:
    st.subheader("🛡️ Actionable Mitigation Framework")
    st.markdown("Based on current indicators, implement these local countermeasures immediately:")
    
    # Dynamic recommendations output
    if "Highlands" in region or mitigation_investment > 50:
        st.success("✅ **Afforestation Target:** Deploying mixed-species vegetation canopies on slopes reduces mudslides.")
        st.success("✅ **Smart Water Management:** Building up-gradient check dams reduces flash flood speed.")
    else:
        st.error("❌ **Critical Action Gap:** Higher funding and resource allocation required for infrastructure protection updates.")
        
    # Structured Plan
    st.markdown("""

    | Action Sector | Strategic Measure | Expected Result |
    | :--- | :--- | :--- |
    | **Agriculture** | Switch to flood-resistant or drought-resilient seed crops. | Protects regional food security. |
    | **Infrastructure** | Scale up the National Flood Forecasting and Early Warning Systems. | Lowers structural and human life loss. |
    | **Urban Centers** | Designate green spaces and implement bicycle lane networks in major cities. | Cuts local heat island impacts. |
    """)
