import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load dataset
df = pd.read_csv("FRA_DATA.csv")

# Convert Tribal Population % from string to number
df["Tribal_Population_Percentage"] = df["Tribal_Population_Percentage"].str.replace("%", "").astype(float)

st.set_page_config(page_title="FRA DSS Prototype", layout="wide")

st.title("🌳 FRA Decision Support System (DSS) Prototype")
st.markdown("This DSS layers Central Sector Schemes (CSS) recommendations for FRA villages in Odisha.")

# Sidebar filters
st.sidebar.header("🔎 Filters")
districts = st.sidebar.multiselect("Select District(s)", df["District"].unique())
min_tribal = st.sidebar.slider("Minimum Tribal Population (%)", 0, 100, 0)

filtered_df = df.copy()
if districts:
    filtered_df = filtered_df[filtered_df["District"].isin(districts)]
filtered_df = filtered_df[filtered_df["Tribal_Population_Percentage"] >= min_tribal]

st.subheader("📌 Filtered Villages")
st.dataframe(filtered_df)

# Show recommendations table
st.subheader("✅ Scheme Recommendations")
st.dataframe(
    filtered_df[[
        "Village_Name",
        "District",
        "Tribal_Population_Percentage",
        "FRA_Claims_Count",
        "Ponds_Count",
        "Farms_Count",
        "Forest_Area_Hectares",
        "DSS_Recommendation"
    ]]
)

# Map visualization
st.subheader("🗺️ FRA Atlas (Prototype Map)")

m = folium.Map(location=[20.3, 85.8], zoom_start=6)

for _, row in filtered_df.iterrows():
    popup_text = f"""
    <b>Village:</b> {row['Village_Name']}<br>
    <b>District:</b> {row['District']}<br>
    <b>Tribal %:</b> {row['Tribal_Population_Percentage']}%<br>
    <b>FRA Claims:</b> {row['FRA_Claims_Count']}<br>
    <b>Ponds:</b> {row['Ponds_Count']}<br>
    <b>Farms:</b> {row['Farms_Count']}<br>
    <b>Forest Area:</b> {row['Forest_Area_Hectares']} ha<br>
    <b>Recommendation:</b> {row['DSS_Recommendation']}
    """
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_text,
        tooltip=row["Village_Name"],
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

st_folium(m, width=900, height=600)

st.success("✅ DSS Prototype running with FRA_DATA.csv")
