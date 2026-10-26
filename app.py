import folium
from folium.plugins import FastMarkerCluster
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Global AI Infrastructure Geopolitical Risk Index",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- EDITORIAL OLIVE & WARM BEIGE STYLING -----------------
st.markdown(
    """
<style>
    /* Global Canvas & Base Typography */
    html, body, [class*="css"], .stApp {
        background-color: #1c241a !important;
        color: #dfd7c2 !important;
        font-family: 'Cambria', 'Georgia', 'Times New Roman', serif !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6, .stTitle {
        font-family: 'Cambria', 'Georgia', serif !important;
        color: #f5f0e1 !important;
        letter-spacing: -0.01em !important;
        font-weight: 700 !important;
    }
    
    h1 {
        color: #f5f0e1 !important;
        border-bottom: 1px solid rgba(226, 218, 196, 0.2);
        padding-bottom: 8px;
    }

    p, span, label, div {
        color: #dfd7c2;
        font-family: 'Cambria', 'Georgia', serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #151b13 !important;
        border-right: 1px solid rgba(226, 218, 196, 0.15) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #dfd7c2 !important;
        font-family: 'Cambria', 'Georgia', serif !important;
    }

    /* Metric Tiles */
    .metric-card {
        background: #242e22;
        border: 1px solid rgba(226, 218, 196, 0.22);
        border-radius: 6px;
        padding: 18px 14px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
    }
    .metric-value {
        font-family: 'Cambria', 'Georgia', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #f5f0e1;
        line-height: 1.1;
    }
    .metric-label {
        font-family: 'Cambria', 'Georgia', serif;
        font-size: 0.82rem;
        font-weight: 600;
        color: #eedcb3;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 28px;
        border-bottom: 1px solid rgba(226, 218, 196, 0.2);
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Cambria', 'Georgia', serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #a8a08b !important;
        padding: 8px 6px !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #f5f0e1 !important;
        border-bottom: 2px solid #eedcb3 !important;
    }

    /* Callouts & Content Boxes */
    .theory-box {
        background-color: #242e22;
        border: 1px solid rgba(226, 218, 196, 0.25);
        border-left: 4px solid #eedcb3;
        border-radius: 4px;
        padding: 18px 22px;
        margin-bottom: 18px;
    }
    .research-card {
        background: #242e22;
        border: 1px solid rgba(226, 218, 196, 0.2);
        border-radius: 6px;
        padding: 20px;
        height: 100%;
    }
    .research-card h4 {
        color: #f5f0e1 !important;
        margin-bottom: 6px;
    }

    /* Streamlit native widget text overrides */
    .stSelectbox label, .stSlider label {
        color: #f5f0e1 !important;
        font-weight: 600 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ----------------- DATA INGESTION -----------------
@st.cache_data
def load_data():
    master_df = pd.read_csv("master_ai_infrastructure_risk_index.csv")
    cables_df = pd.read_csv("cable_landing_stations.csv").dropna(
        subset=["latitude", "longitude"]
    )
    return master_df, cables_df


try:
    df_index, df_cables = load_data()
except Exception as e:
    st.error(f"Error loading CSV datasets: {e}")
    st.stop()

# ----------------- HEADER -----------------
st.title("Global AI Infrastructure Geopolitical Risk Index")
st.markdown(
    """
<p style="font-size: 1.12rem; color: #eedcb3; max-width: 920px; margin-top: 4px; line-height: 1.5;">
An empirical intelligence framework mapping physical subsea connectivity and hyperscale compute concentration 
against sovereign institutional fragility, state surveillance capacity, and judicial vulnerability.
</p>
""",
    unsafe_allow_html=True,
)

# ----------------- TABS SETUP -----------------
tab_explorer, tab_researchers, tab_theory, tab_pipeline = st.tabs(
    [
        "📊 Interactive Risk Explorer",
        "🔬 Researcher & Policy Applications",
        "🏛️ Theoretical Framework",
        "⚙️ Pipeline Architecture",
    ]
)

# =========================================================================
# TAB 1: INTERACTIVE EXPLORER
# =========================================================================
with tab_explorer:
    st.sidebar.markdown(
        "<h3 style='color: #f5f0e1; font-family: Cambria, Georgia;'>Index Controls</h3>",
        unsafe_allow_html=True,
    )

    quadrants = ["All"] + sorted(df_index["risk_quadrant"].unique().tolist())
    selected_quadrant = st.sidebar.selectbox("Risk Quadrant:", quadrants)

    min_risk, max_risk = st.sidebar.slider(
        "V-Dem Governance Risk Threshold:",
        min_value=0.0,
        max_value=100.0,
        value=(0.0, 100.0),
    )

    # Filter logic
    filtered_df = df_index[
        (df_index["governance_risk_score"] >= min_risk)
        & (df_index["governance_risk_score"] <= max_risk)
    ]
    if selected_quadrant != "All":
        filtered_df = filtered_df[
            filtered_df["risk_quadrant"] == selected_quadrant
        ]

    st.write("")
    # Metric summary row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{len(filtered_df)}</div><div class="metric-label">Jurisdictions Monitored</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{int(filtered_df["cable_landing_count"].sum()):,}</div><div class="metric-label">Active Cable Landings</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{int(filtered_df["datacenter_count"].sum()):,}</div><div class="metric-label">Enterprise Facilities</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        avg_exp = (
            filtered_df["composite_exposure_score"].mean()
            if not filtered_df.empty
            else 0.0
        )
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{avg_exp:.2f}</div><div class="metric-label">Mean Exposure Index</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # Map & Table Layout
    col_map, col_table = st.columns([3, 2])

    with col_map:
        st.markdown("### 🗺️ Physical Landing Station Clusters")
        valid_countries = filtered_df["country"].unique()
        cables_subset = df_cables[df_cables["country"].isin(valid_countries)]

        m = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles="OpenStreetMap",
            control_scale=True,
        )

        if not cables_subset.empty:
            locations = cables_subset[["latitude", "longitude"]].values.tolist()
            FastMarkerCluster(data=locations).add_to(m)

        st_folium(m, width=680, height=480, returned_objects=[])

    with col_table:
        st.markdown("### 📋 Exposure Priority Rankings")
        display_cols = [
            "country",
            "composite_exposure_score",
            "physical_density_score",
            "governance_risk_score",
        ]
        st.dataframe(
            filtered_df[display_cols].reset_index(drop=True),
            width="stretch",
            height=480,
        )

    # Sovereign Dossier Drilldown
    st.markdown("---")
    st.subheader("🔍 Sovereign Infrastructure Dossier")
    sel_country = st.selectbox(
        "Select Jurisdiction for Deep-Dive Profile:",
        options=df_index["country"].sort_values(),
    )
    rec = df_index[df_index["country"] == sel_country].iloc[0]

    d1, d2, d3, d4 = st.columns(4)
    d1.info(f"**Classification:**\n{rec['risk_quadrant']}")
    d2.metric("Cable Landings", f"{int(rec['cable_landing_count'])}")
    d3.metric("Data Centers", f"{int(rec['datacenter_count'])}")
    d4.metric("Exposure Metric", f"{rec['composite_exposure_score']}")

    # Export control in sidebar
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Download Active Subset (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="ai_infrastructure_risk_filtered.csv",
        mime="text/csv",
    )

# =========================================================================
# TAB 2: RESEARCHER & POLICY APPLICATIONS
# =========================================================================
with tab_researchers:
    st.markdown("## 🔬 What Researchers & Analysts Can Seek in This Index")
    st.markdown(
        """
    <p style="font-size: 1.05rem; color: #dfd7c2; line-height: 1.6;">
    This index bridges the structural gap between <strong>spatial infrastructure mapping</strong> and <strong>comparative political economy</strong>. 
    Rather than treating compute infrastructure as a purely commercial commodity, researchers can leverage this framework across four distinct empirical inquiry areas:
    </p>
    """,
        unsafe_allow_html=True,
    )

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(
            """
        <div class="research-card">
            <h4>1. Empirical Stress-Testing of AI Supply Chains</h4>
            <p style="color: #dfd7c2; font-size: 0.95rem; line-height: 1.5;">
            Investigate how national frontier model providers (e.g., frontier labs, cloud hyperscalers) route cross-border telemetry. Analysts can test hypotheses on whether network traffic actively avoids or disproportionately transits illiberal transit corridors (e.g., the Suez/Red Sea bottleneck or Straits of Malacca).
            </p>
            <p style="color: #eedcb3; font-size: 0.88rem; font-weight: 600;">Key Query: Which physical corridors present single points of failure under state-sponsored disruption?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
        <div class="research-card">
            <h4>2. Authoritarian Leverage & Data Sovereignty Mandates</h4>
            <p style="color: #dfd7c2; font-size: 0.95rem; line-height: 1.5;">
            Comparative politics researchers can isolate jurisdictions with high compute density but rapid democratic backsliding. Use this index to examine how non-democratic states leverage physical infrastructure hosting to impose local data localization laws, warrantless lawful interception, and telemetry capture.
            </p>
            <p style="color: #eedcb3; font-size: 0.88rem; font-weight: 600;">Key Query: Does asset hosting correlate with coercive extraterritorial surveillance capacity?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with r2:
        st.markdown(
            """
        <div class="research-card">
            <h4>3. Geopolitical Alignment & Compute Decoupling</h4>
            <p style="color: #dfd7c2; font-size: 0.95rem; line-height: 1.5;">
            International relations and trade policy scholars can model the impact of export controls (such as advanced GPU restrictions and semiconductor sanctions). By cross-referencing quadrant classifications with alliance treaties (e.g., NATO, Quad, BRICS+), researchers can track infrastructural decoupling or "splinternet" fragmentation.
            </p>
            <p style="color: #eedcb3; font-size: 0.88rem; font-weight: 600;">Key Query: Are non-aligned states emerging as neutral digital conduits or contested chokepoints?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
        <div class="research-card">
            <h4>4. Human Rights Risk Audits for Enterprise AI Deployment</h4>
            <p style="color: #dfd7c2; font-size: 0.95rem; line-height: 1.5;">
            Corporate governance, ESG auditors, and compliance teams can utilize the Composite Exposure Metric to conduct formal human rights impact assessments (HRIAs). It reveals latent operational risks where compute dependencies inadvertently subject sensitive customer data to unconstrained judicial seizure.
            </p>
            <p style="color: #eedcb3; font-size: 0.88rem; font-weight: 600;">Key Query: Where does an enterprise's physical compute footprint conflict with statutory civil liberties mandates?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# =========================================================================
# TAB 3: THEORETICAL THESIS
# =========================================================================
with tab_theory:
    st.markdown("## 🏛️ Theoretical Thesis: The Materiality of AI")

    st.markdown(
        """
    <div class="theory-box">
        <p style="font-size: 1.15rem; font-style: italic; color: #f5f0e1; margin: 0; line-height: 1.6;">
        "Artificial Intelligence is routinely conceptualized as ethereal compute residing in an abstract, borderless 'cloud.' In physical reality, its foundational architecture is rigidly territorial, geographically vulnerable, and anchored within sovereign jurisdictions possessing highly divergent institutional commitments to civil liberties and the rule of law."
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    t1, t2 = st.columns(2)
    with t1:
        st.markdown(
            """
        ### 1. The Chokepoint Dilemma in Digital Sovereign Transit
        Commercial artificial intelligence models and high-frequency data pipelines rely on fewer than 600 subsea cable systems carrying over 95% of intercontinental traffic. While cloud providers advertise borderless resilience, physical landing stations must anchor in specific coastal geographies.
        
        This index reveals that key global transit routes pass through **high-governance-risk jurisdictions**:
        * **The Suez Canal / Red Sea Corridor (Egypt)**: Represents one of the world's most concentrated digital single points of failure. Nearly all Europe-to-Asia data transit funnels through Egyptian territorial waters and overland corridors controlled by state-managed monopolies.
        * **The Strait of Malacca / South China Sea Corridors**: Highly concentrated landing stations in maritime Southeast Asia create systemic exposure to regional territorial disputes and unconstrained surveillance regimes.
        """
        )

    with t2:
        st.markdown(
            """
        ### 2. Institutional Buffers vs. Coercive Jurisdiction
        Data governance is not purely a legal compliance problem; it is a question of **coercive state capacity**:
        * In **Resilient Hubs** (e.g., Germany, United Kingdom, Canada), institutional checks, administrative proceduralism, and independent courts provide legal predictability against arbitrary seizure, warrantless data interception, and nationalization.
        * In **Critical Chokepoints** (e.g., China, Russia, Saudi Arabia, UAE), immense capital investment in compute infrastructure coexists with state-centric legal architectures. Without autonomous judicial review, physical compute assets remain perpetually exposed to sovereign preemption, state-compelled telemetry access, and sudden regulatory decoupling.
        """
        )

    st.markdown("---")
    st.markdown("### The Four-Quadrant Strategic Typology")

    q_col1, q_col2 = st.columns(2)
    with q_col1:
        st.markdown(
            """
        **1. Critical Chokepoints (High Assets / High Risk)**
        * *Examples*: China, Russia, Saudi Arabia, India, Egypt.
        * *Strategic Reality*: Indispensable for regional routing or local inference, but carry acute exposure to state surveillance mandates, national security preemption, and export controls.
        
        **2. Resilient Hubs (High Assets / Low Risk)**
        * *Examples*: United States, United Kingdom, Canada, Japan, Germany.
        * *Strategic Reality*: The foundational backbone of the liberal international digital order. Characterized by deep capital markets, legal predictability, and high physical protection.
        """
        )
    with q_col2:
        st.markdown(
            """
        **3. Emerging Frontiers (Low Assets / High Risk)**
        * *Examples*: Central Asia, parts of Sub-Saharan Africa.
        * *Strategic Reality*: Digital peripheries vulnerable to predatory digital infrastructure financing ("digital silk road" initiatives) where physical compute has yet to scale.
        
        **4. Stable Periphery (Low Assets / Low Risk)**
        * *Examples*: New Zealand, Nordic states, Uruguay.
        * *Strategic Reality*: High institutional integrity and human rights protections, but constrained by geography or latency from serving as high-volume intercontinental transit cores.
        """
        )

# =========================================================================
# TAB 4: DATA ARCHITECTURE
# =========================================================================
with tab_pipeline:
    st.markdown("## ⚙️ Data Engineering & Pipeline Architecture")
    st.markdown(
        """
    The index executes a reproducible, four-phase computational pipeline converting heterogenous geospatial endpoints and multi-decade democracy indicators into a consolidated analytic index.
    """
    )

    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            """
        #### Phase 1: Physical Asset Ingestion
        * **Subsea Fiber Arteries**: Extracted 1,928 active landing coordinates from TeleGeography's global infrastructure database. String parsing algorithms isolated sovereign territory from station identifiers.
        * **Hyperscale Compute Density**: Ingested 18,000+ colocation and enterprise data center coordinates via the global ATLAS geospatial dataset.
        
        #### Phase 2: Log-Transformed Normalization
        Physical assets follow a power-law distribution (Northern Virginia, Frankfurt, Singapore, and London hold disproportionate compute capacity). A linear index would collapse non-Western hubs to zero:
        $$P_i = 12.5 \\times \\left[0.5 \\ln(1 + C_i) + 0.5 \\ln(1 + D_i)\\right]$$
        *Where $C_i$ = Cable landings, $D_i$ = Data center facilities. Yields a balanced 0–100 scale.*
        """
        )

    with p2:
        st.markdown(
            """
        #### Phase 3: Institutional Governance Scoring
        * Ingested the **Varieties of Democracy (V-Dem) Civil Liberties Index (`v2x_civlib`)**, measuring physical integrity rights, freedom of domestic movement, and judicial independence.
        * Inverted V-Dem's 0–1 scale to calculate sovereign governance risk:
        $$G_i = (1 - \\text{V-Dem}_{\\text{civlib}}) \\times 100$$
        
        #### Phase 4: Exposure Synthesis & Quadrant Classification
        Composite exposure reflects physical concentration weighted by institutional vulnerability:
        $$\\text{Exposure}_i = P_i \\times \\left(\\frac{G_i}{100}\\right)$$
        Jurisdictions are segmented using empirical median splits into four strategic operating profiles.
        """
        )

    st.markdown("---")
    st.markdown("#### Summary Data Dictionary")
    dict_df = pd.DataFrame(
        [
            {
                "Field": "cable_landing_count",
                "Source": "TeleGeography Submarine Cable Map",
                "Description": "Total active transoceanic fiber-optic cable landing points in sovereign territory.",
            },
            {
                "Field": "datacenter_count",
                "Source": "ATLAS Global Data Center Map",
                "Description": "Total enterprise and hyperscale facilities operating within the jurisdiction.",
            },
            {
                "Field": "physical_density_score",
                "Source": "Engineered (Pillar 1)",
                "Description": "Log-normalized composite asset score (0 = negligible, 100 = maximum global density).",
            },
            {
                "Field": "governance_risk_score",
                "Source": "V-Dem Institute (`v2x_civlib`)",
                "Description": "Inverted civil liberties index (0 = robust institutional rule of law, 100 = acute autocracy).",
            },
            {
                "Field": "composite_exposure_score",
                "Source": "Engineered Metric",
                "Description": "Total systemic supply-chain exposure metric ($P_i \\times G_i / 100$).",
            },
        ]
    )
    st.table(dict_df)