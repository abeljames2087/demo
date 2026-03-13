import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Supply Chain AI Agent System", layout="wide", page_icon="🤖")

# --- DUMMY DATA ---
@st.cache_data
def load_data():
    # Inventory Data
    inventory_data = pd.DataFrame({
        'Product ID': [f'PRD-{i:04d}' for i in range(1, 11)],
        'Product Name': ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Webcam', 'Microphone', 'Speaker'],
        'Category': ['Electronics', 'Electronics', 'Electronics', 'Peripherals', 'Peripherals', 'Peripherals', 'Audio', 'Peripherals', 'Audio', 'Audio'],
        'Stock Level': np.random.randint(10, 500, 10),
        'Reorder Target': np.random.randint(50, 200, 10),
        'Unit Price ($)': np.random.uniform(20.0, 1500.0, 10).round(2),
        'Supplier': ['TechCorp', 'MobileInc', 'TechCorp', 'Visionary', 'KeyMasters', 'Clickers', 'SoundWave', 'Visionary', 'SoundWave', 'SoundWave']
    })
    
    # Calculate Status
    inventory_data['Status'] = inventory_data.apply(
        lambda x: 'Low Stock' if x['Stock Level'] < x['Reorder Target'] else 'Healthy', axis=1
    )

    # Order Details
    orders_data = pd.DataFrame({
        'Order ID': [f'ORD-{i:05d}' for i in range(1, 21)],
        'Date': pd.date_range(start='2023-10-01', periods=20, freq='D'),
        'Customer': [f'Customer {i}' for i in range(1, 21)],
        'Total Value ($)': np.random.uniform(100.0, 5000.0, 20).round(2),
        'Status': np.random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'], 20)
    })

    return inventory_data, orders_data

inventory_df, orders_df = load_data()

def load_disruption_data():
    return pd.DataFrame({
        'Event ID': [f'EVT-{i:03d}' for i in range(1, 17)],
        'Type': [
            'Port Strike', 'Typhoon', 'Supplier Delay',
            'Congestion', 'Equipment Failure', 'Customs Delay',
            'Berthing Delay', 'Weather Delay', 'Labor Shortage',
            'Congestion', 'Customs Delay', 'Port Strike',
            'Equipment Failure', 'Weather Delay', 'Berthing Delay',
            'Congestion'
        ],
        'Location': [
            'Port of LA', 'South China Sea', 'Taiwan', 
            'Nhava Sheva (Mumbai)', 'Chennai Port', 'Mundra Port',
            'Kandla Port', 'Mumbai Port', 'Mormugao Port', 
            'New Mangalore Port', 'Cochin Port', 'Tuticorin Port',
            'Ennore Port', 'Visakhapatnam Port', 'Paradip Port',
            'Kolkata Port'
        ],
        'lat': [
            33.729, 15.0, 23.5, 
            18.944, 13.082, 22.840,
            23.011, 18.944, 15.413,
            12.928, 9.963, 8.764,
            13.259, 17.697, 20.269,
            22.029
        ],
        'lon': [
            -118.262, 115.0, 121.0, 
            72.953, 80.291, 69.721,
            70.219, 72.836, 73.799,
            74.809, 76.271, 78.134,
            80.334, 83.292, 86.666,
            88.064
        ],
        'Impact Level': [
            'High', 'Critical', 'Medium',
            'High', 'Medium', 'Low',
            'Medium', 'Low', 'Medium',
            'High', 'Low', 'Critical',
            'Medium', 'High', 'Low',
            'High'
        ],
        'Value at Risk ($)': [
            1250000, 3400000, 450000,
            2100000, 850000, 250000,
            1200000, 500000, 750000,
            1800000, 400000, 3200000,
            900000, 2200000, 300000,
            1500000
        ]
    })

disruptions_df = load_disruption_data()

# --- SIDEBAR: AI Controls ---
st.sidebar.title("🤖 Navigation & Controls")

page = st.sidebar.radio("Navigation", ["Dashboard", "Order Tracking", "Supplier Logistics", "AI Agent Control Center"])

st.sidebar.markdown("---")

automation_mode = st.sidebar.radio(
    "Automation Level",
    ["Advisory Mode (Human in the loop)", "Autonomous Mode (AI executes)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Active Agents")
st.sidebar.checkbox("🕵️ Researcher Agent (Observe)", value=True, disabled=True)
st.sidebar.checkbox("📊 Analyst Agent (Orient)", value=True, disabled=True)
st.sidebar.checkbox("🤝 Negotiator Agent (Decide & Act)", value=True, disabled=True)

st.sidebar.markdown("---")
st.sidebar.info("System is monitoring 12,043 maritime routes and 450 supplier nodes in real-time.")

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    # --- MAIN DASHBOARD: DISRUPTION COCKPIT ---
    st.title("🌐 Supply Chain Disruption Cockpit")

    # High level metrics
    col1, col2, col3 = st.columns(3)
    total_risk = disruptions_df['Value at Risk ($)'].sum()
    with col1:
        st.metric("Total Value at Risk", f"${total_risk:,.0f}", delta="+$1.2M vs yesterday", delta_color="inverse")
    with col2:
        st.metric("Active Disruptions", len(disruptions_df), delta="2 new", delta_color="inverse")
    with col3:
        st.metric("Critical SKUs Affected", 142, delta="15", delta_color="inverse")
    
    st.markdown("---")
    
    # Layout: Map on left, AI Thought logs on right
    col_map, col_logs = st.columns([2, 1])
    
    with col_map:
        st.subheader("Global Threat Map")
        # Simple map showing disruption locations
        st.map(disruptions_df, zoom=1)
        
        st.markdown("### Active Threats")
        st.dataframe(disruptions_df[['Event ID', 'Type', 'Location', 'Impact Level', 'Value at Risk ($)']], use_container_width=True)
    
    with col_logs:
        st.subheader("🧠 Multi-Agent Thought Logs")
        log_container = st.container(height=400)
        with log_container:
            st.markdown("**[10:14 AM] 🕵️ Researcher Agent:** Detected abnormal weather patterns (Typhoon) forming in South China Sea via NOAA satellite API.")
            st.markdown("**[10:15 AM] 🕵️ Researcher Agent:** Cross-referencing active shipments... Found 3 vessels in projected path.")
            st.markdown("**[10:15 AM] 📊 Analyst Agent:** Ingesting signal. Calculating ETA delays: Estimated 4-6 days delay for PO-9921 and PO-9922.")
            st.markdown("**[10:16 AM] 📊 Analyst Agent:** Financial Impact quantified: $3.4M Inventory at risk. SLA breach imminent for 2 key accounts.")
            st.markdown("**[10:17 AM] 🤝 Negotiator Agent:** Searching alternative routing. Air freight capacity available via Singapore.")
            
            if "Advisory" in automation_mode:
                st.info("**[10:18 AM] 🤝 Negotiator Agent:** Proposed Resolution generated for Event EVT-002. Awaiting Human Approval.")
            else:
                st.success("**[10:18 AM] 🤝 Negotiator Agent:** Autonomous execution authorized. Rerouting via Air freight booked.")
    
    st.markdown("---")
    
    # --- RESOLUTION COMPARISON ---
    st.subheader("⚡ AI Resolution Proposals (Event EVT-002: Typhoon)")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.success("Option A: Air Freight via Singapore (AI Recommended)")
        st.metric("Additional Cost", "$45,000")
        st.metric("Delivery Delay", "+1 Day")
        st.metric("Carbon Impact", "+12.4 Tons CO2")
        if st.button("Execute Option A", type="primary"):
            st.toast("Executing Air Freight Re-routing...")
    
    with res_col2:
        st.warning("Option B: Reroute Vessel South")
        st.metric("Additional Cost", "$12,000")
        st.metric("Delivery Delay", "+5 Days")
        st.metric("Carbon Impact", "+2.1 Tons CO2")
        if st.button("Execute Option B"):
            st.toast("Executing Vessel Reroute...")
    
    with res_col3:
        st.error("Option C: Do Nothing (Wait it out)")
        st.metric("Additional Cost", "$0")
        st.metric("Delivery Delay", "+8 to 14 Days")
        st.metric("Carbon Impact", "0 Tons CO2")
        if st.button("Execute Option C"):
            st.toast("No action taken.")

# --- PAGE: ORDER TRACKING ---
elif page == "Order Tracking":
    st.title("Order Tracking")
    
    search_query = st.text_input("Search Order ID or Customer Name", "")
    
    filtered_orders = orders_df.copy()
    if search_query:
        mask = filtered_orders['Order ID'].str.contains(search_query, case=False) | filtered_orders['Customer'].str.contains(search_query, case=False)
        filtered_orders = filtered_orders[mask]
        
    st.dataframe(filtered_orders, use_container_width=True)

# --- PAGE: SUPPLIER LOGISTICS ---
elif page == "Supplier Logistics":
    st.title("Supplier Directory & Logistics")
    
    supplier_perf = pd.DataFrame({
        'Supplier': inventory_df['Supplier'].unique(),
        'On-Time Delivery Rate (%)': np.random.uniform(85, 100, len(inventory_df['Supplier'].unique())).round(1),
        'Quality Score (1-10)': np.random.uniform(7.5, 9.9, len(inventory_df['Supplier'].unique())).round(1),
        'Active Contracts': np.random.randint(1, 5, len(inventory_df['Supplier'].unique()))
    })
    
    st.dataframe(supplier_perf, use_container_width=True)
    
    st.markdown("### Supplier Map (Simulated)")
    # Generate random coordinates for demo map
    map_data = pd.DataFrame(
        np.random.randn(len(supplier_perf), 2) / [20, 20] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    st.map(map_data)

# --- PAGE: AI AGENT CONTROL CENTER ---
elif page == "AI Agent Control Center":
    st.title("AI Agent Control Center")
    

    # Display Active AI Agents
    st.markdown("### 🤖 Active System Agents")
    agent_col1, agent_col2, agent_col3 = st.columns(3)
    with agent_col1:
        st.info("**🕵️ Researcher Agent (Observe)**")
        with st.expander("Agent Directives & Prompt", expanded=True):
            st.markdown("""
            **Role:** Expert AI Research Agent specializing in Global Marine Trade and Maritime Economics.
            
            **Goal:** Deliver actionable insights that help understand how global marine trade operates, its economic importance, and emerging trends shaping the industry.
            
            **Research Areas:**
            1. Global shipping routes and major maritime trade corridors.
            2. Key ports and logistics hubs worldwide.
            3. Major commodities transported via sea (oil, LNG, coal, containers, grains, etc.).
            4. Leading shipping companies and maritime logistics providers.
            5. Current trends affecting marine trade (geopolitics, supply chain disruptions, canal blockages, piracy, environmental regulations).
            6. Technological advancements in shipping (AI, automation, smart ports, green shipping).
            7. Environmental impact and sustainability initiatives in maritime trade.
            8. Trade volumes, economic impact, and future projections.
            
            **Output Requirements:**
            - Provide clear headings and structured sections.
            - Include statistics, charts or summarized data when relevant.
            - Mention important organizations like IMO, WTO, UNCTAD, and major shipping alliances.
            - Highlight recent developments and risks.
            - Provide a concise summary of key insights and future outlook.
            
            **Tone:** Professional, analytical, and research-oriented.
            """)
    with agent_col2:
        st.warning("**📊 Analyst Agent (Orient)**")
        with st.expander("Agent Directives & Prompt", expanded=False):
            st.markdown("""
            **Role:** Supply Chain Financial Analyst.
            
            **Goal:** Quantify the immediate and long-term financial & logistical impact of global marine trade disruptions identified by the Researcher Agent.
            
            **Responsibilities:**
            - Compute ETA delays using historical models.
            - Estimate exact dollar Value at Risk.
            - Check SLA (Service Level Agreement) constraints for affected items.
            """)
    with agent_col3:
        st.success("**🤝 Negotiator Agent (Decide/Act)**")
        with st.expander("Agent Directives & Prompt", expanded=False):
            st.markdown("""
            **Role:** Logistics Resolution & Negotiation Agent.
            
            **Goal:** Rapidly formulate and execute alternative supply chain routing options while minimizing additional cost and carbon impact.
            
            **Responsibilities:**
            - Formulate multiple mitigation options (Air, Rail, Secondary Sea Ports).
            - Evaluate carbon footprint vs delay costs.
            - Execute automated bookings when within Operational Guardrail thresholds.
            """)

    st.markdown("---")
    st.markdown("### Settings & Policies")

    st.markdown("#### Operational Guardrails")
    max_spend = st.slider("Max Autonomous Spend per Resolution ($)", 1000, 50000, 15000, step=1000)
    delay_threshold = st.slider("Calculate rerouting if delay exceeds (Days)", 1, 14, 3)

    st.markdown("#### Prioritization Rules")
    st.multiselect("Prioritize Categories (Always Ensure Stock)", ['Electronics', 'Peripherals', 'Audio'], default=['Electronics'])
    
    st.markdown("---")
    st.markdown("### System Logs")
    st.info("System is healthy. 12,043 maritime routes and 450 supplier nodes monitored.")
    # Quick dummy logs
    st.code("[INFO] Data ingested from Port of LA successfully.\n[WARN] High latency communicating with Supplier MobileInc API.\n[INFO] Weather model updated successfully.", language="log")

    st.markdown("---")
    st.markdown("### 🧪 Live AI Agent Testing")
    st.markdown("Run the **Researcher Agent** with a custom query about global marine trade.")
    
    # Needs GEMINI_API_KEY from environment to work
    import os
    try:
        from research_agent import run_research_agent
        api_key_status = "Available" if os.environ.get("GEMINI_API_KEY") else "Missing"
    except ImportError:
        api_key_status = "Module not found"
        
    if api_key_status != "Available":
        st.warning("⚠️ The `GEMINI_API_KEY` environment variable is not set. The live agent cannot run.")
        api_key = st.text_input("Enter your Gemini API Key here to enable the agent:", type="password")
        if api_key:
             os.environ["GEMINI_API_KEY"] = api_key
             st.success("API Key set temporarily for this session.")
             st.rerun()
    else:
        st.success("✅ Gemini API Key detected. Researcher Agent is ready.")

    query = st.text_area("Research Query:", value="Analyze the current impact of the Suez Canal disruptions on global shipping rates and alternative routes.")
    
    if st.button("Run Researcher Agent 🕵️", type="primary"):
        with st.spinner("Agent is observing and orienting..."):
            try:
                # Get the key dynamically in case they just added it via the UI
                current_api_key = os.environ.get("GEMINI_API_KEY")
                if current_api_key:
                    from research_agent import run_research_agent
                    report = run_research_agent(query, current_api_key)
                    st.markdown("### 📄 Research Report")
                    st.markdown(report)
                else:
                    st.error("API Key not found.")
            except Exception as e:
                st.error(f"Failed to run agent: {str(e)}")
