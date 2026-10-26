import numpy as np
import pandas as pd

print("1. Loading physical infrastructure files...")
df_cables = pd.read_csv("cable_landing_stations.csv")
df_dc = pd.read_csv("datacenters.csv")

# Tidy country names in data centers to match cable data
country_col = "country" if "country" in df_dc.columns else df_dc.columns[0]

# Aggregate counts per country
cables_per_country = df_cables["country"].value_counts().reset_index()
cables_per_country.columns = ["country", "cable_landing_count"]

dc_per_country = df_dc[country_col].value_counts().reset_index()
dc_per_country.columns = ["country", "datacenter_count"]

# Standardize common variations (e.g. US names)
name_cleaner = {
    "USA": "United States",
    "US": "United States",
    "UK": "United Kingdom",
    "GB": "United Kingdom",
    "Korea, Republic of": "South Korea",
}
cables_per_country["country"] = (
    cables_per_country["country"].replace(name_cleaner).str.strip()
)
dc_per_country["country"] = (
    dc_per_country["country"].replace(name_cleaner).str.strip()
)

# Merge physical infrastructure counts
merged_infra = pd.merge(
    cables_per_country, dc_per_country, on="country", how="outer"
).fillna(0)

# Calculate a normalized Physical Asset Density Score (0 to 100)
# We apply log1p so massive hubs like US/UK don't completely flatten other nations
merged_infra["physical_density_score"] = np.round(
    (
        np.log1p(merged_infra["cable_landing_count"]) * 0.5
        + np.log1p(merged_infra["datacenter_count"]) * 0.5
    )
    * 12.5,
    1,
)

print(
    f"Aggregated physical data across {len(merged_infra)} distinct jurisdictions."
)
print("\n--- Top 10 Countries by Combined Physical Compute & Cable Density ---")
print(
    merged_infra.sort_values(by="physical_density_score", ascending=False)[
        [
            "country",
            "cable_landing_count",
            "datacenter_count",
            "physical_density_score",
        ]
    ].head(10)
)

merged_infra.to_csv("pillar1_physical_summary.csv", index=False)
print("\nSaved summary to pillar1_physical_summary.csv!")