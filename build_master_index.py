import numpy as np
import pandas as pd

print("1. Loading Pillar 1 (Physical) and Pillar 2 (Governance)...")
df_p1 = pd.read_csv("pillar1_physical_summary.csv")
df_p2 = pd.read_csv("pillar2_vdem_governance.csv")

# Filter out regional aggregates from V-Dem (e.g., 'Africa', 'World')
df_p2 = df_p2.dropna(subset=["iso_code"]).copy()

# Standardize common names for a seamless merge
country_alias = {
    "United States": "United States",
    "United Kingdom": "United Kingdom",
    "Russian Federation": "Russia",
    "Viet Nam": "Vietnam",
    "Iran (Islamic Republic of)": "Iran",
}
df_p1["country"] = df_p1["country"].replace(country_alias).str.strip()
df_p2["country"] = df_p2["country"].replace(country_alias).str.strip()

# Inner merge to keep jurisdictions present in both datasets
df_index = pd.merge(df_p1, df_p2, on="country", how="inner")

# Define Risk Quadrants using median splits
median_infra = df_index["physical_density_score"].median()
median_risk = df_index["governance_risk_score"].median()


def assign_quadrant(row):
    high_infra = row["physical_density_score"] >= median_infra
    high_risk = row["governance_risk_score"] >= median_risk

    if high_infra and high_risk:
        return "Critical Chokepoint (High Infra / High Risk)"
    elif high_infra and not high_risk:
        return "Resilient Hub (High Infra / Low Risk)"
    elif not high_infra and high_risk:
        return "Emerging Frontier (Low Infra / High Risk)"
    else:
        return "Stable Periphery (Low Infra / Low Risk)"


df_index["risk_quadrant"] = df_index.apply(assign_quadrant, axis=1)

# Composite Exposure Metric: Physical Density weighted by Governance Risk
# Higher score = greater infrastructure exposure to institutional volatility
df_index["composite_exposure_score"] = np.round(
    (
        df_index["physical_density_score"]
        * (df_index["governance_risk_score"] / 100.0)
    ),
    2,
)

# Sort by Composite Exposure Score descending
df_index = df_index.sort_values(by="composite_exposure_score", ascending=False)

print(f"\nIndexed {len(df_index)} sovereign jurisdictions.")
print("\n--- Top 10 High-Exposure Infrastructure Hubs ---")
cols_to_show = [
    "country",
    "cable_landing_count",
    "datacenter_count",
    "physical_density_score",
    "governance_risk_score",
    "composite_exposure_score",
    "risk_quadrant",
]
print(df_index[cols_to_show].head(10).to_string(index=False))

# Breakdown of countries by quadrant
print("\n--- Distribution Across Risk Quadrants ---")
print(df_index["risk_quadrant"].value_counts())

# Save master index
df_index.to_csv("master_ai_infrastructure_risk_index.csv", index=False)
print("\nSuccess! Saved to master_ai_infrastructure_risk_index.csv")