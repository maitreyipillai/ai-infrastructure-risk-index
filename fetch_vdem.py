import io
import numpy as np
import pandas as pd
import requests

# Open endpoint for V-Dem Human Rights / Civil Liberties Index (processed by OWID)
url = "https://ourworldindata.org/grapher/human-rights-index-vdem.csv?v=1&csvType=full&useColumnShortNames=false"

print("1. Downloading official V-Dem Civil Liberties / Human Rights index...")

# Use requests with standard browser headers to avoid SSL / blocking issues
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

# Read directly into pandas from the response text
df_vdem_raw = pd.read_csv(io.StringIO(response.text))
print(f"Total raw country-year records: {len(df_vdem_raw)}")

# Identify the human rights / civil liberties score column
score_col = [
    c
    for c in df_vdem_raw.columns
    if "Human rights" in c or "v2x_civlib" in c or "index" in c.lower()
][0]

# Filter for the most recent available observation per country (latest year)
df_recent = (
    df_vdem_raw.sort_values(by=["Entity", "Year"])
    .groupby("Entity")
    .last()
    .reset_index()
)

# Standardize column names
df_recent = df_recent[["Entity", "Code", "Year", score_col]].rename(
    columns={
        "Entity": "country",
        "Code": "iso_code",
        "Year": "vdem_year",
        score_col: "civil_liberties_score",
    }
)

# Standardize country names to match physical infrastructure data
name_map = {
    "United States": "United States",
    "United Kingdom": "United Kingdom",
    "Cote d'Ivoire": "Ivory Coast",
    "Democratic Republic of Congo": "DR Congo",
    "Korea, South": "South Korea",
}
df_recent["country"] = df_recent["country"].replace(name_map).str.strip()

# In V-Dem: 1 = high freedom/rights, 0 = severe repression/autocracy.
# For our *Risk* Pillar, we invert it so that 100 = Maximum Geopolitical/Rights Risk
df_recent["governance_risk_score"] = np.round(
    (1.0 - df_recent["civil_liberties_score"]) * 100, 1
)

print("\n--- Sample of Most Recent V-Dem Rights & Risk Scores ---")
print(
    df_recent[
        [
            "country",
            "iso_code",
            "vdem_year",
            "civil_liberties_score",
            "governance_risk_score",
        ]
    ].head(10)
)

# Save locally to CSV
df_recent.to_csv("pillar2_vdem_governance.csv", index=False)
print("\nSuccess! Saved clean governance metrics to pillar2_vdem_governance.csv")