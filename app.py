import textwrap
import folium
from folium.plugins import FastMarkerCluster, HeatMap
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Global AI Infrastructure Geopolitical & Ecological Risk Index",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------- EDITORIAL NAVY BLUE & ALABASTER STYLING -----------------
st.markdown(
    """
<style>
    /* Main Background & Base Typography */
    html, body, [class*="css"], .stApp {
        background-color: #0b1320 !important;
        color: #d1dced !important;
        font-family: 'Cambria', 'Georgia', 'Times New Roman', serif !important;
    }
    
    /* Typography Hierarchy */
    h1, h2, h3, h4, h5, h6, .stTitle {
        font-family: 'Cambria', 'Georgia', serif !important;
        color: #f0f4f8 !important;
        letter-spacing: -0.015em !important;
        font-weight: 700 !important;
    }
    h1 {
        border-bottom: 1px solid rgba(190, 206, 230, 0.2);
        padding-bottom: 10px;
        margin-bottom: 6px;
    }
    p, span, label, div {
        color: #d1dced;
        font-family: 'Cambria', 'Georgia', serif;
    }

    /* Top Filter Container Panel */
    .filter-panel {
        background: #111c2e;
        border: 1px solid rgba(190, 206, 230, 0.16);
        border-radius: 8px;
        padding: 16px 20px 8px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }

    /* Modern Metric Cards */
    .metric-card {
        background: #132035;
        border: 1px solid rgba(190, 206, 230, 0.18);
        border-top: 3px solid #3b82f6;
        border-radius: 6px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .metric-value {
        font-family: 'Cambria', 'Georgia', serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .metric-label {
        font-family: 'Cambria', 'Georgia', serif;
        font-size: 0.78rem;
        font-weight: 600;
        color: #94a9c9;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        margin-top: 6px;
    }

    /* Tab Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid rgba(190, 206, 230, 0.18);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Cambria', 'Georgia', serif !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        color: #7b8fae !important;
        padding: 8px 6px !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #f0f4f8 !important;
        border-bottom: 2px solid #60a5fa !important;
    }

    /* Dossier Card & Content Boxes */
    .theory-box {
        background-color: #132035;
        border: 1px solid rgba(190, 206, 230, 0.18);
        border-left: 4px solid #60a5fa;
        border-radius: 4px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .research-card {
        background: #132035;
        border: 1px solid rgba(190, 206, 230, 0.15);
        border-radius: 6px;
        padding: 22px;
        height: 100%;
    }
    .research-card h4 {
        color: #f0f4f8 !important;
        margin-bottom: 8px;
    }

    /* Selectbox & Dropdown Popover (Deep Navy on White) */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] * {
        color: #0b1320 !important;
        font-family: 'Cambria', 'Georgia', serif !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    }
    ul[role="listbox"] li,
    ul[role="listbox"] li div,
    ul[role="listbox"] li span,
    ul[role="listbox"] div[role="option"],
    ul[role="listbox"] div[role="option"] span,
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] span,
    div[role="option"],
    div[role="option"] * {
        color: #0b1320 !important;
        font-family: 'Cambria', 'Georgia', serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #0b1320 !important;
    }
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    div[role="option"]:hover,
    div[role="option"]:hover *,
    li[aria-selected="true"],
    li[aria-selected="true"] * {
        background-color: #e2ebf5 !important;
        color: #08101d !important;
        font-weight: 700 !important;
        -webkit-text-fill-color: #08101d !important;
    }
    .stSelectbox label, .stSlider label {
        color: #f0f4f8 !important;
        font-family: 'Cambria', 'Georgia', serif !important;
        font-weight: 600 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


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

# ----------------- HERO HEADER -----------------
st.title("Global AI Infrastructure Geopolitical & Ecological Risk Index")
st.markdown(
    """
<div style="display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap;">
    <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">158 Sovereign States</span>
    <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">V-Dem Civil Liberties v14</span>
    <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">WRI Aqueduct 4.0</span>
    <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">TeleGeography Subsea Mesh</span>
</div>
<p style="font-size: 1.05rem; color: #94a9c9; max-width: 1000px; line-height: 1.55; margin-bottom: 22px;">
An empirical tri-pillar intelligence model mapping the physical concentration of transoceanic cables and hyperscale data centers against institutional civil liberties vulnerability and municipal evaporative cooling stress.
</p>
""",
    unsafe_allow_html=True,
)

tab_explorer, tab_heatmap, tab_researchers, tab_theory, tab_pipeline = st.tabs(
    [
        "📊 Interactive Risk Explorer",
        "🔥 Global Risk Heatmap",
        "🔬 Researcher & Policy Applications",
        "🏛️ Theoretical Framework",
        "⚙️ Pipeline Architecture",
    ]
)

# =========================================================================
# TAB 1: INTERACTIVE EXPLORER (REFINED LAYOUT)
# =========================================================================
with tab_explorer:
    cluster_col = (
        "empirical_typology"
        if "empirical_typology" in df_index.columns
        else "risk_quadrant"
    )
    clusters = ["All"] + sorted(df_index[cluster_col].unique().tolist())

    # Top Control Filter Bar
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns([1.2, 1.4, 1.4])
    with f1:
        selected_cluster = st.selectbox("Empirical Typology Cluster:", clusters)
    with f2:
        min_gov, max_gov = st.slider(
            "Pillar 2: V-Dem Governance Risk:",
            min_value=0.0,
            max_value=100.0,
            value=(0.0, 100.0),
        )
    with f3:
        min_env, max_env = st.slider(
            "Pillar 3: WRI Water Stress Index:",
            min_value=0.0,
            max_value=100.0,
            value=(0.0, 100.0),
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Filter logic
    filtered_df = df_index[
        (df_index["governance_risk_score"] >= min_gov)
        & (df_index["governance_risk_score"] <= max_gov)
        & (df_index["environmental_stress_score"] >= min_env)
        & (df_index["environmental_stress_score"] <= max_env)
    ]
    if selected_cluster != "All":
        filtered_df = filtered_df[filtered_df[cluster_col] == selected_cluster]

    # Metric Row
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
            f'<div class="metric-card"><div class="metric-value">{int(filtered_df["datacenter_count"].sum()):,}</div><div class="metric-label">Data Center Facilities</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        avg_exp = (
            filtered_df["composite_exposure_score"].mean()
            if not filtered_df.empty
            else 0.0
        )
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{avg_exp:.2f}</div><div class="metric-label">Mean Tri-Pillar Exposure</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # Map & Priority Rankings Split Layout
    col_map, col_table = st.columns([1.6, 1.4])

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

        raw_map_html = m._repr_html_()
        dark_tile_style = """
        <style>
            .leaflet-tile {
                filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3) !important;
            }
            .leaflet-container {
                background: #080d17 !important;
            }
        </style>
        """
        if "<head>" in raw_map_html:
            map_html = raw_map_html.replace("<head>", f"<head>{dark_tile_style}")
        else:
            map_html = dark_tile_style + raw_map_html

        components.html(map_html, width=640, height=480)

    with col_table:
        st.markdown("### 📋 Exposure Priority Rankings")
        display_cols = [
            "country",
            "composite_exposure_score",
            "physical_density_score",
            "governance_risk_score",
            "environmental_stress_score",
        ]
        formatted_table = (
            filtered_df[display_cols]
            .sort_values(by="composite_exposure_score", ascending=False)
            .reset_index(drop=True)
            .rename(
                columns={
                    "country": "Jurisdiction",
                    "composite_exposure_score": "Composite Exposure",
                    "physical_density_score": "Density",
                    "governance_risk_score": "Gov Risk",
                    "environmental_stress_score": "Water Stress",
                }
            )
        )

        table_html = formatted_table.to_html(index=False, classes="rankings-table")
        st.markdown(
            f"""
            <div style="max-height: 480px; overflow-y: auto; border: 1px solid rgba(190, 206, 230, 0.2); border-radius: 6px; padding: 4px; background-color: #0e1726;">
                <style>
                    .rankings-table {{ width: 100%; border-collapse: collapse; font-family: 'Cambria', 'Georgia', serif; font-size: 0.92rem; }}
                    .rankings-table th {{ background-color: #16253d; color: #f0f4f8; padding: 10px 8px; text-align: left; position: sticky; top: 0; border-bottom: 2px solid rgba(190, 206, 230, 0.3); z-index: 1; }}
                    .rankings-table td {{ padding: 8px; border-bottom: 1px solid rgba(190, 206, 230, 0.08); color: #d1dced; }}
                    .rankings-table tr:hover {{ background-color: rgba(59, 130, 246, 0.08); }}
                </style>
                {table_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Sovereign Deep-Dive Dossier Section
    st.markdown("---")
    st.subheader("🔍 Sovereign Tri-Pillar Dossier")
    sel_country = st.selectbox(
        "Select Jurisdiction for Deep-Dive Profile:",
        options=df_index["country"].sort_values(),
    )
    rec = df_index[df_index["country"] == sel_country].iloc[0]

    d1, d2, d3, d4, d5 = st.columns(5)
    d1.info(f"**Empirical Cluster:**\n{rec[cluster_col]}")
    d2.metric("Cable Landings", f"{int(rec['cable_landing_count'])}")
    d3.metric("Data Centers", f"{int(rec['datacenter_count'])}")
    d4.metric("Gov Risk (V-Dem)", f"{rec['governance_risk_score']}")
    d5.metric("Water Stress (WRI)", f"{rec['environmental_stress_score']}")

    case_studies = {
        "Egypt": """
        **Strategic Profile: The Sovereign Transcontinental Bottleneck**  
        Egypt constitutes the single most concentrated maritime data chokepoint on Earth, handling over 15% of all transcontinental internet traffic between Europe and Asia across the Suez transit corridor. State-owned **Telecom Egypt** maintains a statutory monopoly over terrestrial crossing rights, imposing steep transit tariffs and compulsory landing oversight. Combined with severe municipal water deficits (WRI 77.0) along the Nile Delta, the concentration of landing facilities in Alexandria and Port Said poses profound dual-risk exposure to physical interdiction and authoritarian telemetry interception.
        """,
        "Singapore": """
        **Strategic Profile: The Ecological Ceiling on Island Compute**  
        Singapore functions as Southeast Asia’s undisputed digital switching capital, anchoring dozens of major trans-Pacific and intra-Asian subsea cables. However, hyperscale compute expansion faces an acute ecological bottleneck: extreme water import vulnerability (WRI 76.0) and stringent domestic energy constraints prompted the government's multi-year data center moratorium. Singapore illustrates how geographic and hydrological limits force advanced regulatory standards for cooling efficiency and sustainable compute allocation.
        """,
        "Germany": """
        **Strategic Profile: The Institutional Buffer of DE-CIX Frankfurt**  
        Anchored by the world-leading DE-CIX Internet Exchange in Frankfurt, Germany represents a dense compute nexus (Physical Density 54.2) insulated by high institutional durability. Under the V-Dem civil liberties framework, judicial independence and statutory data protection (GDPR) act as an institutional buffer against arbitrary executive interdiction, while temperate hydrology keeps cooling-related water stress low (32.0).
        """,
        "China": """
        **Strategic Profile: Monolithic Infrastructure Density Under Total Surveillance**  
        China combines immense domestic hyperscale capacity and trans-Pacific landings with comprehensive state oversight. Under the Cybersecurity Law and Data Security Law, the boundary between private cloud tenants and state intelligence agencies is legally porous. Despite substantial hydroelectric resources in the south, major compute clusters in northern and western provinces face significant hydrological strain, exacerbating its status as the highest aggregate exposure jurisdiction globally.
        """,
        "United States": """
        **Strategic Profile: Massive Physical Aggregation vs. Localized Aridification**  
        The United States remains the structural core of global AI training clusters (Physical Density 88.9). While federal judicial review and property rights provide robust institutional insulation, extreme compute concentration in hydrological stress corridors (e.g., Northern Virginia's watershed demands, Arizona, and Utah) creates acute municipal friction between cooling requirements and local residential aquifers.
        """,
    }

    if sel_country in case_studies:
        clean_text = textwrap.dedent(case_studies[sel_country]).strip()
        st.markdown(
            f"""
            <div style="background-color: #132035; border: 1px solid rgba(190, 206, 230, 0.2); border-left: 4px solid #3b82f6; border-radius: 4px; padding: 18px 22px; margin-top: 16px; font-size: 0.95rem; line-height: 1.6; color: #d1dced;">
                {clean_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.download_button(
        label="📥 Download Active Subset (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="tri_pillar_ai_infrastructure_risk.csv",
        mime="text/csv",
    )

# =========================================================================
# TAB 2: GLOBAL RISK HEATMAP
# =========================================================================
with tab_heatmap:
    st.markdown("## 🔥 Global Infrastructure & Risk Heatmap")
    st.markdown(
        """
        <p style="font-size: 1.05rem; color: #d1dced; margin-bottom: 20px;">
        Visualize global concentration zones as a dynamic thermal intensity map. Select a tri-pillar metric to weight infrastructure coordinates by sovereign risk severity.
        </p>
        """,
        unsafe_allow_html=True,
    )

    h_col1, h_col2, h_col3 = st.columns([2, 1, 1])

    with h_col1:
        metric_choice = st.selectbox(
            "Select Heatmap Weighting Dimension:",
            options=[
                "composite_exposure_score",
                "governance_risk_score",
                "environmental_stress_score",
                "physical_density_score",
            ],
            format_func=lambda x: {
                "composite_exposure_score": "Composite Exposure Score (Tri-Pillar)",
                "governance_risk_score": "Pillar 2: V-Dem Governance Fragility",
                "environmental_stress_score": "Pillar 3: WRI Water Cooling Stress",
                "physical_density_score": "Pillar 1: Physical Infrastructure Density",
            }[x],
        )

    with h_col2:
        blur_val = st.slider(
            "Heatmap Dispersion (Blur):", min_value=10, max_value=35, value=18
        )

    with h_col3:
        radius_val = st.slider("Point Radius:", min_value=8, max_value=30, value=15)

    heatmap_df = df_cables.merge(
        df_index[["country", metric_choice]], on="country", how="inner"
    ).dropna(subset=["latitude", "longitude", metric_choice])

    if not heatmap_df.empty:
        max_val = heatmap_df[metric_choice].max()
        min_val = heatmap_df[metric_choice].min()
        spread = (max_val - min_val) if max_val != min_val else 1.0

        heatmap_df["weight"] = 0.15 + 0.85 * (
            (heatmap_df[metric_choice] - min_val) / spread
        )

        heat_data = heatmap_df[["latitude", "longitude", "weight"]].values.tolist()

        m_heat = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles="OpenStreetMap",
            control_scale=True,
        )

        gradient_palette = {
            0.2: "#38bdf8",
            0.4: "#22c55e",
            0.7: "#eab308",
            1.0: "#ef4444",
        }

        HeatMap(
            heat_data,
            radius=radius_val,
            blur=blur_val,
            max_zoom=6,
            gradient=gradient_palette,
            min_opacity=0.35,
        ).add_to(m_heat)

        raw_heat_html = m_heat._repr_html_()
        dark_tile_style = """
        <style>
            .leaflet-tile {
                filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3) !important;
            }
            .leaflet-container {
                background: #080d17 !important;
            }
        </style>
        """
        if "<head>" in raw_heat_html:
            heat_html = raw_heat_html.replace("<head>", f"<head>{dark_tile_style}")
        else:
            heat_html = dark_tile_style + raw_heat_html

        components.html(heat_html, width=1080, height=540)
    else:
        st.warning("Insufficient geospatial data points available for this selection.")

# =========================================================================
# TAB 3: RESEARCHER & POLICY APPLICATIONS
# =========================================================================
with tab_researchers:
    st.markdown("## 🔬 Empirical Applications for Scholars & Policy Teams")
    st.markdown(
        """
    <p style="font-size: 1.05rem; color: #d1dced; line-height: 1.6;">
    By linking geospatial infrastructure datasets with institutional governance and municipal resource fragility, 
    the index enables research across four interdisciplinary domains:
    </p>
    """,
        unsafe_allow_html=True,
    )

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(
            """
        <div class="research-card">
            <h4>1. Compute-Sovereignty Decoupling & Supply Chain Shocks</h4>
            <p style="color: #d1dced; font-size: 0.95rem; line-height: 1.55;">
            Evaluate how frontier AI developers and national cloud programs face regulatory or physical interdiction in high-risk transit hubs. Quantifies exposure in jurisdictions that combine concentrated transit assets with low rule-of-law protections.
            </p>
            <p style="color: #60a5fa; font-size: 0.88rem; font-weight: 600; margin-top: 10px;">Key Research Question: How do institutional preemption risks alter global routing topologies?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
        <div class="research-card">
            <h4>2. Ecological Constraints on Hyperscale Expansion</h4>
            <p style="color: #d1dced; font-size: 0.95rem; line-height: 1.55;">
            Cross-references data center concentration against WRI baseline water stress. Highlights jurisdictions where explosive growth in AI training and inference facilities conflicts directly with local municipal water tables and agricultural baselines.
            </p>
            <p style="color: #60a5fa; font-size: 0.88rem; font-weight: 600; margin-top: 10px;">Key Research Question: Where does the physical cooling footprint of compute create localized resource conflict?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with r2:
        st.markdown(
            """
        <div class="research-card">
            <h4>3. Authoritarian Telemetry Interception & Data Localization</h4>
            <p style="color: #d1dced; font-size: 0.95rem; line-height: 1.55;">
            Isolates states where high physical transit density intersects with aggressive civil liberties restrictions. Provides empirical foundation for tracking state-compelled telemetry collection, lawful intercept backdoors, and statutory localization mandates.
            </p>
            <p style="color: #60a5fa; font-size: 0.88rem; font-weight: 600; margin-top: 10px;">Key Research Question: Does physical infrastructure capture enable extraterritorial data surveillance?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
        <div class="research-card">
            <h4>4. Enterprise AI Risk Audits & Compliance</h4>
            <p style="color: #d1dced; font-size: 0.95rem; line-height: 1.55;">
            Enables enterprise compliance officers, cloud architects, and risk analysts to stress-test their physical compute footprints. The composite exposure metric flags hidden dependencies on single-point-of-failure coastal stations and authoritarian legal environments.
            </p>
            <p style="color: #60a5fa; font-size: 0.88rem; font-weight: 600; margin-top: 10px;">Key Research Question: Where are corporate compute dependencies vulnerable to regulatory or physical seizure?</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# =========================================================================
# TAB 4: THEORETICAL FRAMEWORK
# =========================================================================
with tab_theory:
    st.markdown("## 🏛️ Theoretical Thesis: The Materiality of AI")
    st.markdown(
        """
    <div class="theory-box">
        <p style="font-size: 1.15rem; font-style: italic; color: #f0f4f8; margin: 0; line-height: 1.6;">
        "Artificial Intelligence is not an abstract cloud; it is an extractive physical industry. Its frontier capabilities require gigawatt-scale power grids, millions of gallons of evaporative cooling water, and thousands of miles of seabed fiber-optic conduits anchored in physical sovereign territory."
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    t1, t2 = st.columns(2)
    with t1:
        st.markdown(
            """
        ### 1. Physical Vulnerability vs. The Cloud Myth
        While modern cloud marketing suggests compute is distributed and frictionless, the physical reality is concentrated. Transoceanic data transit relies on fewer than 600 subsea cable systems. These conduits land at concentrated, vulnerable coastal chokepoints—such as the Suez Canal, Egypt, the Strait of Malacca, and the English Channel.
        """
        )
    with t2:
        st.markdown(
            """
        ### 2. Institutional Vulnerability & Coercive State Capacity
        When physical infrastructure is hosted in illiberal jurisdictions, legal protections against arbitrary state intervention disappear. Without independent judicial review, governments can enforce lawful intercept orders, demand model weights or training telemetry, or physically sever cables during geopolitical crises.
        """
        )

# =========================================================================
# TAB 5: DATA ARCHITECTURE
# =========================================================================
with tab_pipeline:
    st.markdown("## ⚙️ Tri-Pillar Pipeline & Mathematical Formulation")
    st.markdown(
        """
    The index processes multi-source geospatial, institutional, and environmental data through a reproducible four-stage architecture:
    """
    )

    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            """
        #### 1. Physical Density Index ($P_i$)
        $$P_i = 12.5 \\times \\left[0.5 \\ln(1 + C_i) + 0.5 \\ln(1 + D_i)\\right]$$
        *Logarithmic transformation normalizes cable landings ($C_i$) and data centers ($D_i$), preventing extreme Western and East Asian clusters from skewing the global baseline.*
        
        #### 2. Institutional Governance Fragility ($G_i$)
        $$G_i = (1 - \\text{V-Dem}_{\\text{civlib}}) \\times 100$$
        *Inverts the V-Dem Civil Liberties Index (`v2x_civlib`), so higher values denote autocracy, lack of judicial independence, and state surveillance power.*
        """
        )
    with p2:
        st.markdown(
            """
        #### 3. Environmental Cooling Stress ($E_i$)
        $$E_i = \\left(\\frac{\\text{WRI Water Stress Score}}{5.0}\\right) \\times 100$$
        *Normalizes national baseline water stress from the World Resources Institute Aqueduct Atlas (0 = Low Stress, 100 = Extremely High Stress).*
        
        #### 4. Tri-Pillar Composite Exposure
        $$\\text{Exposure}_i = P_i \\times \\left(0.6 \\cdot \\frac{G_i}{100} + 0.4 \\cdot \\frac{E_i}{100}\\right)$$
        *Weights institutional vulnerability and environmental stress against physical asset concentration.*
        """
        )