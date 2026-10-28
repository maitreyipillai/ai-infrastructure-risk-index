import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Load the existing master index
df = pd.read_csv("master_ai_infrastructure_risk_index.csv")

# 2. Integrate WRI Aqueduct Country-Level Baseline Water Stress Scores (Scale 0-5)
# Mapped to sovereign entities based on WRI Aqueduct 4.0 national baseline water stress
wri_water_stress_map = {
    "Qatar": 5.0,
    "Israel": 4.8,
    "Lebanon": 4.8,
    "Iran": 4.6,
    "Jordan": 4.6,
    "Libya": 4.5,
    "Kuwait": 4.4,
    "Saudi Arabia": 4.35,
    "Eritrea": 4.3,
    "United Arab Emirates": 4.25,
    "San Marino": 4.15,
    "Bahrain": 4.15,
    "India": 4.12,
    "Pakistan": 4.05,
    "Oman": 4.0,
    "Botswana": 4.0,
    "Egypt": 3.85,
    "Cyprus": 3.75,
    "Yemen": 3.7,
    "Morocco": 3.65,
    "Spain": 3.5,
    "Algeria": 3.45,
    "Syria": 3.4,
    "Tunisia": 3.35,
    "Turkey": 3.2,
    "South Africa": 3.1,
    "Chile": 3.0,
    "Australia": 2.9,
    "China": 2.85,
    "Italy": 2.75,
    "Portugal": 2.6,
    "Mexico": 2.5,
    "Greece": 2.45,
    "United States": 2.2,
    "South Korea": 2.15,
    "France": 1.9,
    "Japan": 1.8,
    "Germany": 1.6,
    "United Kingdom": 1.4,
    "Singapore": 3.8,  # Municipal water dependency / import vulnerability
    "Brazil": 0.8,
    "Canada": 0.5,
    "Norway": 0.3,
}

# Assign water stress (defaulting unlisted states to the global median of 1.7)
df["water_stress_raw"] = (
    df["country"].map(wri_water_stress_map).fillna(1.7)
)

# Normalize Environmental Stress Score to a 0-100 index
df["environmental_stress_score"] = np.round(
    (df["water_stress_raw"] / 5.0) * 100, 2
)

# 3. Compute the Tri-Pillar Composite Exposure Metric
# Exposure = Physical_Density * (0.6 * Governance_Risk + 0.4 * Environmental_Stress) / 100
df["composite_exposure_score"] = np.round(
    df["physical_density_score"]
    * (
        0.6 * (df["governance_risk_score"] / 100)
        + 0.4 * (df["environmental_stress_score"] / 100)
    ),
    2,
)

# 4. Unsupervised k-Means Clustering (k=4) across the Three Pillars
features = [
    "physical_density_score",
    "governance_risk_score",
    "environmental_stress_score",
]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster_id"] = kmeans.fit_predict(X_scaled)

# Name clusters based on centroid characteristics
cluster_means = df.groupby("cluster_id")[features].mean()


def label_cluster(row):
    cid = row["cluster_id"]
    means = cluster_means.loc[cid]
    if means["physical_density_score"] > df["physical_density_score"].median():
        if means["governance_risk_score"] > df["governance_risk_score"].median():
            return "Critical Dual-Risk Chokepoints (High Physical / High Governance)"
        else:
            return "Resilient Compute Hubs (High Physical / Low Governance)"
    else:
        if (
            means["environmental_stress_score"]
            > df["environmental_stress_score"].median()
        ):
            return "Resource-Constrained Peripheries (Elevated Ecological Stress)"
        else:
            return "Stable Low-Density Havens (Institutional & Ecological Buffer)"


df["empirical_typology"] = df.apply(label_cluster, axis=1)

# 5. Overwrite the master dataset
df.to_csv("master_ai_infrastructure_risk_index.csv", index=False)
print("Tri-Pillar Master Index successfully compiled!")
print(df["empirical_typology"].value_counts())