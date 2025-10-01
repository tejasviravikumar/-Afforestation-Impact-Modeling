import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json

# Page configuration
st.set_page_config(
    page_title="🌱 Tree Planting CO₂ Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample data based on your chart
TREE_DATA = {
    "Bargad (Banyan)": {
      "Avg_Biomass_kg_per_year": 90,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 20,
      "CO2_Sequestration_20yrs": [115.6,231.21,346.81,462.42,578.02,693.63,809.23,924.84,1040.44,1156.05,1271.65,1387.26,1502.86,1618.47,1734.07,1849.68,1965.28,2080.89,2196.49,2312.1]
    },
    "Gulmohar": {
      "Avg_Biomass_kg_per_year": 45,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 20,
      "CO2_Sequestration_20yrs": [66.06,132.12,198.18,264.24,330.3,396.36,462.42,528.48,594.54,660.6,726.66,792.72,858.78,924.84,990.9,1056.96,1123.02,1189.08,1255.14,1321.2]
    },
    "Neem": {
      "Avg_Biomass_kg_per_year": 60,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.85,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [93.58,187.17,280.75,374.34,467.92,561.51,655.09,748.68,842.26,935.85,1029.43,1123.02,1216.61,1310.19,1403.77,1497.36,1590.94,1684.53,1778.11,1871.7]
    },
    "Peepal": {
      "Avg_Biomass_kg_per_year": 80,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [110.1,220.2,330.3,440.4,550.5,660.6,770.7,880.8,990.9,1101.0,1211.1,1321.2,1431.3,1541.4,1651.5,1761.6,1871.7,1981.8,2091.9,2202.0]
    },
    "Mango": {
      "Avg_Biomass_kg_per_year": 55,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [80.74,161.48,242.22,322.96,403.7,484.44,565.18,645.92,726.66,807.4,888.14,968.88,1049.62,1130.36,1211.1,1291.84,1372.58,1453.32,1534.06,1614.8]
    },
    "Teak": {
      "Avg_Biomass_kg_per_year": 70,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 50,
      "CO2_Sequestration_20yrs": [89.91,179.83,269.75,359.66,449.57,539.49,629.4,719.32,809.23,899.15,989.06,1078.98,1168.89,1258.81,1348.72,1438.64,1528.55,1618.47,1708.38,1798.3]
    },
    "Jamun": {
      "Avg_Biomass_kg_per_year": 50,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [68.81,137.62,206.44,275.25,344.06,412.88,481.69,550.5,619.31,688.12,756.94,825.75,894.56,963.38,1032.19,1101.0,1169.81,1238.62,1307.44,1376.25]
    },
    "Arjun": {
      "Avg_Biomass_kg_per_year": 65,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 40,
      "CO2_Sequestration_20yrs": [83.49,166.98,250.48,333.97,417.46,500.95,584.45,667.94,751.43,834.92,918.42,1001.91,1085.4,1168.89,1252.39,1335.88,1419.37,1502.86,1586.36,1669.85]
    },
    "Sal": {
      "Avg_Biomass_kg_per_year": 75,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.65,
      "Lifespan_Years": 50,
      "CO2_Sequestration_20yrs": [89.46,178.91,268.37,357.82,447.28,536.74,626.19,715.65,805.11,894.56,984.02,1073.47,1162.93,1252.39,1341.84,1431.3,1520.76,1610.21,1699.67,1789.12]
    },
    "Shisham (Sissoo)": {
      "Avg_Biomass_kg_per_year": 60,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 35,
      "CO2_Sequestration_20yrs": [77.07,154.14,231.21,308.28,385.35,462.42,539.49,616.56,693.63,770.7,847.77,924.84,1001.91,1078.98,1156.05,1233.12,1310.19,1387.26,1464.33,1541.4]
    },
    "Kadam": {
      "Avg_Biomass_kg_per_year": 55,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [75.69,151.39,227.08,302.77,378.47,454.16,529.86,605.55,681.24,756.94,832.63,908.32,984.02,1059.71,1135.41,1211.1,1286.79,1362.49,1438.18,1513.88]
    },
    "Mahua": {
      "Avg_Biomass_kg_per_year": 45,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.65,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [53.67,107.35,161.02,214.7,268.37,322.04,375.72,429.39,483.06,536.74,590.41,644.09,697.76,751.43,805.11,858.78,912.45,966.13,1019.8,1073.48]
    },
    "Tecoma (Yellow Bell)": {
      "Avg_Biomass_kg_per_year": 40,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [58.72,117.44,176.16,234.88,293.6,352.32,411.04,469.76,528.48,587.2,645.92,704.64,763.36,822.08,880.8,939.52,998.24,1056.96,1115.68,1174.4]
    },
    "Casuarina": {
      "Avg_Biomass_kg_per_year": 65,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [89.46,178.91,268.37,357.82,447.28,536.74,626.19,715.65,805.11,894.56,984.02,1073.47,1162.93,1252.39,1341.84,1431.3,1520.76,1610.21,1699.67,1789.12]
    },
    "Coconut": {
      "Avg_Biomass_kg_per_year": 70,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.85,
      "Lifespan_Years": 60,
      "CO2_Sequestration_20yrs": [109.18,218.36,327.55,436.73,545.91,655.09,764.28,873.46,982.64,1091.82,1201.01,1310.19,1419.37,1528.55,1637.74,1746.92,1856.1,1965.28,2074.47,2183.65]
    },
    "Kadamba": {
      "Avg_Biomass_kg_per_year": 55,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 35,
      "CO2_Sequestration_20yrs": [70.65,141.29,211.94,282.59,353.24,423.88,494.53,565.18,635.83,706.47,777.12,847.77,918.42,989.06,1059.71,1130.36,1201.01,1271.65,1342.3,1412.95]
    },
    "Babool (Acacia)": {
      "Avg_Biomass_kg_per_year": 50,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [68.81,137.62,206.44,275.25,344.06,412.88,481.69,550.5,619.31,688.12,756.94,825.75,894.56,963.38,1032.19,1101.0,1169.81,1238.62,1307.44,1376.25]
    },
    "Indian Laburnum (Amaltas)": {
      "Avg_Biomass_kg_per_year": 40,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [58.72,117.44,176.16,234.88,293.6,352.32,411.04,469.76,528.48,587.2,645.92,704.64,763.36,822.08,880.8,939.52,998.24,1056.96,1115.68,1174.4]
    },
    "Tamarind": {
      "Avg_Biomass_kg_per_year": 60,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 50,
      "CO2_Sequestration_20yrs": [82.57,165.15,247.72,330.3,412.87,495.45,578.02,660.6,743.17,825.75,908.32,990.9,1073.47,1156.05,1238.62,1321.2,1403.77,1486.35,1568.92,1651.5]
    },
    "Amla (Indian Gooseberry)": {
      "Avg_Biomass_kg_per_year": 45,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 40,
      "CO2_Sequestration_20yrs": [66.06,132.12,198.18,264.24,330.3,396.36,462.42,528.48,594.54,660.6,726.66,792.72,858.78,924.84,990.9,1056.96,1123.02,1189.08,1255.14,1321.2]
    },
    "Eucalyptus": {
      "Avg_Biomass_kg_per_year": 85,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.65,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [101.38,202.77,304.15,405.54,506.92,608.3,709.69,811.07,912.45,1013.84,1115.22,1216.61,1317.99,1419.37,1520.76,1622.14,1723.52,1824.91,1926.29,2027.68]
    },
    "Pongamia (Karanja)": {
      "Avg_Biomass_kg_per_year": 55,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 40,
      "CO2_Sequestration_20yrs": [ 70.65,141.29,211.94,282.59,353.24,423.88,494.53,565.18,635.83,706.47,777.12,847.77,918.42,989.06,1059.71,1130.36,1201.01,1271.65,1342.3,1412.95]
    },
    "Jackfruit": {
      "Avg_Biomass_kg_per_year": 75,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 50,
      "CO2_Sequestration_20yrs": [96.34,192.67,289.01,385.35,481.69,578.02,674.36,770.7,867.04,963.37,1059.71,1156.05,1252.39,1348.72,1445.06,1541.4,1637.74,1734.07,1830.41,1926.75]
    },
    "Fig (Anjeer)": {
      "Avg_Biomass_kg_per_year": 50,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [68.81,137.62,206.44,275.25,344.06,412.88,481.69,550.5,619.31,688.12,756.94,825.75,894.56,963.38,1032.19,1101.0,1169.81,1238.62,1307.44,1376.25]
    },
    "Palmyra Palm (Borassus)": {
      "Avg_Biomass_kg_per_year": 65,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 60,
      "CO2_Sequestration_20yrs": [83.49,166.98,250.48,333.97,417.46,500.95,584.45,667.94,751.43,834.92,918.42,1001.91,1085.4,1168.89,1252.39,1335.88,1419.37,1502.86,1586.36,1669.85]
    },
    "Silk Cotton (Semal)": {
      "Avg_Biomass_kg_per_year": 55,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [70.65,141.29,211.94,282.59,353.24,423.88,494.53,565.18,635.83,706.47,777.12,847.77,918.42,989.06,1059.71,1130.36,1201.01,1271.65,1342.3,1412.95]
    },
    "Indian Coral Tree (Erythrina)": {
      "Avg_Biomass_kg_per_year": 40,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 20,
      "CO2_Sequestration_20yrs": [55.05,110.1,165.15,220.2,275.25,330.3,385.35,440.4,495.45,550.5,605.55,660.6,715.65,770.7,825.75,880.8,935.85,990.9,1045.95,1101.0]
    },
    "Bael (Aegle marmelos)": {
      "Avg_Biomass_kg_per_year": 45,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 35,
      "CO2_Sequestration_20yrs": [66.06,132.12,198.18,264.24,330.3,396.36,462.42,528.48,594.54,660.6,726.66,792.72,858.78,924.84,990.9,1056.96,1123.02,1189.08,1255.14,1321.2]
    },
    "Flame of the Forest (Palash)": {
      "Avg_Biomass_kg_per_year": 50,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 30,
      "CO2_Sequestration_20yrs": [64.22,128.45,192.67,256.9,321.12,385.35,449.57,513.8,578.02,642.25,706.47,770.7,834.92,899.15,963.37,1027.6,1091.82,1156.05,1220.27,1284.5]
    },
    "Bamboo": {
      "Avg_Biomass_kg_per_year": 100,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.85,
      "Lifespan_Years": 15,
      "CO2_Sequestration_20yrs": [155.97,311.95,467.92,623.9,779.88,935.85,1091.83,1247.8,1403.77,1559.75,1715.72,1871.7,2027.67,2183.65,2339.62,2339.62,2339.62,2339.62,2339.62,2339.62]
    },
    "Subabul (Leucaena)": {
      "Avg_Biomass_kg_per_year": 60,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.8,
      "Lifespan_Years": 20,
      "CO2_Sequestration_20yrs": [88.08,176.16,264.24,352.32,440.4,528.48,616.56,704.64,792.72,880.8,968.88,1056.96,1145.04,1233.12,1321.2,1409.28,1497.36,1585.44,1673.52,1761.6]
    },
    "Red Sandalwood": {
      "Avg_Biomass_kg_per_year": 70,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.65,
      "Lifespan_Years": 40,
      "CO2_Sequestration_20yrs": [83.49,166.98,250.48,333.97,417.46,500.95,584.45,667.94,751.43,834.92,918.42,1001.91,1085.4,1168.89,1252.39,1335.88,1419.37,1502.86,1586.36,1669.85]
    },
    "Ashoka Tree (Saraca asoca)": {
      "Avg_Biomass_kg_per_year": 45,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.75,
      "Lifespan_Years": 25,
      "CO2_Sequestration_20yrs": [61.93,123.86,185.79,247.73,309.66,371.59,433.52,495.45,557.38,619.31,681.24,743.18,805.11,867.04,928.97,990.9,1052.83,1114.76,1176.69,1238.62]
    },
    "Indian Kino (Pterocarpus marsupium)": {
      "Avg_Biomass_kg_per_year": 65,
      "Carbon_Content_Ratio": 0.5,
      "CO2_Conversion_Factor": 3.67,
      "Survival_Rate": 0.7,
      "Lifespan_Years": 40,
      "CO2_Sequestration_20yrs": [83.49,166.98,250.48,333.97,417.46,500.95,584.45,667.94,751.43,834.92,918.42,1001.91,1085.4,1168.89,1252.39,1335.88,1419.37,1502.86,1586.36,1669.85]
    }
}

def main():
    # Title and description
    st.title("🌱 Tree Planting CO₂ Impact Dashboard")
    st.markdown("**Visualize the carbon sequestration potential of different tree species over 20 years**")
    
    # Sidebar for controls
    st.sidebar.header("🌳 Tree Selection & Planning")
    
    # Select All / Deselect All buttons
    col1, col2 = st.sidebar.columns(2)
    select_all = col1.button("Select All")
    deselect_all = col2.button("Deselect All")
    
    # Initialize session state for species selection
    if 'selected_species' not in st.session_state:
        st.session_state.selected_species = list(TREE_DATA.keys())[:3]  # Default selection
    
    if select_all:
        st.session_state.selected_species = list(TREE_DATA.keys())
    if deselect_all:
        st.session_state.selected_species = []
    
    # Species selection with number of trees
    st.sidebar.subheader("Select Species & Quantity")
    selected_species = {}
    
    for species in TREE_DATA.keys():
        col1, col2 = st.sidebar.columns([3, 1])
        
        # Checkbox for species selection
        is_selected = col1.checkbox(
            species, 
            value=species in st.session_state.selected_species,
            key=f"check_{species}"
        )
        
        # Number input for quantity
        if is_selected:
            num_trees = col2.number_input(
                "", 
                min_value=1, 
                max_value=10000, 
                value=100,
                key=f"num_{species}",
                label_visibility="collapsed"
            )
            selected_species[species] = num_trees
    
    # Update session state
    st.session_state.selected_species = list(selected_species.keys())
    
    if not selected_species:
        st.warning("Please select at least one tree species to see the analysis.")
        return
    
    # Calculate metrics
    total_trees = sum(selected_species.values())
    total_survivors = sum(
        num_trees * TREE_DATA[species]["Survival_Rate"] 
        for species, num_trees in selected_species.items()
    )
    total_co2_20yrs = sum(
        sum(TREE_DATA[species]["CO2_Sequestration_20yrs"]) * num_trees * TREE_DATA[species]["Survival_Rate"]
        for species, num_trees in selected_species.items()
    )
    
    # Display key metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌱 Total Trees Planted", f"{total_trees:,}")
    
    with col2:
        st.metric("🌳 Expected Survivors", f"{total_survivors:,.0f}")
    
    with col3:
        st.metric("🌍 Total CO₂ Captured (20 years)", f"{total_co2_20yrs:,.0f} kg")
    
    with col4:
        st.metric("♻️ CO₂ per Tree (avg)", f"{total_co2_20yrs/total_trees:,.0f} kg")
    
    # Create visualizations
    st.header("📈 CO₂ Sequestration Analysis")
    
    # 1. Line chart - CO₂ over 20 years
    st.subheader("CO₂ Sequestration Over 20 Years (Per Species)")
    
    # Prepare data for line chart
    years = list(range(1, 21))
    line_fig = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for i, (species, num_trees) in enumerate(selected_species.items()):
        survival_rate = TREE_DATA[species]["Survival_Rate"]
        co2_data = [
            co2_per_tree * num_trees * survival_rate 
            for co2_per_tree in TREE_DATA[species]["CO2_Sequestration_20yrs"]
        ]
        
        line_fig.add_trace(go.Scatter(
            x=years,
            y=co2_data,
            mode='lines',
            name=species,
            line=dict(
                color=colors[i % len(colors)],
                width=3,
                shape='spline',  # Smooth curves
                smoothing=0.3
            ),
            hovertemplate=f"<b>{species}</b><br>" +
                         "Year: %{x}<br>" +
                         "CO₂ Captured: %{y:,.0f} kg<extra></extra>"
        ))
    
    line_fig.update_layout(
        title="",
        xaxis_title="Year",
        yaxis_title="CO₂ Captured (kg)",
        hovermode='x unified',
        height=500,
        showlegend=True,
        template="plotly_white"
    )
    
    st.plotly_chart(line_fig, use_container_width=True)
    
    # 2. Area chart - Total CO₂ by species
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total CO₂ by Species (20-year sum)")
        
        species_totals = {}
        for species, num_trees in selected_species.items():
            survival_rate = TREE_DATA[species]["Survival_Rate"]
            total_co2 = sum(TREE_DATA[species]["CO2_Sequestration_20yrs"]) * num_trees * survival_rate
            species_totals[species] = total_co2
        
        # Create bar chart
        bar_fig = px.bar(
            x=list(species_totals.keys()),
            y=list(species_totals.values()),
            color=list(species_totals.values()),
            color_continuous_scale="Viridis"
        )
        
        bar_fig.update_layout(
            xaxis_title="Tree Species",
            yaxis_title="Total CO₂ Captured (kg)",
            showlegend=False,
            height=400,
            template="plotly_white"
        )
        
        bar_fig.update_xaxes(tickangle=45)
        
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with col2:
        st.subheader("CO₂ Contribution by Species")
        
        # Donut chart
        pie_fig = px.pie(
            values=list(species_totals.values()),
            names=list(species_totals.keys()),
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        pie_fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "CO₂: %{value:,.0f} kg<br>" +
                         "Percentage: %{percent}<extra></extra>"
        )
        
        pie_fig.update_layout(
            height=400,
            showlegend=True,
            template="plotly_white"
        )
        
        st.plotly_chart(pie_fig, use_container_width=True)
    
    # 3. Cumulative CO₂ area chart
    st.subheader("Cumulative CO₂ Sequestration Over Time")
    
    # Calculate cumulative data
    cumulative_fig = go.Figure()
    
    for i, (species, num_trees) in enumerate(selected_species.items()):
        survival_rate = TREE_DATA[species]["Survival_Rate"]
        annual_co2 = [
            co2_per_tree * num_trees * survival_rate 
            for co2_per_tree in TREE_DATA[species]["CO2_Sequestration_20yrs"]
        ]
        cumulative_co2 = np.cumsum(annual_co2)
        
        cumulative_fig.add_trace(go.Scatter(
            x=years,
            y=cumulative_co2,
            mode='lines',
            name=species,
            fill='tonexty' if i > 0 else 'tozeroy',
            line=dict(width=0.5),
            fillcolor=colors[i % len(colors)],
            hovertemplate=f"<b>{species}</b><br>" +
                         "Year: %{x}<br>" +
                         "Cumulative CO₂: %{y:,.0f} kg<extra></extra>"
        ))
    
    cumulative_fig.update_layout(
        title="",
        xaxis_title="Year",
        yaxis_title="Cumulative CO₂ Captured (kg)",
        hovermode='x unified',
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(cumulative_fig, use_container_width=True)
    
    # Data table
    st.header("📋 Species Details")
    
    # Create detailed dataframe
    details_data = []
    for species, num_trees in selected_species.items():
        data = TREE_DATA[species]
        total_co2_species = sum(data["CO2_Sequestration_20yrs"]) * num_trees * data["Survival_Rate"]
        
        details_data.append({
            "Species": species,
            "Trees Planted": num_trees,
            "Survival Rate": f"{data['Survival_Rate']:.0%}",
            "Expected Survivors": f"{num_trees * data['Survival_Rate']:.0f}",
            "Lifespan (years)": data["Lifespan_Years"],
            "Total CO₂ (20 years)": f"{total_co2_species:,.0f} kg",
            "CO₂ per Tree": f"{total_co2_species/num_trees:,.0f} kg"
        })
    
    df_details = pd.DataFrame(details_data)
    st.dataframe(df_details, use_container_width=True, hide_index=True)
    
    # Export functionality
    st.header("📥 Export Data")
    
    # Convert to CSV
    csv = df_details.to_csv(index=False)
    st.download_button(
        label="Download Species Details (CSV)",
        data=csv,
        file_name="tree_planting_analysis.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**🌱 Tree Planting CO₂ Dashboard** - Helping plan sustainable reforestation efforts")

if __name__ == "__main__":
    main()